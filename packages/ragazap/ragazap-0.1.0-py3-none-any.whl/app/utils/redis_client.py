import asyncio
import sys
from typing import Dict, Any
import redis.asyncio as redis
from loguru import logger
from datetime import timedelta
import json
import httpx

from app.core.config import settings # Import settings for Redis URL and history length
from app.utils.http_client import get_http_client # For marking messages read

# Global Redis client instance
redis_client: redis.Redis | None = None

async def initialize_redis_client():
    """Initializes the global Redis client."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await redis_client.ping() # Verify connection
            print(f"Redis Client initialized and connected to {settings.REDIS_URL}.")
            logger.info(f"Redis Client initialized and connected to {settings.REDIS_URL}.")
        except Exception as e:
            print(f"Error initializing Redis client: {e}", file=sys.stderr)
            logger.error(f"Error initializing Redis client: {e}")
            redis_client = None # Ensure it's None if connection failed

async def close_redis_client():
    """Closes the global Redis client connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        print("Redis Client closed.")
        logger.info("Redis Client closed.")

async def get_redis_client() -> redis.Redis:
    """Returns the initialized global Redis client."""
    if redis_client is None:
        logger.warning("Redis client accessed before initialization or connection failed.")
        # Optionally, try to initialize again or raise an error
        await initialize_redis_client()
        if redis_client is None: # Still None after retry
            raise ConnectionError("Redis client is not available.")
    return redis_client

async def add_message_turn_to_history(contact_wa_id: str, turn_data: Dict[str, Any]):
    """Adds a message turn to the contact's history in Redis (as a sorted set)."""
    r = await get_redis_client()
    history_key = f"history:{contact_wa_id}"
    timestamp_score = int(turn_data["timestamp"].timestamp()) # Use Unix timestamp as score
    message_json = json.dumps(turn_data) # Serialize the turn data

    try:
        # Add the new message
        await r.zadd(history_key, {message_json: timestamp_score})
        # Trim the history to keep only the last N messages
        await r.zremrangebyrank(history_key, 0, -settings.MAX_CONVERSATION_HISTORY_LENGTH - 1)
        # Optionally set an expiration for the history key (e.g., 7 days)
        await r.expire(history_key, timedelta(days=settings.CONVERSATION_EXPIRATION_DAYS))
        logger.debug(f"Added message WAMID {turn_data.get('wamid')} to history for {contact_wa_id}. History size maintained at <= {settings.MAX_CONVERSATION_HISTORY_LENGTH}.")
    except Exception as e:
        logger.error(f"Error adding message turn to Redis for {contact_wa_id}: {e}")

async def mark_whatsapp_message_read(wamid: str):
    """Sends a request to the WhatsApp Cloud API to mark a message as read."""
    http_client = await get_http_client()
    api_url = f"https://graph.facebook.com/{settings.META_API_VERSION}/{settings.BUSINESS_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": wamid,
    }
    try:
        response = await http_client.post(api_url, headers=headers, json=payload)
        response.raise_for_status() # Raise exception for bad status codes
        logger.info(f"Successfully marked message WAMID {wamid} as read.")
        # TODO: Optionally update the message status in Redis history if needed
    except httpx.HTTPStatusError as e:
        logger.error(f"Error marking message WAMID {wamid} as read. Status: {e.response.status_code}, Response: {e.response.text}")
    except Exception as e:
        logger.error(f"Failed to mark message WAMID {wamid} as read: {e}") 