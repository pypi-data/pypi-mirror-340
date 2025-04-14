import sys
import asyncio
import uvicorn
from fastapi import FastAPI
from loguru import logger

# Import core components
from app.core.lifespan import lifespan
from app.core.config import settings
from app.api.api_v1.api import api_router

# --- Logging Setup --- #
# Configure Loguru
# Remove default handler
logger.remove()
# Add stderr handler with level from settings
logger.add(sys.stderr, level=settings.LOG_LEVEL)
# Add file handler (optional)
# logger.add("file_{time}.log", level="DEBUG") # Example file logging

# --- FastAPI App Creation --- #
app = FastAPI(
    title="WhatsApp MCP Server",
    description="Integrates WhatsApp Cloud API with the Multi-Controller Protocol (MCP).",
    version="1.0.0",
    lifespan=lifespan, # Use the lifespan context manager
    # Add other FastAPI options like docs_url, redoc_url if needed
)

# --- Mount API Routers --- #
# Include the v1 API router (which contains webhook and MCP endpoints)
# The prefix /api/v1 is optional, but good practice
app.include_router(api_router, prefix="/api/v1")

# Add a root endpoint for basic health check (optional)
@app.get("/", tags=["Health Check"])
async def read_root():
    return {"status": "ok", "message": "WhatsApp MCP Server is running."}


# --- Main Execution Logic (for running with uvicorn) --- #

def start_server():
    """Starts the FastAPI server using uvicorn."""
    logger.info(f"Starting FastAPI server on http://{settings.WEBHOOK_HOST}:{settings.WEBHOOK_PORT}")
    logger.info(f"API V1 available at /api/v1")
    logger.info(f"Webhook endpoint: /api/v1/webhook")
    logger.info(f"MCP WebSocket endpoint: ws://{settings.WEBHOOK_HOST}:{settings.WEBHOOK_PORT}/api/v1/mcp")
    logger.info(f"Log level set to: {settings.LOG_LEVEL}")

    config = uvicorn.Config(
        "app.main:app", # Point uvicorn to the app instance
        host=settings.WEBHOOK_HOST,
        port=settings.WEBHOOK_PORT,
        log_level=settings.LOG_LEVEL.lower(), # Use lowercase for uvicorn
        lifespan="on",
        reload=False # Set reload=True for development if desired
    )
    server = uvicorn.Server(config)

    # Running the server directly (asyncio.run is typically called outside)
    # This function might be called by a script or entry point
    # await server.serve() # Don't await here if called from non-async context
    server.run() # Use run() for synchronous context

# Entry point for pip package CLI command
def run_app():
    """Entry point for the pip-installed CLI command."""
    logger.info("Starting WhatsApp MCP Server as a package...")
    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user.")
    except Exception as e:
         logger.error(f"Server exited with error: {e}", exc_info=True)
         sys.exit(1)

# The if __name__ == "__main__" block is usually in a top-level run script,
# but can be here for direct execution.
if __name__ == "__main__":
    logger.info("Starting WhatsApp MCP Server (Webhook + WebSocket)...")
    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user.")
    except Exception as e:
         logger.error(f"Server exited with error: {e}", exc_info=True)
         sys.exit(1) 