from loguru import logger
from mcp.server.fastmcp import FastMCP # Assuming this path is correct for your SDK
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import asyncio
import httpx
import uuid

# Import necessary components from the new structure
from app.core.config import settings # Import settings
from app.utils.redis_client import get_redis_client
from app.utils.http_client import get_http_client
from app.models.internal_state import StoredMessageTurn, MessageRole, IncomingMessageType
from app.zap_mcp_server.completions import register_completion_handlers
from app.zap_mcp_server.session_manager import get_session_manager
from app.zap_mcp_server.context_manager import get_current_context, SessionContext
from app.zap_mcp_server.tenant_settings import (
    get_tenant_api_url, 
    get_tenant_api_token, 
    get_tenant_settings, 
    get_tenant_business_phone,
    get_tenant_phone_id,
    initialize_tenant_settings,
    get_api_url_for_phone,
    get_api_token_for_phone
)

# Define what symbols are exported from this module
__all__ = ["initialize_mcp_server", "get_mcp_server"]

# --- Global MCP Server Instance --- #
mcp_server: FastMCP | None = None

# --- Tool Definitions --- #

# Define Input/Output Models for Tools
class SendMessageInput(BaseModel):
    contact_wa_id: str = Field(..., description="The WhatsApp ID of the recipient.")
    message_text: str = Field(..., description="The text content of the message to send.")
    from_phone_id: Optional[str] = Field(None, description="Optional specific phone number ID to send from. If not provided, the default will be used.")

class SendMessageOutput(BaseModel):
    wamid: str = Field(..., description="The WAMID of the sent message.")
    status: str = Field(default="sent", description="Initial status of the message (usually 'sent').")

class SetContextInput(BaseModel):
    scope: str = Field(..., description="The context scope to store the value in (e.g., 'conversation', 'user', 'system', 'contact', 'memory').")
    key: str = Field(..., description="The key to store the value under.")
    value: Any = Field(..., description="The value to store.")
    ttl: Optional[int] = Field(None, description="Optional time-to-live in seconds.")

class SetContextOutput(BaseModel):
    success: bool = Field(True, description="Whether the operation was successful.")
    message: str = Field("Context value set successfully.", description="A message describing the result.")

class GetContextInput(BaseModel):
    scope: str = Field(..., description="The context scope to get the value from.")
    key: str = Field(..., description="The key to get the value for.")
    default: Optional[Any] = Field(None, description="Default value to return if the key doesn't exist.")

class GetContextOutput(BaseModel):
    success: bool = Field(True, description="Whether the operation was successful.")
    value: Optional[Any] = Field(None, description="The retrieved value.")
    exists: bool = Field(False, description="Whether the key exists in the context.")

class ClearContextInput(BaseModel):
    scope: str = Field(..., description="The context scope to clear.")

class ClearContextOutput(BaseModel):
    success: bool = Field(True, description="Whether the operation was successful.")
    message: str = Field("Context scope cleared successfully.", description="A message describing the result.")

class GetContextScopesOutput(BaseModel):
    scopes: List[str] = Field([], description="List of available context scopes.")
    success: bool = Field(True, description="Whether the operation was successful.")

class GetContextSnapshotOutput(BaseModel):
    snapshot: Dict[str, Dict[str, Any]] = Field({}, description="A snapshot of all current context values across scopes.")
    success: bool = Field(True, description="Whether the operation was successful.")

class ConfigureTenantInput(BaseModel):
    """Input for configuring tenant settings."""
    business_phone_number_id: Optional[str] = Field(None, description="The WhatsApp Business Phone Number ID.")
    business_phone_number: Optional[str] = Field(None, description="The WhatsApp Business Phone Number (with country code).")
    whatsapp_api_token: Optional[str] = Field(None, description="The WhatsApp API Token for authentication.")
    meta_api_version: Optional[str] = Field(None, description="The Meta API version to use.")
    business_name: Optional[str] = Field(None, description="The name of the business.")
    waba_id: Optional[str] = Field(None, description="The WhatsApp Business Account ID.")
    display_name: Optional[str] = Field(None, description="The display name for the business.")

