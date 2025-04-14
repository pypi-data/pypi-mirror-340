import os
import sys
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from loguru import logger

# Load .env file first
load_dotenv()

class Settings(BaseSettings):
    # --- Mode Configuration ---
    STANDALONE_MODE: bool = os.getenv("STANDALONE_MODE", "false").lower() == "true"

    # --- Meta/WhatsApp Configuration ---
    META_API_VERSION: str = os.getenv("META_API_VERSION", "v22.0")
    META_APP_SECRET: str = os.getenv("META_APP_SECRET", "")
    WHATSAPP_API_TOKEN: str = os.getenv("WHATSAPP_API_TOKEN", "")
    WEBHOOK_VERIFY_TOKEN: str = os.getenv("WEBHOOK_VERIFY_TOKEN", "")
    # Specific Business Phone Number ID managed by this server
    BUSINESS_PHONE_NUMBER_ID: str = os.getenv("BUSINESS_PHONE_NUMBER_ID", "") # Added this explicitly

    # --- Webhook Server Configuration ---
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8080"))

    # --- MCP Configuration ---
    MCP_SERVER_ID: str = "whatsapp-server"
    MCP_PROTOCOL_VERSION: str = "2025-03-26"

    # --- Redis Configuration ---
    UPSTASH_REDIS_URL: str = os.getenv("UPSTASH_REDIS_URL", "") # Default Redis URL
    UPSTASH_REDIS_TOKEN: str = os.getenv("UPSTASH_REDIS_TOKEN", "") # Default Redis Token
    MAX_CONVERSATION_HISTORY_LENGTH: int = int(os.getenv("MAX_CONVERSATION_HISTORY_LENGTH", "100")) # Max turns per conversation
    CONVERSATION_EXPIRATION_DAYS: int = int(os.getenv("CONVERSATION_EXPIRATION_DAYS", "7")) # How long history persists

    # --- Internal Settings ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    def validate_standalone_mode(self) -> None:
        """Validate configuration based on the selected mode."""
        if self.STANDALONE_MODE:
            # In standalone mode, we require all WhatsApp credentials
            if not all([self.WHATSAPP_API_TOKEN, self.BUSINESS_PHONE_NUMBER_ID, self.WEBHOOK_VERIFY_TOKEN]):
                logger.warning("Standalone mode requires WHATSAPP_API_TOKEN, BUSINESS_PHONE_NUMBER_ID, and WEBHOOK_VERIFY_TOKEN")
                logger.warning("These will be required when making API calls")
            
            # Redis is optional in standalone mode
            if not all([self.UPSTASH_REDIS_URL, self.UPSTASH_REDIS_TOKEN]):
                logger.warning("Redis configuration is optional in standalone mode")
                logger.warning("Conversation history will not be persisted")
        else:
            # In client mode, we don't require WhatsApp credentials upfront
            # They will be provided by the client through the MCP protocol
            if any([self.WHATSAPP_API_TOKEN, self.BUSINESS_PHONE_NUMBER_ID]):
                logger.warning("WhatsApp credentials are not required in client mode")
                logger.warning("These will be provided by the client through MCP")

settings = Settings()
settings.validate_standalone_mode()

# --- Post-Load Checks/Warnings --- # Can be moved to app startup if preferred
if not settings.WHATSAPP_API_TOKEN:
    logger.warning("WHATSAPP_API_TOKEN environment variable not set. API calls will fail.")
if not settings.BUSINESS_PHONE_NUMBER_ID:
    logger.warning("BUSINESS_PHONE_NUMBER_ID environment variable not set. Cannot mark messages read or send messages correctly.")
if not settings.WEBHOOK_VERIFY_TOKEN:
    logger.warning("WEBHOOK_VERIFY_TOKEN not set. Webhook verification endpoint will fail.")
if not settings.META_APP_SECRET:
    logger.warning("META_APP_SECRET not set. Webhook signature verification will be skipped.") 