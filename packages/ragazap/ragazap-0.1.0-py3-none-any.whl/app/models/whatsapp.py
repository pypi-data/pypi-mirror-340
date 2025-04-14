from pydantic import BaseModel, Field, TypeAdapter
from typing import List, Optional, Any, Dict, Union, Literal
from enum import Enum

# --- Enums --- #
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
    ORDER = "order"
    SYSTEM = "system"
    # Add other types as needed from Meta docs

class InteractiveType(Enum):
    BUTTON_REPLY = "button_reply"
    LIST_REPLY = "list_reply"

class WhatsAppIdType(Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"

class MessageStatus(Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    DELETED = "deleted"

# --- Nested Models --- #

# Common Components
class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str = Field(..., description="Sender WhatsApp ID")

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str = Field(..., description="Recipient Business Phone Number ID")

class Origin(BaseModel):
    type: str # e.g., "user_initiated", "business_initiated"

class Pricing(BaseModel):
    billable: bool
    pricing_model: str # e.g., "CBP"
    category: str # e.g., "user_initiated"

class Conversation(BaseModel):
    id: str
    origin: Origin
    # Optional: expiration_timestamp if needed

class StatusError(BaseModel):
    code: int
    title: str
    # Optional: message, error_data

class Status(BaseModel):
    id: str = Field(..., description="WAMID of the message being updated")
    status: MessageStatus
    timestamp: str
    recipient_id: str = Field(..., description="Recipient WhatsApp ID")
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[StatusError]] = None

# Message Type Specific Components
class Text(BaseModel):
    body: str

class Button(BaseModel):
    payload: str
    text: str

class ButtonReply(BaseModel):
    id: str
    title: str

class ListReply(BaseModel):
    id: str
    title: str
    description: Optional[str] = None

class Interactive(BaseModel):
    type: InteractiveType
    button_reply: Optional[ButtonReply] = None
    list_reply: Optional[ListReply] = None

class Location(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None

class Reaction(BaseModel):
    message_id: str = Field(..., description="WAMID of the message being reacted to")
    emoji: str

class MediaBase(BaseModel):
    id: str # Media ID
    mime_type: str
    sha256: Optional[str] = None
    caption: Optional[str] = None

class Image(MediaBase):
    pass

class Audio(MediaBase):
    voice: Optional[bool] = None # True if it's a voice note

class Video(MediaBase):
    pass

class Document(MediaBase):
    filename: Optional[str] = None

class Sticker(MediaBase):
    animated: Optional[bool] = None

class System(BaseModel):
    body: str # Description of the system event
    # type: Optional[str] = None # e.g., "user_changed_number"
    # identity: Optional[str] = None # Related to identity changes
    # wa_id: Optional[str] = None # User associated with the system event

# --- Main Incoming Message Model --- #
class IncomingMessageBase(BaseModel):
    id: str = Field(..., description="WhatsApp Message ID (WAMID)")
    from_: str = Field(..., alias="from", description="Sender WhatsApp ID")
    timestamp: str # Unix timestamp as string
    type: IncomingMessageType
    context: Optional[Dict[str, Any]] = None # For forwarded messages, replies, etc.

# Using inheritance with discriminated unions (supported in Pydantic v2)
# Need explicit type definition for the union
class IncomingTextMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.TEXT] = IncomingMessageType.TEXT
    text: Text

class IncomingButtonMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.BUTTON] = IncomingMessageType.BUTTON
    button: Button

class IncomingInteractiveMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.INTERACTIVE] = IncomingMessageType.INTERACTIVE
    interactive: Interactive

class IncomingLocationMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.LOCATION] = IncomingMessageType.LOCATION
    location: Location

class IncomingReactionMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.REACTION] = IncomingMessageType.REACTION
    reaction: Reaction

class IncomingImageMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.IMAGE] = IncomingMessageType.IMAGE
    image: Image

class IncomingAudioMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.AUDIO] = IncomingMessageType.AUDIO
    audio: Audio

class IncomingVideoMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.VIDEO] = IncomingMessageType.VIDEO
    video: Video

class IncomingDocumentMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.DOCUMENT] = IncomingMessageType.DOCUMENT
    document: Document

class IncomingStickerMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.STICKER] = IncomingMessageType.STICKER
    sticker: Sticker

class IncomingOrderMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.ORDER] = IncomingMessageType.ORDER
    order: Dict[str, Any] # Placeholder for complex order structure

class IncomingSystemMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.SYSTEM] = IncomingMessageType.SYSTEM
    system: System

class IncomingUnknownMessage(IncomingMessageBase):
    type: Literal[IncomingMessageType.UNKNOWN] = IncomingMessageType.UNKNOWN
    # Include other fields if Meta sends them for unknown types

# Create a Union of all possible incoming message types
IncomingMessageObject = Union[
    IncomingTextMessage,
    IncomingButtonMessage,
    IncomingInteractiveMessage,
    IncomingLocationMessage,
    IncomingReactionMessage,
    IncomingImageMessage,
    IncomingAudioMessage,
    IncomingVideoMessage,
    IncomingDocumentMessage,
    IncomingStickerMessage,
    IncomingOrderMessage,
    IncomingSystemMessage,
    IncomingUnknownMessage
]

# Adapter for easy validation
IncomingMessageAdapter = TypeAdapter(IncomingMessageObject)

# --- Webhook Payload Structure --- #

class ChangeValue(BaseModel):
    messaging_product: str = Field(...)
    metadata: Metadata
    contacts: Optional[List[Contact]] = None # Present for messages
    messages: Optional[List[IncomingMessageObject]] = None # Present for messages
    statuses: Optional[List[Status]] = None # Present for status updates
    errors: Optional[List[StatusError]] = None # Present for errors

    # Pydantic v2 validator to ensure either messages or statuses/errors exist
    # @model_validator(mode='after')
    # def check_messages_or_statuses(self) -> 'ChangeValue':
    #     if not self.messages and not self.statuses and not self.errors:
    #         raise ValueError("Webhook value must contain messages, statuses, or errors")
    #     return self

class Change(BaseModel):
    value: ChangeValue
    field: str = Field(...)

class Entry(BaseModel):
    id: str # Business Account ID
    changes: List[Change]

class WhatsappWebhookRequest(BaseModel):
    object: str = Field(...)
    entry: List[Entry]

# Re-introduce the simple TypeAdapter for the root list if needed for parsing
# WhatsappWebhookRequestAdapter = TypeAdapter(WhatsappWebhookRequest)

# If the webhook payload is sometimes just a list of entries:
# WebhookPayload = Union[WhatsappWebhookRequest, List[Entry]]
# WebhookPayloadAdapter = TypeAdapter(WebhookPayload) 