class ConfigureTenantOutput(BaseModel):
    """Output from configuring tenant settings."""
    success: bool = Field(True, description="Whether the operation was successful.")
    message: str = Field("Tenant settings configured successfully.", description="A message describing the result.")
    settings: Dict[str, Any] = Field({}, description="The current tenant settings after configuration.")

class ConfigureWABAInput(BaseModel):
    """Input for configuring a WhatsApp Business Account."""
    waba_id: str = Field(..., description="The WABA ID from Meta.")
    business_name: str = Field(..., description="The name of the business.")
    api_token: str = Field(..., description="The API token for this WABA.")
    api_version: Optional[str] = Field(None, description="The API version to use.")
    display_name: Optional[str] = Field(None, description="A friendly display name.")
    webhook_verification_token: Optional[str] = Field(None, description="The webhook verification token.")
    make_default: bool = Field(False, description="Whether to make this the default WABA.")

class ConfigurePhoneInput(BaseModel):
    """Input for configuring a WhatsApp phone number."""
    waba_id: str = Field(..., description="The parent WABA ID this phone belongs to.")
    phone_id: str = Field(..., description="The phone number ID from Meta.")
    display_number: Optional[str] = Field(None, description="The formatted phone number with country code.")
    display_name: Optional[str] = Field(None, description="A friendly display name.")
    make_default: bool = Field(False, description="Whether to make this the default phone for its WABA.")

class ConfigureMultiTenantOutput(BaseModel):
    """Output from tenant configuration operations."""
    success: bool = Field(True, description="Whether the operation was successful.")
    message: str = Field("Configuration successful.", description="A message describing the result.")
    waba_count: int = Field(0, description="The current number of WABAs.")
    phone_count: int = Field(0, description="The current number of phone numbers.")
    default_waba_id: Optional[str] = Field(None, description="The ID of the default WABA.")
    default_phone_id: Optional[str] = Field(None, description="The ID of the default phone number.")

