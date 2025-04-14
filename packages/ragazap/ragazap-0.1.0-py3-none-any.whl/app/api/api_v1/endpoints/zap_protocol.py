import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from pydantic import BaseModel, ValidationError
import inspect # For tool call argument inspection

from app.zap_mcp_server.protocol import send_json_rpc_response, send_json_rpc_notification
from app.core.config import settings
from app.zap_mcp_server.instance import get_mcp_server, handle_client_connect, handle_client_disconnect, get_session_for_request

router = APIRouter()

@router.websocket("/mcp")
async def handle_mcp_websocket(websocket: WebSocket):
    """Handles MCP communication over WebSocket."""
    await websocket.accept()
    logger.info("MCP Client Connected via WebSocket.")
    
    client_initialized = False
    session_id = None
    mcp_server = get_mcp_server() # Get the initialized instance

    try:
        # Create a new client session
        client_info = {
            "remote_addr": str(websocket.client.host) if websocket.client else "unknown",
            "transport": "websocket",
            "user_agent": websocket.headers.get("user-agent", "Unknown")
        }
        session_id = await handle_client_connect(client_info)
        logger.info(f"Created MCP session: {session_id}")
        
        while True:
            raw_data = await websocket.receive_text()
            message = None
            message_id = None # Keep track of ID
            try:
                message = json.loads(raw_data)
                message_id = message.get("id")
                
                # Get and attach the session for this request
                if session_id:
                    await get_session_for_request(session_id)
                    
            except json.JSONDecodeError:
                await send_json_rpc_response(websocket, None, error={"code": -32700, "message": "Parse error"})
                continue

            method = message.get("method")
            params = message.get("params", {})

            if not method:
                if message_id is not None:
                    await send_json_rpc_response(websocket, message_id, error={"code": -32600, "message": "Invalid Request: Missing method"})
                continue # Ignore notification with no method

            logger.debug(f"MCP WS Received: Method={method}, ID={message_id}, Session={session_id}")

            # --- Handle MCP Methods --- #
            if method == "initialize":
                if message_id is None: continue # Must be a request
                
                client_protocol_version = params.get('protocolVersion')
                if not client_protocol_version:
                    await send_json_rpc_response(websocket, message_id, error={"code": -32602, "message": "Invalid params: Missing protocol version"})
                    continue
                
                if client_protocol_version != settings.MCP_PROTOCOL_VERSION:
                    logger.warning(f"Client requested protocol version {client_protocol_version}, server uses {settings.MCP_PROTOCOL_VERSION}.")
                
                client_capabilities = params.get('capabilities', {})
                logger.debug(f"Client capabilities: {client_capabilities}")
                
                # Check for a client-provided session ID during initialization
                if session_id is None:  # Only handle if we don't already have a session
                    client_session_id = params.get('sessionId')
                    if client_session_id:
                        logger.info(f"Client requested specific session ID: {client_session_id}")
                        # Close the auto-created session
                        if session_id:
                            await handle_client_disconnect(session_id)
                        
                        # Create/load the client-requested session
                        session_id = await handle_client_connect(client_info, client_session_id)
                        logger.info(f"Using client-provided session: {session_id}")
                
                response = {
                    "protocolVersion": settings.MCP_PROTOCOL_VERSION,
                    "serverInfo": {"name": settings.MCP_SERVER_ID, "version": "1.0.0"}, # Add version
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"subscribe": True, "listChanged": True},
                        "completion": True
                    },
                    "sessionId": session_id,  # Return the active session ID in the response
                    "instructions": "WhatsApp integration server. Use tools/list and resources/list for details."
                }
                await send_json_rpc_response(websocket, message_id, result=response)
                logger.info(f"MCP WS: Responded to initialize request ID {message_id}, Session={session_id}.")

            elif method == "notifications/initialized":
                client_initialized = True
                logger.info(f"MCP WS: Client initialized confirmation received. Session={session_id}")
                # No response needed

            elif not client_initialized and method not in ["initialize", "notifications/initialized"]:
                 if message_id is not None:
                      await send_json_rpc_response(websocket, message_id, error={"code": -32002, "message": "Server not initialized"})
                 continue

            elif method == "tools/list":
                if message_id is None: continue
                tools_list = []
                for name, tool_func in getattr(mcp_server, '_tools', {}).items():
                    desc = getattr(tool_func, '__doc__', 'No description available.')
                    inputs_schema = {}
                    outputs_schema = {}
                    param_hints = getattr(tool_func, '__annotations__', {})

                    param_name = next((k for k, v in param_hints.items() if k != 'return'), None)
                    if param_name and isinstance(param_hints.get(param_name), type) and issubclass(param_hints[param_name], BaseModel):
                        try: inputs_schema = param_hints[param_name].model_json_schema() 
                        except Exception as e: logger.error(f"Error getting input schema for tool {name}: {e}")
                    
                    if 'return' in param_hints and isinstance(param_hints['return'], type) and issubclass(param_hints['return'], BaseModel):
                        try: outputs_schema = param_hints['return'].model_json_schema()
                        except Exception as e: logger.error(f"Error getting output schema for tool {name}: {e}")
                        
                    tools_list.append({"name": name, "description": desc, "inputs": inputs_schema, "outputs": outputs_schema})
                
                await send_json_rpc_response(websocket, message_id, result={"tools": tools_list})

            elif method == "resources/list":
                if message_id is None: continue
                resources_list = []
                for uri, resource_func in getattr(mcp_server, '_resources', {}).items():
                    desc = getattr(resource_func, '__doc__', 'No description available.')
                    content_types = ["application/json"] # Assume JSON list output for now
                    resources_list.append({"uri": uri, "description": desc, "contentTypes": content_types})
                
                result = {"resources": resources_list}
                cursor = params.get('cursor') # Handle pagination cursor if needed
                if cursor: logger.debug(f"Cursor provided: {cursor}, but pagination not implemented.")
                
                await send_json_rpc_response(websocket, message_id, result=result)

            elif method == "tools/call":
                if message_id is None: continue
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if not tool_name:
                    await send_json_rpc_response(websocket, message_id, error={"code": -32602, "message": "Invalid params: Missing tool name"})
                    continue

                tool_func = getattr(mcp_server, '_tools', {}).get(tool_name)
                if not tool_func:
                    await send_json_rpc_response(websocket, message_id, error={"code": -32601, "message": f"Method not found: Tool '{tool_name}'"})
                    continue

                try:
                    validated_params = arguments
                    pydantic_model_class = None
                    param_hints = getattr(tool_func, '__annotations__', {})
                    param_name = next(iter(param_hints), None)
                    if param_name and param_name != 'return':
                         param_type = param_hints.get(param_name)
                         if isinstance(param_type, type) and issubclass(param_type, BaseModel):
                              pydantic_model_class = param_type

                    if pydantic_model_class:
                        try:
                            if not isinstance(arguments, dict):
                                # Simplify: Raise ValueError directly
                                raise ValueError("Arguments for Pydantic model must be a JSON object")
                            validated_params = pydantic_model_class.model_validate(arguments)
                            result = await tool_func(validated_params)
                        except ValidationError as e:
                                await send_json_rpc_response(websocket, message_id, error={"code": -32602, "message": f"Invalid params for tool '{tool_name}': {e}"})
                                continue
                    else:
                         # Inspect signature and call
                         sig = inspect.signature(tool_func)
                         try:
                              # Bind arguments carefully
                              bound_args = sig.bind(**arguments) # Assumes keywords match
                              result = await tool_func(*bound_args.args, **bound_args.kwargs)
                         except TypeError as te:
                             logger.warning(f"Could not call tool '{tool_name}' with arguments: {te}")
                             await send_json_rpc_response(websocket, message_id, error={"code": -32602, "message": f"Invalid params for tool '{tool_name}': Could not map arguments to function signature. {te}"})
                             continue

                    # Convert Pydantic result to dict if necessary
                    result_dict = result.model_dump() if isinstance(result, BaseModel) else result
                    await send_json_rpc_response(websocket, message_id, result=result_dict)

                except Exception as e:
                    logger.error(f"Error executing tool '{tool_name}': {e}", exc_info=True)
                    await send_json_rpc_response(websocket, message_id, error={"code": -32000, "message": f"Tool execution error: {e}"})

            elif method == "resources/read":
                if message_id is None: continue
                resource_uri = params.get("uri")
                if not resource_uri:
                     await send_json_rpc_response(websocket, message_id, error={"code": -32602, "message": "Invalid params: Missing resource uri"})
                     continue

                resource_func = None
                resource_params = {}
                matched = False
                for template_uri, func in getattr(mcp_server, '_resources', {}).items():
                    # Simple template matching logic (from original main.py)
                    if '{' in template_uri and '}' in template_uri:
                        try:
                            prefix, rest_part = template_uri.split('{', 1)
                            param_name, suffix = rest_part.split('}', 1)
                            if resource_uri.startswith(prefix) and resource_uri.endswith(suffix) and len(resource_uri) > len(prefix) + len(suffix):
                                param_value = resource_uri[len(prefix):-len(suffix)]
                                resource_params[param_name] = param_value
                                resource_func = func
                                matched = True
                                break
                        except (ValueError, IndexError):
                             logger.warning(f"Skipping malformed resource template URI: {template_uri}")
                             continue
                    elif template_uri == resource_uri: # Exact match
                        resource_func = func
                        matched = True
                        break

                if not matched or not resource_func:
                    await send_json_rpc_response(websocket, message_id, error={"code": -32601, "message": f"Method not found: Resource '{resource_uri}'"})
                    continue

                try:
                    result = await resource_func(**resource_params)
                    
                    # Ensure result is a list of Pydantic models or dicts matching MCP spec (e.g., TextContent)
                    if not isinstance(result, list):
                        logger.warning(f"Resource '{resource_uri}' returned non-list. Wrapping.")
                        result = [result] if result is not None else []
                    
                    contents = []
                    for item in result:
                        if isinstance(item, BaseModel):
                             # Assume it conforms to TextContent or similar schema expected by caller
                            item_dict = item.model_dump(mode='json')
                            if 'type' not in item_dict: item_dict['type'] = 'text' # Ensure type field
                            contents.append(item_dict)
                        elif isinstance(item, dict):
                            if 'type' not in item: item['type'] = 'text' # Ensure type field
                            contents.append(item)
                        else:
                            logger.warning(f"Resource '{resource_uri}' item not a Model or dict. Converting to TextContent.")
                            contents.append({"type": "text", "text": str(item)}) 
                            
                    await send_json_rpc_response(websocket, message_id, result={"contents": contents})
                except Exception as e:
                    logger.error(f"Error reading resource '{resource_uri}': {e}", exc_info=True)
                    await send_json_rpc_response(websocket, message_id, error={"code": -32000, "message": f"Resource read error: {e}"})

            else:
                # Handle other standard MCP methods or unknown methods
                if message_id is not None:
                     await send_json_rpc_response(websocket, message_id, error={"code": -32601, "message": f"Method not found: {method}"})

    except WebSocketDisconnect:
        logger.info(f"MCP Client Disconnected from WebSocket. Session={session_id}")
        if session_id:
            await handle_client_disconnect(session_id)
    except Exception as e:
        logger.error(f"MCP WebSocket Error: {e}, Session={session_id}", exc_info=True)
        # Attempt to close gracefully
        try: 
            await websocket.close(code=1011)
            if session_id:
                await handle_client_disconnect(session_id)
        except RuntimeError: pass # Ignore if already closed 