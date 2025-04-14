import asyncio
import json
import sys
from typing import Dict, Any, Optional, Callable
from loguru import logger

from app.zap_mcp_server.instance import get_mcp_server, initialize_mcp_server

class StdioMCPClient:
    """A client that interacts with the MCP server through standard input/output."""
    
    def __init__(self):
        """Initialize the STDIO MCP client."""
        self.reader = None
        self.writer = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize the MCP server and the STDIO interface."""
        if not self.initialized:
            # Initialize MCP server
            await initialize_mcp_server()
            
            # Set up stdin/stdout as streams
            self.reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(self.reader)
            await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
            
            loop = asyncio.get_event_loop()
            transport, protocol = await loop.connect_write_pipe(
                asyncio.streams.FlowControlMixin, sys.stdout
            )
            self.writer = asyncio.StreamWriter(transport, protocol, self.reader, loop)
            
            self.initialized = True
            logger.info("STDIO MCP client initialized")
    
    async def write_json(self, data: Dict[str, Any]):
        """Write a JSON object to stdout."""
        if not self.writer:
            await self.initialize()
            if not self.writer:
                raise RuntimeError("Failed to initialize writer")
                
        message = json.dumps(data) + "\n"
        self.writer.write(message.encode())
        await self.writer.drain()
    
    async def read_json(self) -> Optional[Dict[str, Any]]:
        """Read a JSON object from stdin."""
        if not self.reader:
            await self.initialize()
            if not self.reader:
                raise RuntimeError("Failed to initialize reader")
                
        try:
            line = await self.reader.readline()
            if not line:
                return None
                
            data = json.loads(line.decode().strip())
            return data
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from stdin")
            return None
        except Exception as e:
            logger.error(f"Error reading from stdin: {e}")
            return None
    
    async def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP request and return a response."""
        try:
            mcp_server = get_mcp_server()
            
            # Extract request details
            request_type = data.get("type")
            content = data.get("content", {})
            
            if request_type == "tool":
                # Handle tool request
                tool_name = content.get("name")
                tool_args = content.get("args", {})
                
                # Call the tool through MCP
                # Use the appropriate method based on your MCP server implementation
                if hasattr(mcp_server, "execute_tool"):
                    result = await mcp_server.execute_tool(tool_name, tool_args)  # type: ignore
                elif hasattr(mcp_server, "call_tool"):
                    result = await mcp_server.call_tool(tool_name, tool_args)
                else:
                    raise AttributeError("MCP server has no method to execute tools")
                
                return {
                    "type": "tool_response",
                    "status": "success",
                    "content": result
                }
                
            elif request_type == "resource":
                # Handle resource request
                resource_uri = content.get("uri")
                
                # Fetch the resource through MCP
                # Use the appropriate method based on your MCP server implementation
                if hasattr(mcp_server, "fetch_resource"):
                    result = await mcp_server.fetch_resource(resource_uri)  # type: ignore
                elif hasattr(mcp_server, "read_resource"):
                    result = await mcp_server.read_resource(resource_uri)
                else:
                    raise AttributeError("MCP server has no method to read resources")
                
                return {
                    "type": "resource_response",
                    "status": "success", 
                    "content": result
                }
                
            else:
                return {
                    "type": "error",
                    "status": "error",
                    "content": {"message": f"Unknown request type: {request_type}"}
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "type": "error",
                "status": "error",
                "content": {"message": str(e)}
            }
    
    async def run_forever(self):
        """Run the STDIO client in a loop, processing requests."""
        await self.initialize()
        
        logger.info("STDIO MCP client started - waiting for input...")
        
        try:
            while True:
                data = await self.read_json()
                if data is None:
                    logger.warning("Received end of input, exiting")
                    break
                    
                response = await self.handle_request(data)
                await self.write_json(response)
                
        except asyncio.CancelledError:
            logger.info("STDIO client task cancelled")
        except Exception as e:
            logger.error(f"Error in STDIO client loop: {e}")
        finally:
            # Clean up if needed
            if self.writer:
                self.writer.close()

def run_stdio_client():
    """Entry point for running the STDIO client."""
    async def main():
        client = StdioMCPClient()
        await client.run_forever()
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("STDIO client interrupted by user")
    except Exception as e:
        logger.error(f"STDIO client exited with error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_stdio_client() 