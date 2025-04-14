from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.utils.http_client import initialize_http_client, close_http_client
from app.utils.redis_client import initialize_redis_client, close_redis_client
from app.zap_mcp_server.instance import initialize_mcp_server # We'll create this next

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize clients and MCP server
    logger.info("Application startup...")
    await initialize_http_client()
    await initialize_redis_client()
    await initialize_mcp_server() # Initialize MCP server with tools/resources
    logger.info("Initialization complete.")
    yield
    # Shutdown: Close clients
    logger.info("Application shutdown...")
    await close_http_client()
    await close_redis_client()
    logger.info("Shutdown complete.") 