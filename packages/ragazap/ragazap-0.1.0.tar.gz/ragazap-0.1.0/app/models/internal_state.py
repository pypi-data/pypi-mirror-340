from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

# Re-define IncomingMessageType here or import from whatsapp
# For simplicity, let's redefine it if it's small, or import if large/complex
class IncomingMessageType(Enum):
    TEXT = "text"
    BUTTON = "button"
    INTERACTIVE = "interactive"
    LOCATION = "location"
    REACTION = "reaction"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    STICKER = "sticker"
    UNKNOWN = "unknown"
    # Potentially add 'system' or 'agent' types if the agent also logs messages
    AGENT = "agent" # For messages sent *by* the agent


class MessageRole(Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system" # For system messages in the log


class StoredMessageTurn(BaseModel):
    """Represents a single turn in the conversation stored in Redis."""
    wamid: str = Field(..., description="WhatsApp Message ID (WAMID)")
    sender_wa_id: str = Field(..., description="WhatsApp ID of the sender")
    recipient_wa_id: str = Field(..., description="WhatsApp ID of the recipient (Business Phone Number ID)")
    role: MessageRole # 'user' or 'agent'
    content: str
    message_type: IncomingMessageType # Use the enum
    timestamp: datetime
    is_read: bool = False
    agent_tool_calls: Optional[list] = None # Optional field for agent tool calls
    agent_tool_responses: Optional[list] = None # Optional field for tool responses leading to this message
    raw_message_data: Optional[dict] = None # Store original message object if needed 