async def send_whatsapp_message(input_data: SendMessageInput) -> SendMessageOutput:
    """Sends a text message to a WhatsApp contact using the Cloud API."""
    logger.info(f"MCP Tool: Received request to send message to {input_data.contact_wa_id}")
    
    # Get the active session manager
    session_manager = await get_session_manager()
    
    # If there's a current client session in request context, update it
    current_session = getattr(asyncio.current_task(), "mcp_session", None)
    if current_session:
        current_session.set_active_contact(input_data.contact_wa_id)
        await session_manager.update_session(current_session)
    
    # Determine which phone number to use for sending
    sender_phone_id = input_data.from_phone_id or get_tenant_phone_id()
    
    # Get tenant-specific settings for this phone
    api_url = get_api_url_for_phone(sender_phone_id)
    api_token = get_api_token_for_phone(sender_phone_id)
    
    # Log the tenant info for debugging
    tenant_settings = get_tenant_settings()
    if tenant_settings:
        tenant = tenant_settings.get("wabas", [])
        logger.debug(f"Using phone ID: {sender_phone_id} from {len(tenant)} WABAs")
    else:
        logger.debug("No tenant settings available, using defaults")
    
    http_client = await get_http_client()
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": input_data.contact_wa_id,
        "type": "text",
        "text": {"preview_url": False, "body": input_data.message_text}
    }
    try:
        response = await http_client.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        sent_wamid = response_data.get("messages", [{}])[0].get("id")
        if not sent_wamid:
            raise ValueError("Could not extract WAMID from API response")

        logger.info(f"Successfully sent message to {input_data.contact_wa_id} from {sender_phone_id}, WAMID: {sent_wamid}")

        # --- Log Agent Message to Redis --- #
        turn_data = StoredMessageTurn(
            wamid=sent_wamid,
            sender_wa_id=sender_phone_id, # Use the specific phone ID that sent the message
            recipient_wa_id=input_data.contact_wa_id,
            role=MessageRole.AGENT,
            content=input_data.message_text,
            message_type=IncomingMessageType.AGENT,
            timestamp=datetime.now(),
            is_read=False
        ).model_dump(mode='json')

        # Add to history (fire and forget)
        from app.utils.redis_client import add_message_turn_to_history # Local import avoids cycle
        asyncio.create_task(add_message_turn_to_history(input_data.contact_wa_id, turn_data))

        return SendMessageOutput(wamid=sent_wamid)

    except httpx.HTTPStatusError as e:
        logger.error(f"Error sending message to {input_data.contact_wa_id} from {sender_phone_id}. Status: {e.response.status_code}, Response: {e.response.text}")
        # Re-raise for MCP error handling
        raise Exception(f"WhatsApp API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error(f"Failed to send message to {input_data.contact_wa_id} from {sender_phone_id}: {e}")
        raise

async def set_context_value(input_data: SetContextInput) -> SetContextOutput:
    """Sets a value in the current session's context."""
    logger.info(f"MCP Tool: Setting context value {input_data.scope}/{input_data.key}")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return SetContextOutput(success=False, message="No context available for current request")
    
    try:
        context.set(input_data.scope, input_data.key, input_data.value, input_data.ttl)
        return SetContextOutput(success=True, message=f"Context value set: {input_data.scope}/{input_data.key}")
    except Exception as e:
        logger.error(f"Error setting context value: {e}")
        return SetContextOutput(success=False, message=f"Error setting context value: {str(e)}")

async def get_context_value(input_data: GetContextInput) -> GetContextOutput:
    """Gets a value from the current session's context."""
    logger.info(f"MCP Tool: Getting context value {input_data.scope}/{input_data.key}")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return GetContextOutput(success=False, value=None, exists=False)
    
    try:
        value = context.get(input_data.scope, input_data.key, input_data.default)
        exists = context.has(input_data.scope, input_data.key)
        return GetContextOutput(success=True, value=value, exists=exists)
    except Exception as e:
        logger.error(f"Error getting context value: {e}")
        return GetContextOutput(success=False, value=None, exists=False)

async def clear_context_scope(input_data: ClearContextInput) -> ClearContextOutput:
    """Clears all values in a context scope."""
    logger.info(f"MCP Tool: Clearing context scope {input_data.scope}")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return ClearContextOutput(success=False, message="No context available for current request")
    
    try:
        context.clear_scope(input_data.scope)
        return ClearContextOutput(success=True, message=f"Context scope cleared: {input_data.scope}")
    except Exception as e:
        logger.error(f"Error clearing context scope: {e}")
        return ClearContextOutput(success=False, message=f"Error clearing context scope: {str(e)}")

async def get_context_scopes() -> GetContextScopesOutput:
    """Gets all available context scopes."""
    logger.info("MCP Tool: Getting context scopes")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return GetContextScopesOutput(scopes=[], success=False)
    
    try:
        scopes = context.list_scopes()
        return GetContextScopesOutput(scopes=scopes, success=True)
    except Exception as e:
        logger.error(f"Error getting context scopes: {e}")
        return GetContextScopesOutput(scopes=[], success=False)

async def get_context_snapshot() -> GetContextSnapshotOutput:
    """Gets a snapshot of all context values across all scopes."""
    logger.info("MCP Tool: Getting context snapshot")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return GetContextSnapshotOutput(snapshot={}, success=False)
    
    try:
        snapshot = context.create_snapshot()
        return GetContextSnapshotOutput(snapshot=snapshot, success=True)
    except Exception as e:
        logger.error(f"Error getting context snapshot: {e}")
        return GetContextSnapshotOutput(snapshot={}, success=False)

async def configure_tenant_settings(input_data: ConfigureTenantInput) -> ConfigureTenantOutput:
    """Configures tenant-specific WhatsApp Business API settings."""
    logger.info("MCP Tool: Configuring tenant settings")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return ConfigureTenantOutput(
            success=False, 
            message="No context available for current request",
            settings={}
        )
    
    try:
        # Get current settings
        tenant_settings = get_tenant_settings()
        if not tenant_settings:
            logger.warning("No existing tenant settings found, initializing")
            # Initialize if not present
            from app.zap_mcp_server.tenant_settings import initialize_tenant_settings
            initialize_tenant_settings(context)
            tenant_settings = get_tenant_settings() or {}
        
        # Update with new values
        updates = {}
        for field, value in input_data.model_dump(exclude_unset=True).items():
            if value is not None:
                context.set_tenant(field, value)
                updates[field] = value
        
        if "business_phone_number_id" in updates or "meta_api_version" in updates:
            # Regenerate API URL if key components changed
            meta_version = context.tenant("meta_api_version")
            phone_id = context.tenant("business_phone_number_id")
            api_url = f"https://graph.facebook.com/{meta_version}/{phone_id}/messages"
            context.set_tenant("api_url", api_url)
            updates["api_url"] = api_url
        
        # Update the settings dictionary
        tenant_settings.update(updates)
        context.set_tenant("settings", tenant_settings)
        
        logger.info(f"Tenant settings updated: {', '.join(updates.keys())}")
        return ConfigureTenantOutput(
            success=True,
            message=f"Tenant settings updated: {', '.join(updates.keys())}",
            settings=tenant_settings
        )
    except Exception as e:
        logger.error(f"Error configuring tenant settings: {e}")
        return ConfigureTenantOutput(
            success=False,
            message=f"Error configuring tenant settings: {str(e)}",
            settings=get_tenant_settings() or {}
        )

async def configure_waba(input_data: ConfigureWABAInput) -> ConfigureMultiTenantOutput:
    """Configures a WhatsApp Business Account."""
    logger.info(f"MCP Tool: Configuring WABA {input_data.waba_id}")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return ConfigureMultiTenantOutput(
            success=False,
            message="No context available for current request",
            waba_count=0,
            phone_count=0,
            default_waba_id=None,
            default_phone_id=None
        )
    
    try:
        # Get current tenant settings
        tenant_data = context.tenant("tenant_settings")
        if not tenant_data:
            # If not found, initialize with defaults
            from app.zap_mcp_server.tenant_settings import initialize_tenant_settings
            initialize_tenant_settings(context)
            tenant_data = context.tenant("tenant_settings")
            if not tenant_data:
                return ConfigureMultiTenantOutput(
                    success=False,
                    message="Failed to initialize tenant settings",
                    waba_count=0,
                    phone_count=0,
                    default_waba_id=None,
                    default_phone_id=None
                )
        
        # Convert to tenant model
        from app.zap_mcp_server.tenant_settings import TenantSettings, WABASettings
        tenant = TenantSettings(**tenant_data)
        
        # Check if WABA already exists
        existing_waba = None
        for waba in tenant.wabas:
            if waba.id == input_data.waba_id:
                existing_waba = waba
                break
        
        if existing_waba:
            # Update existing WABA
            existing_waba.business_name = input_data.business_name
            existing_waba.api_token = input_data.api_token
            if input_data.api_version:
                existing_waba.api_version = input_data.api_version
            if input_data.display_name:
                existing_waba.display_name = input_data.display_name
            if input_data.webhook_verification_token:
                existing_waba.webhook_verification_token = input_data.webhook_verification_token
            
            if input_data.make_default:
                tenant.default_waba_id = input_data.waba_id
                for waba in tenant.wabas:
                    waba.is_default = (waba.id == input_data.waba_id)
            
            logger.info(f"Updated existing WABA: {input_data.waba_id}")
            message = f"Updated existing WABA: {input_data.waba_id}"
        else:
            # Create new WABA
            new_waba = WABASettings(
                id=input_data.waba_id,
                business_name=input_data.business_name,
                api_token=input_data.api_token,
                api_version=input_data.api_version or "v18.0",
                display_name=input_data.display_name,
                webhook_verification_token=input_data.webhook_verification_token,
                is_default=input_data.make_default
            )
            
            tenant.add_waba(new_waba)
            
            if input_data.make_default:
                tenant.default_waba_id = input_data.waba_id
                for waba in tenant.wabas:
                    waba.is_default = (waba.id == input_data.waba_id)
            
            logger.info(f"Added new WABA: {input_data.waba_id}")
            message = f"Added new WABA: {input_data.waba_id}"
        
        # Update tenant settings in context
        context.set_tenant("tenant_settings", tenant.model_dump())
        
        # Update convenience fields
        default_waba = tenant.get_default_waba()
        default_phone = tenant.get_default_phone()
        
        if default_waba:
            context.set_tenant("default_waba_id", default_waba.id)
            context.set_tenant("default_api_token", default_waba.api_token)
            context.set_tenant("default_api_version", default_waba.api_version)
        
        if default_phone:
            context.set_tenant("default_phone_id", default_phone.id)
            context.set_tenant("default_phone_number", default_phone.display_number)
        
        # Count phones across all WABAs
        phone_count = sum(len(waba.phone_numbers) for waba in tenant.wabas)
        
        return ConfigureMultiTenantOutput(
            success=True,
            message=message,
            waba_count=len(tenant.wabas),
            phone_count=phone_count,
            default_waba_id=tenant.default_waba_id,
            default_phone_id=default_phone.id if default_phone else None
        )
        
    except Exception as e:
        logger.error(f"Error configuring WABA: {e}")
        return ConfigureMultiTenantOutput(
            success=False,
            message=f"Error configuring WABA: {str(e)}",
            waba_count=0,
            phone_count=0,
            default_waba_id=None,
            default_phone_id=None
        )

async def configure_phone(input_data: ConfigurePhoneInput) -> ConfigureMultiTenantOutput:
    """Configures a WhatsApp phone number."""
    logger.info(f"MCP Tool: Configuring phone {input_data.phone_id} for WABA {input_data.waba_id}")
    
    context = get_current_context()
    if not context:
        logger.error("No context available for current request")
        return ConfigureMultiTenantOutput(
            success=False,
            message="No context available for current request",
            waba_count=0,
            phone_count=0,
            default_waba_id=None,
            default_phone_id=None
        )
    
    try:
        # Get current tenant settings
        tenant_data = context.tenant("tenant_settings")
        if not tenant_data:
            # If not found, initialize with defaults
            from app.zap_mcp_server.tenant_settings import initialize_tenant_settings
            initialize_tenant_settings(context)
            tenant_data = context.tenant("tenant_settings")
            if not tenant_data:
                return ConfigureMultiTenantOutput(
                    success=False,
                    message="Failed to initialize tenant settings",
                    waba_count=0,
                    phone_count=0,
                    default_waba_id=None,
                    default_phone_id=None
                )
        
        # Convert to tenant model
        from app.zap_mcp_server.tenant_settings import TenantSettings, PhoneNumberSettings
        tenant = TenantSettings(**tenant_data)
        
        # Check if WABA exists
        waba_exists = any(waba.id == input_data.waba_id for waba in tenant.wabas)
        if not waba_exists:
            return ConfigureMultiTenantOutput(
                success=False,
                message=f"WABA not found: {input_data.waba_id}",
                waba_count=len(tenant.wabas),
                phone_count=sum(len(waba.phone_numbers) for waba in tenant.wabas),
                default_waba_id=tenant.default_waba_id,
                default_phone_id=None
            )
        
        # Format the display number if not provided
        display_number = input_data.display_number
        if not display_number:
            display_number = f"+{input_data.phone_id}" if not input_data.phone_id.startswith("+") else input_data.phone_id
        
        # Check if phone already exists in any WABA
        existing_phone = tenant.get_phone(input_data.phone_id)
        
        if existing_phone:
            # Update existing phone
            existing_phone.display_number = display_number
            if input_data.display_name:
                existing_phone.display_name = input_data.display_name
            
            # Handle WABA reassignment if needed
            if existing_phone.waba_id != input_data.waba_id:
                # Remove from old WABA
                for waba in tenant.wabas:
                    if waba.id == existing_phone.waba_id:
                        waba.phone_numbers = [p for p in waba.phone_numbers if p.id != input_data.phone_id]
                        break
                
                # Add to new WABA
                existing_phone.waba_id = input_data.waba_id
                for waba in tenant.wabas:
                    if waba.id == input_data.waba_id:
                        waba.phone_numbers.append(existing_phone)
                        break
                
                # Rebuild mappings
                tenant._build_mappings()
            
            if input_data.make_default:
                # Set as default for its WABA
                for waba in tenant.wabas:
                    if waba.id == input_data.waba_id:
                        for phone in waba.phone_numbers:
                            phone.is_default = (phone.id == input_data.phone_id)
            
            logger.info(f"Updated existing phone: {input_data.phone_id}")
            message = f"Updated existing phone: {input_data.phone_id}"
        else:
            # Create new phone
            new_phone = PhoneNumberSettings(
                id=input_data.phone_id,
                display_number=display_number,
                waba_id=input_data.waba_id,
                display_name=input_data.display_name,
                is_default=input_data.make_default
            )
            
            # Add to WABA
            for waba in tenant.wabas:
                if waba.id == input_data.waba_id:
                    if input_data.make_default:
                        # Set as default for this WABA
                        for phone in waba.phone_numbers:
                            phone.is_default = False
                        new_phone.is_default = True
                    
                    waba.phone_numbers.append(new_phone)
                    break
            
            # Rebuild mappings
            tenant._build_mappings()
            
            logger.info(f"Added new phone: {input_data.phone_id}")
            message = f"Added new phone: {input_data.phone_id}"
        
        # Update tenant settings in context
        context.set_tenant("tenant_settings", tenant.model_dump())
        
        # Update convenience fields
        default_waba = tenant.get_default_waba()
        default_phone = tenant.get_default_phone()
        
        if default_waba:
            context.set_tenant("default_waba_id", default_waba.id)
        
        if default_phone:
            context.set_tenant("default_phone_id", default_phone.id)
            context.set_tenant("default_phone_number", default_phone.display_number)
            
            # Update API URL if needed
            if default_waba and default_phone:
                api_url = f"https://graph.facebook.com/{default_waba.api_version}/{default_phone.id}/messages"
                context.set_tenant("default_api_url", api_url)
        
        # Count phones across all WABAs
        phone_count = sum(len(waba.phone_numbers) for waba in tenant.wabas)
        
        return ConfigureMultiTenantOutput(
            success=True,
            message=message,
            waba_count=len(tenant.wabas),
            phone_count=phone_count,
            default_waba_id=tenant.default_waba_id,
            default_phone_id=default_phone.id if default_phone else None
        )
        
    except Exception as e:
        logger.error(f"Error configuring phone: {e}")
        return ConfigureMultiTenantOutput(
            success=False,
            message=f"Error configuring phone: {str(e)}",
            waba_count=0,
            phone_count=0,
            default_waba_id=None,
            default_phone_id=None
        )

# --- Resource Definitions --- #

# Define Content Models for Resources
class TextContent(BaseModel):
    type: str = Field(default="text", description="Content type indicator.")
    text: str = Field(..., description="The actual text content.")

async def get_conversation_history(contact_wa_id: str) -> List[TextContent]:
    """Retrieves the conversation history for a given contact WA ID from Redis."""
    logger.info(f"MCP Resource: Received request for history of {contact_wa_id}")
    
    # Get the active session manager
    session_manager = await get_session_manager()
    
    # If there's a current client session in request context, update it
    current_session = getattr(asyncio.current_task(), "mcp_session", None)
    if current_session:
        current_session.set_active_contact(contact_wa_id)
        current_session.subscribe_to_resource(f"whatsapp://conversations/{contact_wa_id}")
        await session_manager.update_session(current_session)
    
    r = await get_redis_client()
    history_key = f"history:{contact_wa_id}"
    try:
        # Retrieve messages, ordered by timestamp (score)
        history_json_list = await r.zrange(history_key, 0, -1)

        contents = []
        for msg_json in history_json_list:
            try:
                msg_data = json.loads(msg_json)
                role = msg_data.get('role', 'unknown').upper()
                content_text = msg_data.get('content', '')
                timestamp_str = msg_data.get('timestamp', '[no timestamp]')
                # Format for display
                formatted_text = f"[{timestamp_str}] {role}: {content_text}"
                contents.append(TextContent(text=formatted_text))
            except json.JSONDecodeError:
                logger.warning(f"Could not decode message JSON from history for {contact_wa_id}: {msg_json}")
            except Exception as e:
                 logger.warning(f"Error processing message from history for {contact_wa_id}: {e}")

        logger.debug(f"Retrieved {len(contents)} messages for history of {contact_wa_id}")
        return contents
    except Exception as e:
        logger.error(f"Error retrieving history from Redis for {contact_wa_id}: {e}")
        return [] # Return empty list on error

async def get_session_context(scope: Optional[str] = None) -> List[TextContent]:
    """Gets the current session context as a resource.
    
    Args:
        scope: Optional scope to filter by. If not provided, all scopes are included.
    """
    logger.info(f"MCP Resource: Retrieving session context{f' for scope {scope}' if scope else ''}")
    
    context = get_current_context()
    if not context:
        return [TextContent(text="No context available for the current session.")]
    
    try:
        if scope:
            # Return just the requested scope
            if not context.has(scope, ""):  # Check if scope exists using empty key
                return [TextContent(text=f"Scope '{scope}' does not exist or is empty.")]
            
            keys = context.list_keys(scope)
            items = []
            for key in keys:
                value = context.get(scope, key)
                items.append(f"- {key}: {json.dumps(value)}")
            
            text = f"Context for scope '{scope}':\n" + "\n".join(items)
            return [TextContent(text=text)]
        else:
            # Return all scopes
            snapshot = context.create_snapshot()
            formatted_items = []
            
            for scope_name, values in snapshot.items():
                if not values:  # Skip empty scopes
                    continue
                
                scope_items = [f"- {key}: {json.dumps(value)}" for key, value in values.items()]
                if scope_items:
                    formatted_scope = f"## {scope_name}\n" + "\n".join(scope_items)
                    formatted_items.append(formatted_scope)
            
            if not formatted_items:
                return [TextContent(text="No context data available.")]
                
            text = "# Session Context\n\n" + "\n\n".join(formatted_items)
            return [TextContent(text=text)]
            
    except Exception as e:
        logger.error(f"Error retrieving context as resource: {e}")
        return [TextContent(text=f"Error retrieving context: {str(e)}")]

# --- MCP Server Initialization --- #

async def initialize_mcp_server():
    """Initializes the global FastMCP server instance and registers tools/resources."""
    global mcp_server
    if mcp_server is None:
        mcp_server = FastMCP(settings.MCP_SERVER_ID)
        
        # Initialize session manager
        session_manager = await get_session_manager()
        logger.info("Session manager initialized")

        # Register Tools
        try:
            mcp_server.tool("send_message")(send_whatsapp_message)
            logger.info("Registered MCP tool: send_message")
            
            # Register context management tools
            mcp_server.tool("context_set")(set_context_value)
            mcp_server.tool("context_get")(get_context_value)
            mcp_server.tool("context_clear")(clear_context_scope)
            mcp_server.tool("context_scopes")(get_context_scopes)
            mcp_server.tool("context_snapshot")(get_context_snapshot)
            logger.info("Registered MCP context management tools")
            
            # Register tenant management tools
            mcp_server.tool("tenant_configure")(configure_tenant_settings)
            mcp_server.tool("waba_configure")(configure_waba)
            mcp_server.tool("phone_configure")(configure_phone)
            logger.info("Registered MCP tenant configuration tools")
            
            # Register other tools here...
        except Exception as e:
             logger.error(f"Failed to register MCP tools: {e}")

        # Register Resources
        try:
            # URI pattern allows extracting contact_wa_id
            mcp_server.resource("whatsapp://conversations/{contact_wa_id}")(get_conversation_history)
            logger.info("Registered MCP resource: whatsapp://conversations/{contact_wa_id}")
            
            # Register context resources
            mcp_server.resource("mcp://context")(get_session_context)
            mcp_server.resource("mcp://context/{scope}")(get_session_context)
            logger.info("Registered MCP context resources")
            
            # Register other resources here...
        except Exception as e:
            logger.error(f"Failed to register MCP resources: {e}")
            
        # Register Completion Handlers
        try:
            register_completion_handlers(mcp_server)
            logger.info("Registered MCP completion handlers")
        except Exception as e:
            logger.error(f"Failed to register MCP completion handlers: {e}")

        logger.info(f"MCP Server ({settings.MCP_SERVER_ID}) initialized.")
    else:
        logger.warning("MCP Server already initialized.")

# --- Getter for the Instance --- #

def get_mcp_server() -> FastMCP:
    """Returns the initialized global MCP server instance."""
    if mcp_server is None:
        logger.error("MCP server accessed before initialization!")
        raise RuntimeError("MCP server has not been initialized. Check application lifespan.")
    return mcp_server

# --- MCP Session Handling --- #

async def handle_client_connect(client_info: Dict[str, Any], client_session_id: Optional[str] = None) -> str:
    """Handle a new client connection and create a session.
    
    Args:
        client_info: Information about the client
        client_session_id: Optional session ID provided by the client for reconnection
        
    Returns:
        The session ID (either client-provided or server-generated)
    """
    session_manager = await get_session_manager()
    
    # If client provided a session ID, try to load it first
    if client_session_id:
        existing_session = await session_manager.load_session(client_session_id)
        if existing_session:
            logger.info(f"Client reconnected with existing session: {client_session_id}")
            # Update client info in case it changed
            existing_session.client_info.update(client_info)
            existing_session.touch()  # Update last active time
            await session_manager.update_session(existing_session)
            return client_session_id
        else:
            logger.info(f"Client provided session ID {client_session_id} not found, creating new session")
    
    # Create a new session (either with client's ID or a generated one)
    session_id = client_session_id if client_session_id else str(uuid.uuid4())
    session = await session_manager.create_session(session_id, client_info)
    return session_id

async def handle_client_disconnect(session_id: str):
    """Handle a client disconnection and close the session."""
    session_manager = await get_session_manager()
    await session_manager.close_session(session_id)

async def get_session_for_request(session_id: str) -> Optional[Dict[str, Any]]:
    """Get the session for a request and attach it to the current task."""
    session_manager = await get_session_manager()
    session = session_manager.get_session(session_id)
    
    if session:
        # Attach the session to the current task for context
        current_task = asyncio.current_task()
        if current_task:
            setattr(current_task, "mcp_session", session)
        return session.to_dict()
    
    return None

# --- Notify Sessions About WhatsApp Events --- #

async def notify_sessions_about_message(message_data: Dict[str, Any]):
    """Notify relevant sessions about a new WhatsApp message."""
    contact_id = message_data.get("from", "")
    if not contact_id:
        return
        
    session_manager = await get_session_manager()
    
    # Find sessions that are interacting with this contact
    sessions = await session_manager.get_sessions_by_contact(contact_id)
    
    # Also find sessions subscribed to this contact's conversation
    resource_uri = f"whatsapp://conversations/{contact_id}"
    subscribed_sessions = await session_manager.get_sessions_subscribed_to_resource(resource_uri)
    
    # Combine and deduplicate
    all_sessions = {s.session_id: s for s in sessions + subscribed_sessions}
    
    # Broadcast the message notification
    notification = {
        "type": "new_message",
        "data": message_data,
        "timestamp": datetime.now().isoformat()
    }
    
    for session in all_sessions.values():
        session.add_message(notification)
        await session_manager.update_session(session)
    
    logger.info(f"Notified {len(all_sessions)} sessions about message from {contact_id}")
