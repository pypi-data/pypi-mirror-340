from fastapi import APIRouter

from app.api.api_v1.endpoints import webhook, zap_protocol

api_router = APIRouter()

# Include webhook router
api_router.include_router(webhook.router, prefix="", tags=["webhook"])

# Include ZAP Protocol WebSocket router
# Note: Including WebSockets in a sub-router needs careful handling depending on FastAPI version.
# For simplicity here, we assume it works directly.
# Alternatively, the WebSocket endpoint could be defined directly in app/main.py.
api_router.include_router(zap_protocol.router, prefix="", tags=["zap_protocol"]) 