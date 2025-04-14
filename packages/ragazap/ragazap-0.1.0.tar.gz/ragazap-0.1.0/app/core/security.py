import hmac
import hashlib
import sys
from loguru import logger
from app.core.config import settings # Import settings

def verify_meta_signature(request_body: bytes, x_hub_signature_256: str | None):
    """Verify the incoming webhook signature from Meta."""
    if not settings.META_APP_SECRET:
        logger.warning("META_APP_SECRET not set. Skipping signature verification.")
        return True # Allow if secret not set
    if not x_hub_signature_256:
        logger.error("X-Hub-Signature-256 header missing.")
        return False
    if not x_hub_signature_256.startswith("sha256="):
         logger.error("Invalid signature format.")
         return False

    try:
        expected_signature = x_hub_signature_256.split("=", 1)[1]
        hashed_payload = hmac.new(
            settings.META_APP_SECRET.encode('utf-8'),
            request_body,
            hashlib.sha256
        ).hexdigest()

        is_valid = hmac.compare_digest(hashed_payload, expected_signature)
        if not is_valid:
             logger.error(f"Invalid webhook signature. Expected {expected_signature}, got {hashed_payload}")
        return is_valid
    except IndexError:
        logger.error("Malformed X-Hub-Signature-256 header.")
        return False
    except Exception as e:
         logger.error(f"Error during signature verification: {e}")
         return False 