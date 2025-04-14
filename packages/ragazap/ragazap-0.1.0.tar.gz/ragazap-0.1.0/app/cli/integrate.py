import argparse
import os
import sys
from loguru import logger
import importlib.util
import inspect
import textwrap
import json

def validate_fastapi_app(app_path):
    """Validates that the specified path contains a FastAPI app."""
    try:
        # Split the path into module path and attribute
        module_path, app_var = app_path.rsplit(":", 1) if ":" in app_path else (app_path, "app")
        
        # Convert dotted path to file path if needed
        if not module_path.endswith(".py"):
            file_path = module_path.replace(".", "/") + ".py"
        else:
            file_path = module_path
            module_path = module_path[:-3].replace("/", ".")
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
            
        # Load the module
        spec = importlib.util.spec_from_file_location(module_path, file_path)
        if spec is None or spec.loader is None:
            logger.error(f"Could not load module spec from {file_path}")
            return False
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the FastAPI app instance
        app = getattr(module, app_var, None)
        
        # Verify it's a FastAPI instance
        if not app or not str(type(app).__module__).startswith("fastapi"):
            logger.error(f"Object {app_var} in {module_path} is not a FastAPI instance")
            return False
            
        return app
    except Exception as e:
        logger.error(f"Error validating FastAPI app: {e}")
        return False

def generate_integration_code(app_path, base_url):
    """Generates code to integrate the WhatsApp MCP server with an existing FastAPI app."""
    base_url = base_url.rstrip("/")
    
    integration_code = textwrap.dedent(f"""
    # --- WhatsApp MCP Server Integration ---
    from whatsapp_mcp_server.app.api.api_v1.api import api_router as whatsapp_router
    from whatsapp_mcp_server.app.zap_mcp_server.instance import initialize_mcp_server
    
    # Initialize MCP server on startup
    @app.on_event("startup")
    async def initialize_whatsapp_mcp():
        await initialize_mcp_server()
        logger.info("WhatsApp MCP Server initialized")
    
    # Mount the WhatsApp webhook endpoint
    app.include_router(whatsapp_router, prefix="{base_url}")
    logger.info(f"WhatsApp webhook available at: {base_url}/webhook")
    # --- End WhatsApp MCP Server Integration ---
    """)
    
    return integration_code

def create_integration_file(app_path, base_url="api/whatsapp", output=None):
    """Creates an integration file that can be imported into the main app."""
    try:
        app = validate_fastapi_app(app_path)
        if not app:
            return False
            
        code = generate_integration_code(app_path, base_url)
        
        # Determine output file name
        if output:
            output_file = output
        else:
            output_file = "whatsapp_integration.py"
            
        # Write the integration file
        with open(output_file, "w") as f:
            f.write(code)
            
        logger.info(f"Integration file created: {output_file}")
        logger.info(f"Add 'import {output_file[:-3]}' to your FastAPI app to complete integration")
        
        return True
    except Exception as e:
        logger.error(f"Error creating integration file: {e}")
        return False

