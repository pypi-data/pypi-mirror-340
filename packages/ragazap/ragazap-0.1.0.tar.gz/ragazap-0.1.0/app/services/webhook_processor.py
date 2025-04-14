import asyncio
import sys
from typing import Dict, Any, Optional, cast
from datetime import datetime
from loguru import logger
from pydantic import TypeAdapter, ValidationError

# Import necessary components from the new structure
from app.models.whatsapp import (
    IncomingMessageObject, IncomingTextMessage, IncomingButtonMessage,
    IncomingInteractiveMessage, IncomingLocationMessage, IncomingReactionMessage,
    IncomingImageMessage, IncomingAudioMessage, IncomingVideoMessage,
    IncomingDocumentMessage, IncomingStickerMessage
)
from app.models.internal_state import StoredMessageTurn, MessageRole, IncomingMessageType
from app.utils.redis_client import add_message_turn_to_history, mark_whatsapp_message_read, get_redis_client
from app.core.config import settings
from app.zap_mcp_server.tenant_settings import get_waba_for_phone, WABASettings

async def process_incoming_message(value: Dict[str, Any]):
    """Processes a single incoming message value from the webhook."""
    messages = value.get("messages", [])
    contacts = value.get("contacts", [])

    if not messages or not contacts:
        logger.warning("Webhook: Skipping value object without messages or contacts.")
        return

    contact = contacts[0] # Assuming one contact per message notification
    sender_wa_id = contact.get("wa_id")
    sender_name = contact.get("profile", {}).get("name")

    if not sender_wa_id:
        logger.error("Webhook message received without sender WA ID. Skipping.")
        return

    message_data = messages[0] # Assuming one message per notification

    try:
        # Get recipient phone number ID from metadata
        recipient_phone_number_id = value.get("metadata", {}).get("phone_number_id")
        if not recipient_phone_number_id:
            logger.error("Could not determine recipient phone number ID from webhook metadata. Skipping.")
            return

        # In client mode, verify we have the WABA settings for this phone
        waba_settings: Optional[WABASettings] = None
        if not settings.STANDALONE_MODE:
            waba_dict = get_waba_for_phone(recipient_phone_number_id)
            if waba_dict:
                waba_settings = WABASettings.model_validate(waba_dict)
            if not waba_settings:
                logger.error(f"No WABA settings found for phone {recipient_phone_number_id} in client mode. Skipping.")
                return

        # Validate the structure
        incoming_message = TypeAdapter(IncomingMessageObject).validate_python(message_data)

        logger.info(f"Webhook: Received message type {incoming_message.type.value} from {sender_wa_id} ({sender_name}) WAMID: {incoming_message.id}")

        # --- Mark as Read Immediately (Run in background) --- #
        if settings.STANDALONE_MODE:
            # In standalone mode, use settings directly
            if settings.BUSINESS_PHONE_NUMBER_ID:
                asyncio.create_task(mark_whatsapp_message_read(wamid=incoming_message.id))
            else:
                logger.warning("BUSINESS_PHONE_NUMBER_ID not set, cannot mark message as read.")
        else:
            # In client mode, use WABA settings
            if waba_settings and waba_settings.api_token:
                asyncio.create_task(mark_whatsapp_message_read(wamid=incoming_message.id))
            else:
                logger.warning(f"No API token found for WABA of phone {recipient_phone_number_id}, cannot mark message as read.")

        # --- Extract Content --- #
        message_content = "Unsupported message type" # Default
        if isinstance(incoming_message, IncomingTextMessage) and incoming_message.text:
            message_content = incoming_message.text.body
        elif isinstance(incoming_message, IncomingButtonMessage) and incoming_message.button:
            message_content = f"Button Clicked: '{incoming_message.button.text}' (Payload: {incoming_message.button.payload})"
        elif isinstance(incoming_message, IncomingInteractiveMessage) and incoming_message.interactive:
            if incoming_message.interactive.type == "button_reply" and incoming_message.interactive.button_reply:
                message_content = f"Replied Button: '{incoming_message.interactive.button_reply.title}' (ID: {incoming_message.interactive.button_reply.id})"
            elif incoming_message.interactive.type == "list_reply" and incoming_message.interactive.list_reply:
                message_content = f"Selected List Item: '{incoming_message.interactive.list_reply.title}' (ID: {incoming_message.interactive.list_reply.id})"
            else:
                message_content = f"Received interactive message (type: {incoming_message.interactive.type})"
        elif isinstance(incoming_message, (IncomingImageMessage, IncomingAudioMessage, IncomingVideoMessage, IncomingDocumentMessage, IncomingStickerMessage)):
            media_attr = getattr(incoming_message, incoming_message.type.value, None)
            message_content = f"Received {incoming_message.type.value}"
            if media_attr:
                if hasattr(media_attr, 'caption') and media_attr.caption:
                    message_content += f" with caption: {media_attr.caption}"
                elif hasattr(media_attr, 'filename') and media_attr.filename:
                    message_content += f": {media_attr.filename}"
        elif isinstance(incoming_message, IncomingReactionMessage) and incoming_message.reaction:
            message_content = f"Reacted '{incoming_message.reaction.emoji}' to message {incoming_message.reaction.message_id}"
        elif isinstance(incoming_message, IncomingLocationMessage) and incoming_message.location:
            message_content = f"Shared Location: Lat {incoming_message.location.latitude}, Lon {incoming_message.location.longitude}" + (f" ({incoming_message.location.name})" if incoming_message.location.name else "")

        # --- Update State (Name and History in Redis) --- #
        redis = await get_redis_client()
        if redis and sender_name:
            try:
                # Create a coroutine for setting the contact name
                async def set_contact_name():
                    await redis.set(f"contact_name:{sender_wa_id}", sender_name)
                # Run in background to avoid blocking webhook response
                asyncio.create_task(set_contact_name())
            except Exception as e:
                logger.error(f"Error setting contact name in Redis for {sender_wa_id}: {e}")

        # Create the message turn data
        turn_data = StoredMessageTurn(
            wamid=incoming_message.id,
            sender_wa_id=sender_wa_id,
            recipient_wa_id=recipient_phone_number_id,
            role=MessageRole.USER,
            content=message_content,
            message_type=IncomingMessageType(incoming_message.type.value),  # Convert to internal state enum
            timestamp=datetime.fromtimestamp(int(incoming_message.timestamp)),
            is_read=True,
            raw_message_data=incoming_message.model_dump(mode='json')
        ).model_dump(mode='json')

        # Add message turn to Redis history if Redis is available
        if redis:
            asyncio.create_task(add_message_turn_to_history(sender_wa_id, turn_data))
            logger.debug(f"State updated in Redis for {sender_wa_id}")
        else:
            logger.debug(f"Redis not available, skipping state update for {sender_wa_id}")

    except ValidationError as e:
        logger.error(f"Webhook: Error validating incoming message: {e}")
    except AttributeError as e:
        logger.error(f"Webhook: Error accessing message attribute: {e}")
    except ConnectionError as e:
        logger.error(f"Webhook: Redis connection error: {e}")
    except Exception as e:
        logger.error(f"Webhook: Unexpected error processing message: {e}", exc_info=True) 