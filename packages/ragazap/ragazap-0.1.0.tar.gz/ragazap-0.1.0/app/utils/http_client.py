import httpx
from loguru import logger

# Global HTTP client instance
_http_client: httpx.AsyncClient | None = None

async def initialize_http_client():
    """Initializes the global httpx.AsyncClient."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient()
        logger.info("HTTPX AsyncClient initialized.")

async def close_http_client():
    """Closes the global httpx.AsyncClient."""
    global _http_client
    if _http_client:
        await _http_client.aclose()
        _http_client = None
        logger.info("HTTPX AsyncClient closed.")

async def get_http_client() -> httpx.AsyncClient:
    """Returns the initialized global httpx.AsyncClient."""
    if _http_client is None:
        logger.warning("HTTP client accessed before initialization.")
        # Optionally initialize here or raise an error depending on desired behavior
        await initialize_http_client()
        if _http_client is None: # Check again after attempting init
             raise ConnectionError("HTTP client is not available.")
    return _http_client 