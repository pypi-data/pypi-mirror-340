import json
import sys
from typing import Any, Dict, Optional, Union
from fastapi import WebSocket
from loguru import logger

async def send_json_rpc_response(
    websocket: WebSocket, 
    id: Union[str, int, None], 
    result: Optional[Any] = None, 
    error: Optional[Dict] = None
):
    """Helper to send JSON-RPC responses."""
    response = {"jsonrpc": "2.0", "id": id}
    if error:
        response["error"] = error
    else:
        response["result"] = result if result is not None else {} # Result must be present if error is not
    try:
        await websocket.send_text(json.dumps(response))
    except Exception as e:
        logger.error(f"Error sending JSON-RPC response for ID {id}: {e}")

async def send_json_rpc_notification(
    websocket: WebSocket, 
    method: str, 
    params: Optional[Any] = None
):
    """Helper to send JSON-RPC notifications."""
    notification = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        notification["params"] = params
    try:
        await websocket.send_text(json.dumps(notification))
    except Exception as e:
        logger.error(f"Error sending JSON-RPC notification {method}: {e}")