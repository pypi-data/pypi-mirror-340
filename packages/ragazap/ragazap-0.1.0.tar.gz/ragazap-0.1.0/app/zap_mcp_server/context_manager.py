"""Context management for WhatsApp MCP sessions."""
from typing import Dict, Any, Optional, List, Union, Set
from datetime import datetime
from loguru import logger
import json
import copy

class ContextValue:
    """Represents a value in the context with metadata."""
    
    def __init__(self, value: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Initialize a context value.
        
        Args:
            value: The actual value to store
            ttl: Time-to-live in seconds (None means no expiration)
            metadata: Additional metadata about this value
        """
        self.value = value
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.ttl = ttl
        self.metadata = metadata or {}
        self.access_count = 0
        
    def is_expired(self) -> bool:
        """Check if this value has expired based on TTL."""
        if self.ttl is None:
            return False
        return (datetime.now() - self.updated_at).total_seconds() > self.ttl
        
    def touch(self):
        """Update the last access time and count."""
        self.access_count += 1
        
    def update(self, value: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Update this context value."""
        self.value = value
        self.updated_at = datetime.now()
        if ttl is not None:
            self.ttl = ttl
        if metadata:
            self.metadata.update(metadata)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "ttl": self.ttl,
            "metadata": self.metadata,
            "access_count": self.access_count
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextValue':
        """Create from a dictionary."""
        value = cls(
            data["value"],
            ttl=data.get("ttl"),
            metadata=data.get("metadata", {})
        )
        value.created_at = datetime.fromisoformat(data["created_at"])
        value.updated_at = datetime.fromisoformat(data["updated_at"])
        value.access_count = data.get("access_count", 0)
        return value

class ContextScope:
    """A scope for organizing context values (e.g., 'conversation', 'user', 'system')."""
    
    def __init__(self, name: str):
        """Initialize a context scope.
        
        Args:
            name: The name of this scope
        """
        self.name = name
        self.values: Dict[str, ContextValue] = {}
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from this scope."""
        if key not in self.values:
            return default
            
        value_obj = self.values[key]
        if value_obj.is_expired():
            del self.values[key]
            return default
            
        value_obj.touch()
        return value_obj.value
        
    def set(self, key: str, value: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Set a value in this scope."""
        if key in self.values:
            self.values[key].update(value, ttl, metadata)
        else:
            self.values[key] = ContextValue(value, ttl, metadata)
            
    def delete(self, key: str) -> bool:
        """Delete a value from this scope.
        
        Returns:
            True if the key existed and was deleted, False otherwise
        """
        if key in self.values:
            del self.values[key]
            return True
        return False
        
    def clear(self):
        """Clear all values from this scope."""
        self.values.clear()
        
    def has(self, key: str) -> bool:
        """Check if a key exists in this scope."""
        if key not in self.values:
            return False
        if self.values[key].is_expired():
            del self.values[key]
            return False
        return True
        
    def keys(self) -> List[str]:
        """Get all active keys in this scope."""
        # Remove expired values first
        expired_keys = [k for k, v in self.values.items() if v.is_expired()]
        for k in expired_keys:
            del self.values[k]
            
        return list(self.values.keys())
        
    def items(self) -> List[tuple]:
        """Get all active key-value pairs in this scope."""
        # Remove expired values first
        expired_keys = [k for k, v in self.values.items() if v.is_expired()]
        for k in expired_keys:
            del self.values[k]
            
        return [(k, v.value) for k, v in self.values.items()]
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return {
            "name": self.name,
            "values": {k: v.to_dict() for k, v in self.values.items() if not v.is_expired()}
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextScope':
        """Create from a dictionary."""
        scope = cls(data["name"])
        for key, value_data in data.get("values", {}).items():
            scope.values[key] = ContextValue.from_dict(value_data)
        return scope

class SessionContext:
    """Manages context data for an MCP session with multiple scopes."""
    
    # Standard scope names
    CONVERSATION = "conversation"  # For current conversation state
    USER = "user"                  # For user-specific data
    SYSTEM = "system"              # For system configuration
    CONTACT = "contact"            # For WhatsApp contact information
    MEMORY = "memory"              # For persistent memory across conversations
    TENANT = "tenant"              # For tenant-specific WhatsApp Business API settings
    
    def __init__(self):
        """Initialize the session context."""
        self.scopes: Dict[str, ContextScope] = {}
        self._ensure_standard_scopes()
        
    def _ensure_standard_scopes(self):
        """Ensure standard scopes exist."""
        for scope_name in [self.CONVERSATION, self.USER, self.SYSTEM, self.CONTACT, self.MEMORY, self.TENANT]:
            if scope_name not in self.scopes:
                self.scopes[scope_name] = ContextScope(scope_name)
                
    def scope(self, name: str) -> ContextScope:
        """Get or create a scope by name."""
        if name not in self.scopes:
            self.scopes[name] = ContextScope(name)
        return self.scopes[name]
        
    def get(self, scope: str, key: str, default: Any = None) -> Any:
        """Get a value from a specific scope."""
        return self.scope(scope).get(key, default)
        
    def set(self, scope: str, key: str, value: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Set a value in a specific scope."""
        self.scope(scope).set(key, value, ttl, metadata)
        
    def delete(self, scope: str, key: str) -> bool:
        """Delete a value from a specific scope."""
        return self.scope(scope).delete(key)
        
    def clear_scope(self, scope: str):
        """Clear all values in a specific scope."""
        if scope in self.scopes:
            self.scopes[scope].clear()
            
    def clear_all(self):
        """Clear all values in all scopes."""
        for scope in self.scopes.values():
            scope.clear()
            
    def has(self, scope: str, key: str) -> bool:
        """Check if a key exists in a specific scope."""
        if scope not in self.scopes:
            return False
        return self.scopes[scope].has(key)
        
    def list_scopes(self) -> List[str]:
        """List all available scopes."""
        return list(self.scopes.keys())
        
    def list_keys(self, scope: str) -> List[str]:
        """List all keys in a specific scope."""
        if scope not in self.scopes:
            return []
        return self.scopes[scope].keys()
        
    # Convenience methods for standard scopes
    
    def conversation(self, key: str, default: Any = None) -> Any:
        """Get a conversation context value."""
        return self.get(self.CONVERSATION, key, default)
        
    def set_conversation(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a conversation context value."""
        self.set(self.CONVERSATION, key, value, ttl)
        
    def user(self, key: str, default: Any = None) -> Any:
        """Get a user context value."""
        return self.get(self.USER, key, default)
        
    def set_user(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a user context value."""
        self.set(self.USER, key, value, ttl)
        
    def system(self, key: str, default: Any = None) -> Any:
        """Get a system context value."""
        return self.get(self.SYSTEM, key, default)
        
    def set_system(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a system context value."""
        self.set(self.SYSTEM, key, value, ttl)
        
    def contact(self, key: str, default: Any = None) -> Any:
        """Get a contact context value."""
        return self.get(self.CONTACT, key, default)
        
    def set_contact(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a contact context value."""
        self.set(self.CONTACT, key, value, ttl)
        
    def memory(self, key: str, default: Any = None) -> Any:
        """Get a persistent memory value."""
        return self.get(self.MEMORY, key, default)
        
    def set_memory(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a persistent memory value."""
        self.set(self.MEMORY, key, value, ttl)
        
    def tenant(self, key: str, default: Any = None) -> Any:
        """Get a tenant setting value."""
        return self.get(self.TENANT, key, default)
        
    def set_tenant(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a tenant setting value."""
        self.set(self.TENANT, key, value, ttl)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return {
            "scopes": {name: scope.to_dict() for name, scope in self.scopes.items()}
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionContext':
        """Create from a dictionary."""
        context = cls()
        for name, scope_data in data.get("scopes", {}).items():
            context.scopes[name] = ContextScope.from_dict(scope_data)
        return context
        
    def create_snapshot(self) -> Dict[str, Any]:
        """Create a simple snapshot of all current values across scopes."""
        snapshot = {}
        for scope_name, scope in self.scopes.items():
            snapshot[scope_name] = dict(scope.items())
        return snapshot

# Helper function to get and attach context to current task
def get_current_context() -> Optional[SessionContext]:
    """Get the context attached to the current task."""
    import asyncio
    current_task = asyncio.current_task()
    if not current_task:
        return None
        
    # Try to get session first
    session = getattr(current_task, "mcp_session", None)
    if session and hasattr(session, "context_manager"):
        return session.context_manager
        
    # Fall back to direct context attachment
    return getattr(current_task, "mcp_context", None)

def set_current_context(context: SessionContext):
    """Set the context on the current task."""
    import asyncio
    current_task = asyncio.current_task()
    if not current_task:
        return
        
    setattr(current_task, "mcp_context", context) 