def setup_stdio_mode():
    """Configures the MCP server to use STDIO with full MCP specification compliance."""
    import sys
    import os
    from loguru import logger
    
    try:
        # Create a fully compliant STDIO server implementation
        server_script = """
import asyncio
import os
import uuid
from loguru import logger
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

from mcp.server.stdio import stdio_server
from mcp.server.lowlevel import NotificationOptions, ServerCapabilities
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, ResourceMetadata, ToolArgument, PromptArgument
from mcp import types

from app.zap_mcp_server.instance import get_mcp_server, initialize_mcp_server, handle_client_connect, handle_client_disconnect, get_session_for_request
from app.core.config import settings

# Configure logging
logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)
logger.add(f"whatsapp_mcp_stdio_{datetime.now().strftime('%Y%m%d%H%M%S')}.log", level="DEBUG")

async def main():
    # Initialize the MCP server
    logger.info("Initializing WhatsApp MCP Server with full MCP specification support")
    await initialize_mcp_server()
    mcp_server = get_mcp_server()
    
    # Get server capabilities with all features enabled
    capabilities = ServerCapabilities(
        prompts={"listChanged": True},
        resources={"subscribelistChanged": True, "subscribe": True},
        tools={"listChanged": True},
        logging=True,
        completion=True,  # Enable completion support
        notification_options=NotificationOptions(
            message_types=["info", "warning", "error"],
            report_periodic_progress=True
        ),
        experimental_capabilities={}
    )
    
    # Initialize options
    init_options = InitializationOptions(
        server_name="WhatsApp MCP Server",
        server_version=f"{settings.SERVER_VERSION}",
        capabilities=capabilities
    )
    
    # Create a session for this STDIO connection
    client_info = {
        "transport": "stdio",
        "pid": os.getpid(),
        "session_start": datetime.now().isoformat()
    }
    session_id = await handle_client_connect(client_info)
    logger.info(f"Created STDIO session: {session_id}")
    
    # Run the server using STDIO transport with full spec compliance
    logger.info("Starting fully-compliant WhatsApp MCP Server with STDIO transport")
    try:
        async with stdio_server() as (read_stream, write_stream):
            # Custom wrapper for read_stream that attaches session context and handles session ID requests
            async def session_read_stream():
                message = await read_stream()
                
                # Check if this is an initialization request with a session ID
                nonlocal session_id
                try:
                    if isinstance(message, dict) and message.get("method") == "initialize":
                        params = message.get("params", {})
                        client_session_id = params.get("sessionId")
                        if client_session_id:
                            logger.info(f"STDIO client requested session ID: {client_session_id}")
                            # Close current session and create/load the requested one
                            await handle_client_disconnect(session_id)
                            session_id = await handle_client_connect(client_info, client_session_id)
                            # Update the session ID in the response (this will happen in mcp.run)
                            if "id" in message:
                                # We don't need to modify the message because the return
                                # value from initialize will include the session ID
                                pass
                except Exception as e:
                    logger.error(f"Error handling client session ID: {e}")
                
                # Attach the session to the current task
                await get_session_for_request(session_id)
                return message
                
            await mcp_server.run(
                session_read_stream, 
                write_stream,
                initialization_options=init_options
            )
    finally:
        # Clean up session when connection ends
        await handle_client_disconnect(session_id)
        logger.info(f"Closed STDIO session: {session_id}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
"""
        
        # Create a fully compliant client example
        client_script = """
import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(f"whatsapp_mcp_client_{datetime.now().strftime('%Y%m%d%H%M%S')}.log", level="DEBUG")

# Optional callback to handle server notifications
async def handle_notification(notification: types.Notification) -> None:
    if notification.type == "info":
        logger.info(f"Server notification: {notification.message}")
    elif notification.type == "warning":
        logger.warning(f"Server warning: {notification.message}")
    elif notification.type == "error":
        logger.error(f"Server error: {notification.message}")
    elif notification.type == "progress":
        logger.debug(f"Progress: {notification.message} ({notification.percentage}%)")

# Optional callback to handle resource changes
async def handle_resource_change(uri: str, metadata: Optional[types.ResourceMetadata]) -> None:
    if metadata:
        logger.info(f"Resource changed: {uri} (type: {metadata.mime_type})")
    else:
        logger.info(f"Resource removed: {uri}")

# Optional callback to handle tool list changes
async def handle_tool_list_change() -> None:
    logger.info("Tool list changed notification received")

# Optional callback to handle prompt list changes
async def handle_prompt_list_change() -> None:
    logger.info("Prompt list changed notification received")

async def run_whatsapp_client():
    server_params = StdioServerParameters(
        command="python",
        args=["whatsapp_mcp_stdio.py"],
        env=None,  # Use current environment
    )
    
    # Connect to the server
    logger.info("Connecting to WhatsApp MCP server...")
    async with stdio_client(server_params) as (read, write):
        # Create session with all handlers
        async with ClientSession(
            read, 
            write,
            notification_callback=handle_notification,
            resource_change_callback=handle_resource_change,
            tool_list_change_callback=handle_tool_list_change,
            prompt_list_change_callback=handle_prompt_list_change
        ) as session:
            try:
                # Initialize the connection
                logger.info("Initializing session...")
                init_result = await session.initialize()
                logger.info(f"Connected to: {init_result.server_name} v{init_result.server_version}")
                
                # Discover capabilities
                logger.info("Server capabilities:")
                for capability, enabled in init_result.capabilities.items():
                    if enabled and isinstance(enabled, dict):
                        logger.info(f"  {capability}: {json.dumps(enabled)}")
                    elif enabled:
                        logger.info(f"  {capability}: enabled")
                
                # List available tools
                tools = await session.list_tools()
                logger.info(f"Available tools ({len(tools)}):")
                for tool in tools:
                    args = ', '.join([f"{arg.name}" + (" (required)" if arg.required else "") for arg in tool.arguments])
                    logger.info(f"  {tool.name}: {tool.description} - Args: [{args}]")
                
                # List available resources
                resources = await session.list_resources()
                logger.info(f"Available resources ({len(resources)}):")
                for res in resources:
                    logger.info(f"  {res.uri}: {res.description} ({res.mime_type})")
                
                # Example: Subscribe to conversation history resource
                # The pattern is based on your implementation in instance.py
                contact_id = "example_contact_id"  # Replace with actual contact ID
                conversation_uri = f"whatsapp://conversations/{contact_id}"
                
                logger.info(f"Subscribing to resource: {conversation_uri}")
                try:
                    await session.subscribe_resource(conversation_uri)
                    logger.info(f"Subscribed to {conversation_uri}")
                except Exception as e:
                    logger.error(f"Failed to subscribe: {e}")
                
                # Example: Send a message using the tool
                logger.info("Sending a test message...")
                try:
                    # Try completions before sending message
                    logger.info("Testing argument completion for contact_wa_id...")
                    completion_result = await session.complete_argument(
                        "ref/tool", 
                        "send_message", 
                        "contact_wa_id", 
                        "123"
                    )
                    logger.info(f"Completion results: {completion_result}")
                    
                    # Get the first completion value or use default
                    contact_id = completion_result.get("values", [])[0] if completion_result.get("values") else contact_id
                    
                    # Test message text completion
                    logger.info("Testing argument completion for message_text...")
                    msg_completion = await session.complete_argument(
                        "ref/tool",
                        "send_message",
                        "message_text",
                        "Hello"
                    )
                    logger.info(f"Message text completion results: {msg_completion}")
                    
                    # Use a completion or default message
                    message_text = msg_completion.get("values", [])[0] if msg_completion.get("values") else "Hello from fully-compliant MCP client!"
                
                    # Demonstrate context management
                    logger.info("Testing context management...")
                    
                    # View and configure tenant settings
                    logger.info("Getting tenant settings from context...")
                    tenant_scope = await session.read_resource("mcp://context/tenant")
                    logger.info(f"Tenant settings from resource:\n{tenant_scope}")
                    
                    # Configure tenant settings
                    logger.info("Configuring tenant settings...")
                    tenant_config_result = await session.call_tool(
                        "tenant_configure",
                        arguments={
                            "business_name": "Example WABA Name",
                            "display_name": "Example Bot"
                        }
                    )
                    logger.info(f"Tenant configured: {tenant_config_result.get('message')}")
                    
                    # Set some values in different context scopes
                    logger.info("Setting context values...")
                    await session.call_tool(
                        "context_set",
                        arguments={
                            "scope": "conversation",
                            "key": "last_message",
                            "value": message_text,
                            "ttl": 3600  # 1 hour TTL
                        }
                    )
                    
                    await session.call_tool(
                        "context_set",
                        arguments={
                            "scope": "contact",
                            "key": "contact_name",
                            "value": "Example User"
                        }
                    )
                    
                    await session.call_tool(
                        "context_set",
                        arguments={
                            "scope": "user",
                            "key": "preferences",
                            "value": {
                                "language": "en",
                                "notification_preference": "all"
                            }
                        }
                    )
                    
                    # Get a context value
                    logger.info("Getting a context value...")
                    context_result = await session.call_tool(
                        "context_get",
                        arguments={
                            "scope": "contact",
                            "key": "contact_name",
                            "default": "Unknown User"
                        }
                    )
                    logger.info(f"Contact name from context: {context_result.get('value')}")
                    
                    # Get a snapshot of all context
                    logger.info("Getting context snapshot...")
                    snapshot_result = await session.call_tool(
                        "context_snapshot",
                        arguments={}
                    )
                    logger.info(f"Context snapshot: {json.dumps(snapshot_result.get('snapshot'), indent=2)}")
                    
                    # Read context as a resource
                    logger.info("Reading context as a resource...")
                    context_resource = await session.read_resource("mcp://context")
                    logger.info(f"Context resource:\n{context_resource[0]}")
                    
                    # Send a message using the contact name from context
                    contact_name = context_result.get('value', 'friend')
                    customized_message = f"Hello {contact_name}, {message_text}"
                    
                    # Send the message
                    result = await session.call_tool(
                        "send_message", 
                        arguments={
                            "contact_wa_id": contact_id,
                            "message_text": customized_message
                        }
                    )
                    logger.info(f"Message sent successfully. Result: {result}")
                except Exception as e:
                    logger.error(f"Failed to send message: {e}")
                
                # Keep running to receive notifications until user interrupts
                logger.info("Client running. Press Ctrl+C to exit...")
                try:
                    while True:
                        await asyncio.sleep(1)
                except asyncio.CancelledError:
                    logger.info("Client cancelled")
                
            except Exception as e:
                logger.error(f"Error during client operation: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(run_whatsapp_client())
    except KeyboardInterrupt:
        logger.info("Client stopped by user")
    except Exception as e:
        logger.error(f"Client error: {e}", exc_info=True)
        sys.exit(1)
"""

        # Write the server script
        with open("whatsapp_mcp_stdio.py", "w") as f:
            f.write(server_script)
        
        # Write the client script
        with open("whatsapp_mcp_client.py", "w") as f:
            f.write(client_script)
        
        logger.info("Created fully MCP spec-compliant STDIO server: whatsapp_mcp_stdio.py")
        logger.info("Created fully MCP spec-compliant client: whatsapp_mcp_client.py")
        logger.info("Run server with: python whatsapp_mcp_stdio.py")
        logger.info("Run client with: python whatsapp_mcp_client.py")
        
        # Also add a setting for server version if it doesn't exist
        from app.core.config import settings
        if not hasattr(settings, "SERVER_VERSION"):
            settings_file = "app/core/config.py"
            try:
                with open(settings_file, "r") as f:
                    content = f.read()
                    
                if "SERVER_VERSION" not in content:
                    import re
                    # Find the Settings class
                    match = re.search(r"class Settings\([^)]+\):(.*?)(?:class|\Z)", content, re.DOTALL)
                    if match:
                        # Add SERVER_VERSION to the class
                        class_content = match.group(1)
                        new_class_content = class_content + "    SERVER_VERSION: str = \"1.0.0\"\n    "
                        new_content = content.replace(class_content, new_class_content)
                        
                        with open(settings_file, "w") as f:
                            f.write(new_content)
                        logger.info(f"Added SERVER_VERSION to {settings_file}")
            except Exception as e:
                logger.warning(f"Could not add SERVER_VERSION to settings: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error setting up fully-compliant STDIO mode: {e}")
        return False

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="WhatsApp MCP Server Integration Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # integrate command
    integrate_parser = subparsers.add_parser("integrate", help="Integrate with existing FastAPI app")
    integrate_parser.add_argument("app_path", help="Path to FastAPI app (module:variable)")
    integrate_parser.add_argument("--base-url", default="/api/whatsapp", help="Base URL for webhook")
    integrate_parser.add_argument("--output", help="Output file for integration code")
    
    # stdio command
    subparsers.add_parser("stdio", help="Configure for STDIO communication")
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == "integrate":
        success = create_integration_file(args.app_path, args.base_url, args.output)
        sys.exit(0 if success else 1)
    elif args.command == "stdio":
        setup_stdio_mode()
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 