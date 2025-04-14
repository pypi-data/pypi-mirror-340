"""Session management for the WhatsApp MCP Server"""
import asyncio
import time
import uuid
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from loguru import logger
import json
from app.zap_mcp_server.context_manager import SessionContext

class MCPSession:
    """Represents a single MCP client session."""
    
    def __init__(self, session_id: str, client_info: Optional[Dict[str, Any]] = None):
        self.session_id = session_id
        self.client_info = client_info or {}
        self.created_at = datetime.now()
        self.last_active = self.created_at
        self.subscribed_resources: Set[str] = set()
        self.context_manager = SessionContext()  # Replace simple dict with structured context
        self.active_contact_id: Optional[str] = None
        self.message_history: List[Dict[str, Any]] = []
        self.heartbeat_count = 0
        self.is_expired = False
        
        # Initialize some default context values
        self.context_manager.set_system("session_id", session_id)
        self.context_manager.set_system("created_at", self.created_at.isoformat())
        if client_info:
            for key, value in client_info.items():
                self.context_manager.set_user(f"client_{key}", value)
        
        # Initialize tenant settings
        from app.zap_mcp_server.tenant_settings import initialize_tenant_settings
        initialize_tenant_settings(self.context_manager)
        
    def touch(self):
        """Update the last active timestamp."""
        self.last_active = datetime.now()
        self.heartbeat_count += 1
        
    def add_message(self, message: Dict[str, Any]):
        """Add a message to the session history."""
        self.message_history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
        # Keep only the last 100 messages
        if len(self.message_history) > 100:
            self.message_history = self.message_history[-100:]
            
    def subscribe_to_resource(self, resource_uri: str):
        """Subscribe to a resource."""
        self.subscribed_resources.add(resource_uri)
        
    def unsubscribe_from_resource(self, resource_uri: str):
        """Unsubscribe from a resource."""
        self.subscribed_resources.discard(resource_uri)
        
    def set_context(self, key: str, value: Any):
        """Set a context value."""
        self.context_manager.set_memory(key, value)
        
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context value."""
        return self.context_manager.memory(key, default)
    
    def set_active_contact(self, contact_id: str):
        """Set the active contact being interacted with."""
        self.active_contact_id = contact_id
        # Also store in context
        self.context_manager.set_contact("active_contact_id", contact_id)
        self.context_manager.set_system("last_contact_change", datetime.now().isoformat())
        
    def clear_active_contact(self):
        """Clear the active contact."""
        self.active_contact_id = None
        
    def is_inactive(self, timeout_seconds: int = 3600) -> bool:
        """Check if the session is inactive based on a timeout."""
        return (datetime.now() - self.last_active).total_seconds() > timeout_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to a dictionary for storage/serialization."""
        return {
            "session_id": self.session_id,
            "client_info": self.client_info,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "subscribed_resources": list(self.subscribed_resources),
            "context": self.context_manager.to_dict(),  # Use context manager serialization
            "active_contact_id": self.active_contact_id,
            "heartbeat_count": self.heartbeat_count,
            "is_expired": self.is_expired
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPSession':
        """Create a session from a dictionary."""
        session = cls(data["session_id"], data["client_info"])
        session.created_at = datetime.fromisoformat(data["created_at"])
        session.last_active = datetime.fromisoformat(data["last_active"])
        session.subscribed_resources = set(data["subscribed_resources"])
        
        # Restore context using the context manager
        if "context" in data:
            if isinstance(data["context"], dict) and "scopes" in data["context"]:
                # New format with SessionContext
                session.context_manager = SessionContext.from_dict(data["context"])
            else:
                # Old format with simple dict - migrate
                old_context = data["context"]
                for key, value in old_context.items():
                    # Put old values in the memory scope for persistence
                    session.context_manager.set_memory(key, value)
        
        session.active_contact_id = data["active_contact_id"]
        session.heartbeat_count = data["heartbeat_count"]
        session.is_expired = data["is_expired"]
        return session

class SessionManager:
    """Manages MCP client sessions."""
    
    def __init__(self, session_timeout: int = 3600, cleanup_interval: int = 300):
        self.sessions: Dict[str, MCPSession] = {}
        self.session_timeout = session_timeout  # seconds
        self.cleanup_interval = cleanup_interval  # seconds
        self.cleanup_task = None
        self._redis_key_prefix = "mcp:session:"
        
    async def start(self):
        """Start the session manager and periodic cleanup."""
        self.cleanup_task = asyncio.create_task(self._periodic_cleanup())
        logger.info(f"Session manager started with timeout={self.session_timeout}s, cleanup_interval={self.cleanup_interval}s")
        
    async def stop(self):
        """Stop the session manager."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("Session manager stopped")
        
    async def _periodic_cleanup(self):
        """Periodically clean up expired sessions."""
        try:
            while True:
                await asyncio.sleep(self.cleanup_interval)
                await self.cleanup_expired_sessions()
        except asyncio.CancelledError:
            logger.debug("Session cleanup task cancelled")
            raise
            
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        now = datetime.now()
        expired_sessions = []
        
        for session_id, session in list(self.sessions.items()):
            if session.is_inactive(self.session_timeout):
                expired_sessions.append(session_id)
                session.is_expired = True
                # Persist the final state before removing
                await self._persist_session(session)
                
        for session_id in expired_sessions:
            del self.sessions[session_id]
            
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
    async def create_session(self, session_id: Optional[str] = None, client_info: Optional[Dict[str, Any]] = None) -> MCPSession:
        """Create a new session.
        
        Args:
            session_id: Optional custom session ID
            client_info: Optional client information
            
        Returns:
            The newly created session
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            
        session = MCPSession(session_id, client_info)
        self.sessions[session_id] = session
        
        # Persist the new session
        await self._persist_session(session)
        
        logger.info(f"Created new session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[MCPSession]:
        """Get a session by ID."""
        session = self.sessions.get(session_id)
        if session:
            session.touch()
        return session
    
    async def update_session(self, session: MCPSession):
        """Update a session."""
        if session.session_id in self.sessions:
            self.sessions[session.session_id] = session
            session.touch()
            await self._persist_session(session)
        else:
            logger.warning(f"Tried to update non-existent session: {session.session_id}")
            
    async def close_session(self, session_id: str):
        """Close a session."""
        session = self.sessions.pop(session_id, None)
        if session:
            session.is_expired = True
            # Persist the final state before removing
            await self._persist_session(session)
            logger.info(f"Closed session: {session_id}")
            
    async def _persist_session(self, session: MCPSession):
        """Persist session data to Redis."""
        from app.utils.redis_client import get_redis_client
        try:
            redis = await get_redis_client()
            redis_key = f"{self._redis_key_prefix}{session.session_id}"
            
            # Convert session to JSON and store
            session_data = session.to_dict()
            await redis.set(redis_key, json.dumps(session_data))
            
            # Set expiry for expired sessions
            if session.is_expired:
                # Keep expired sessions for 7 days for analytics
                await redis.expire(redis_key, 60 * 60 * 24 * 7)
            
        except Exception as e:
            logger.error(f"Failed to persist session {session.session_id}: {e}")
            
    async def load_session(self, session_id: str) -> Optional[MCPSession]:
        """Load session data from Redis."""
        from app.utils.redis_client import get_redis_client
        try:
            redis = await get_redis_client()
            redis_key = f"{self._redis_key_prefix}{session_id}"
            
            session_data = await redis.get(redis_key)
            if not session_data:
                return None
                
            session_dict = json.loads(session_data)
            session = MCPSession.from_dict(session_dict)
            
            # Only load non-expired sessions
            if not session.is_expired:
                self.sessions[session_id] = session
                return session
                
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {e}")
            
        return None
        
    async def get_active_sessions_count(self) -> int:
        """Get the count of active sessions."""
        return len(self.sessions)
        
    async def get_sessions_by_contact(self, contact_id: str) -> List[MCPSession]:
        """Get all sessions currently interacting with a specific contact."""
        return [
            session for session in self.sessions.values() 
            if session.active_contact_id == contact_id
        ]
        
    async def get_sessions_subscribed_to_resource(self, resource_uri: str) -> List[MCPSession]:
        """Get all sessions subscribed to a specific resource."""
        return [
            session for session in self.sessions.values()
            if resource_uri in session.subscribed_resources
        ]
        
    async def broadcast_to_sessions(self, message: Dict[str, Any], filter_func=None):
        """Broadcast a message to all sessions that match the filter."""
        target_sessions = self.sessions.values()
        if filter_func:
            target_sessions = [s for s in target_sessions if filter_func(s)]
            
        for session in target_sessions:
            session.add_message(message)
            # Note: actual message delivery would happen elsewhere
            
        return len(target_sessions)

# Global instance
_session_manager: Optional[SessionManager] = None

async def get_session_manager() -> SessionManager:
    """Get the global session manager instance."""
    global _session_manager
    if _session_manager is None:
        from app.core.config import settings
        timeout = getattr(settings, "SESSION_TIMEOUT", 3600)
        _session_manager = SessionManager(session_timeout=timeout)
        await _session_manager.start()
    return _session_manager 