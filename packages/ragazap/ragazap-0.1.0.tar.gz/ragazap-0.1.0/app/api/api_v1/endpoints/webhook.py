from fastapi import APIRouter, Request, Response, HTTPException, BackgroundTasks, Header, Query
from fastapi.responses import PlainTextResponse
from loguru import logger

from app.core.config import settings
from app.core.security import verify_meta_signature
from app.services.webhook_processor import process_incoming_message
from app.models.whatsapp import WhatsappWebhookRequest #, WhatsappWebhookRequestAdapter # If using adapter

router = APIRouter()

@router.get("/webhook", tags=["webhook"])
async def verify_webhook_endpoint(
    mode: str = Query(..., alias="hub.mode"),
    challenge: str = Query(..., alias="hub.challenge"),
    token: str = Query(..., alias="hub.verify_token"),
):
    """Handles webhook verification challenge from Meta."""
    logger.info(f"GET /webhook verification request: mode={mode}, token={token}")
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        logger.info(f"Webhook verification successful. Responding with challenge: {challenge}")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        logger.error("Webhook verification failed.")
        raise HTTPException(status_code=403, detail="Webhook verification failed")

@router.post("/webhook", tags=["webhook"])
async def handle_webhook_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str | None = Header(None, alias="X-Hub-Signature-256") # Correct alias
):
    """Handles incoming WhatsApp notifications (messages, status updates)."""
    logger.info("POST /webhook received...")
    body_bytes = await request.body()

    # Verify signature (if secret is configured)
    if not verify_meta_signature(body_bytes, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")
    if settings.META_APP_SECRET: # Log verification only if secret is present
        logger.info("Webhook signature verified.")

    try:
        # Parse the entire webhook request payload
        # Use model_validate_json for Pydantic v2
        webhook_data = WhatsappWebhookRequest.model_validate_json(body_bytes)
        logger.info(f"Webhook payload parsed. Object: {webhook_data.object}")

    except Exception as e:
        logger.error(f"Webhook: Error parsing payload: {e}", exc_info=True)
        # Acknowledge receipt even on parse error, per Meta recommendations
        return Response(status_code=200)

    # Process changes in the background
    if webhook_data.entry:
        for entry in webhook_data.entry:
            if entry.changes:
                for change in entry.changes:
                    # Field check remains relevant
                    if change.field == "messages":
                        value_dict = change.value.model_dump() # Get the value dict
                        # Ensure messages or statuses are present before scheduling
                        if value_dict.get("messages") or value_dict.get("statuses"):
                            # Pass the raw value dictionary to the background task
                            background_tasks.add_task(process_incoming_message, value_dict)
                            logger.debug(f"Scheduled processing for change value: {value_dict}")
                        elif value_dict.get("errors"):
                            # Handle errors directly if needed, or log
                            logger.error(f"Received webhook error notification: {value_dict.get('errors')}")
                        else:
                            logger.warning(f"Received 'messages' change field with no messages, statuses, or errors: {value_dict}")
                    else:
                        logger.info(f"Webhook: Ignoring change field '{change.field}'")
            else:
                 logger.debug(f"Webhook: Entry {entry.id} had no changes.") # Use debug level
    else:
        logger.warning("Webhook: Parsed data did not contain 'entry' list.")

    # Always return 200 OK quickly to Meta
    return Response(status_code=200) 