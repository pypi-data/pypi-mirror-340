"""Tenant settings management for WhatsApp MCP Server."""
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field
from loguru import logger
import uuid

from app.core.config import settings
from app.zap_mcp_server.context_manager import SessionContext, get_current_context

class PhoneNumberSettings(BaseModel):
    """Settings for a WhatsApp phone number."""
    id: str  # Phone number ID from Meta
    display_number: str  # Formatted phone number with country code
    waba_id: str  # Parent WABA ID
    display_name: Optional[str] = None
    is_default: bool = False
    verified: bool = True
    quality_rating: Optional[str] = None  # e.g., "GREEN", "YELLOW", "RED"
    
    # Metadata
    phone_number_uuid: Optional[str] = None  # Internal UUID for this phone number

class WABASettings(BaseModel):
    """Settings for a WhatsApp Business Account."""
    id: str  # WABA ID from Meta
    business_name: str
    display_name: Optional[str] = None
    verification_status: str = "VERIFIED"  # or "PENDING", "REJECTED"
    currency: str = "USD"
    timezone_id: Optional[str] = None
    
    # API credentials
    api_token: str
    api_version: str = "v18.0"
    
    # Webhook settings
    webhook_url: Optional[str] = None
    webhook_verification_token: Optional[str] = None
    
    # Phone numbers under this WABA
    phone_numbers: List[PhoneNumberSettings] = []
    
    # Metadata
    waba_uuid: Optional[str] = None  # Internal UUID for this WABA
    is_default: bool = False

class TenantSettings(BaseModel):
    """Settings for a tenant with multiple WABAs."""
    tenant_id: str
    name: str
    wabas: List[WABASettings] = []
    default_waba_id: Optional[str] = None
    
    # Internal mappings for quick lookups
    _phone_id_to_waba: Dict[str, str] = Field(default_factory=dict)
    _waba_id_to_phones: Dict[str, List[str]] = Field(default_factory=dict)
    
    def __init__(self, **data):
        super().__init__(**data)
        self._build_mappings()
    
    def _build_mappings(self):
        """Build internal mappings for quick lookups."""
        self._phone_id_to_waba = {}
        self._waba_id_to_phones = {}
        
        for waba in self.wabas:
            if waba.waba_uuid is None:
                waba.waba_uuid = str(uuid.uuid4())
                
            phone_ids = []
            for phone in waba.phone_numbers:
                if phone.phone_number_uuid is None:
                    phone.phone_number_uuid = str(uuid.uuid4())
                    
                self._phone_id_to_waba[phone.id] = waba.id
                phone_ids.append(phone.id)
                
            self._waba_id_to_phones[waba.id] = phone_ids
            
    def get_waba_for_phone(self, phone_id: str) -> Optional[WABASettings]:
        """Get the WABA for a specific phone ID."""
        waba_id = self._phone_id_to_waba.get(phone_id)
        if not waba_id:
            return None
            
        for waba in self.wabas:
            if waba.id == waba_id:
                return waba
                
        return None
        
    def get_phone(self, phone_id: str) -> Optional[PhoneNumberSettings]:
        """Get a phone number by ID."""
        for waba in self.wabas:
            for phone in waba.phone_numbers:
                if phone.id == phone_id:
                    return phone
        return None
        
    def get_default_waba(self) -> Optional[WABASettings]:
        """Get the default WABA."""
        if self.default_waba_id:
            for waba in self.wabas:
                if waba.id == self.default_waba_id:
                    return waba
                    
        # Try to find one marked as default
        for waba in self.wabas:
            if waba.is_default:
                return waba
                
        # Just return the first one if any exist
        return self.wabas[0] if self.wabas else None
        
    def get_default_phone(self, waba_id: Optional[str] = None) -> Optional[PhoneNumberSettings]:
        """Get the default phone number for a WABA, or overall."""
        if waba_id:
            # Get default phone for specific WABA
            for waba in self.wabas:
                if waba.id == waba_id:
                    # Try to find one marked as default
                    for phone in waba.phone_numbers:
                        if phone.is_default:
                            return phone
                    # Otherwise return first one
                    return waba.phone_numbers[0] if waba.phone_numbers else None
        else:
            # Get overall default phone
            default_waba = self.get_default_waba()
            if default_waba:
                return self.get_default_phone(default_waba.id)
                
        return None
        
    def add_waba(self, waba: WABASettings) -> WABASettings:
        """Add a new WABA to the tenant."""
        # Ensure it has a UUID
        if waba.waba_uuid is None:
            waba.waba_uuid = str(uuid.uuid4())
            
        # Add to collection
        self.wabas.append(waba)
        
        # Update mappings
        self._build_mappings()
        
        # Set as default if first one
        if len(self.wabas) == 1:
            self.default_waba_id = waba.id
            waba.is_default = True
            
        return waba
        
    def add_phone(self, waba_id: str, phone: PhoneNumberSettings) -> Optional[PhoneNumberSettings]:
        """Add a phone number to a WABA."""
        # Find the WABA
        target_waba = None
        for waba in self.wabas:
            if waba.id == waba_id:
                target_waba = waba
                break
                
        if not target_waba:
            return None
            
        # Ensure it has a UUID and correct WABA ID
        if phone.phone_number_uuid is None:
            phone.phone_number_uuid = str(uuid.uuid4())
        phone.waba_id = waba_id
        
        # Add to collection
        target_waba.phone_numbers.append(phone)
        
        # Update mappings
        self._build_mappings()
        
        # Set as default if first one for this WABA
        if len(target_waba.phone_numbers) == 1:
            phone.is_default = True
            
        return phone

def get_default_tenant_settings() -> TenantSettings:
    """Get default tenant settings from environment configuration."""
    # Check if we're in standalone mode
    if not settings.STANDALONE_MODE:
        # In client mode, create an empty tenant that will be populated by the client
        return TenantSettings(
            tenant_id="default_tenant",
            name="Default Tenant",
            wabas=[]  # Empty list, will be populated by client
        )

    # In standalone mode, create tenant with environment settings
    # The business phone number is derived from the ID
    phone_id = settings.BUSINESS_PHONE_NUMBER_ID
    if not phone_id:
        logger.warning("BUSINESS_PHONE_NUMBER_ID not set in standalone mode")
        return TenantSettings(
            tenant_id="default_tenant",
            name="Default Tenant",
            wabas=[]  # Empty list since we don't have credentials
        )

    formatted_phone = f"+{phone_id}" if not phone_id.startswith("+") else phone_id
    
    # Create default phone
    phone = PhoneNumberSettings(
        id=phone_id,
        display_number=formatted_phone,
        waba_id="default_waba",  # Temporary ID, will be replaced
        is_default=True
    )
    
    # Create default WABA
    waba = WABASettings(
        id="default_waba",
        business_name=getattr(settings, "BUSINESS_NAME", "WhatsApp Business"),
        api_token=settings.WHATSAPP_API_TOKEN,
        api_version=settings.META_API_VERSION,
        webhook_verification_token=settings.WEBHOOK_VERIFY_TOKEN,
        display_name=getattr(settings, "DISPLAY_NAME", None),
        is_default=True,
        phone_numbers=[phone]
    )
    
    # Create tenant
    tenant = TenantSettings(
        tenant_id="default_tenant",
        name="Default Tenant",
        wabas=[waba],
        default_waba_id=waba.id
    )
    
    return tenant

def initialize_tenant_settings(context: SessionContext):
    """Initialize tenant settings in the context."""
    tenant_settings = get_default_tenant_settings()
    
    # Store the full tenant settings object
    context.set_tenant("tenant_settings", tenant_settings.model_dump())
    
    # Store convenience references to default values
    default_waba = tenant_settings.get_default_waba()
    default_phone = tenant_settings.get_default_phone()
    
    if default_waba:
        context.set_tenant("default_waba_id", default_waba.id)
        context.set_tenant("default_api_token", default_waba.api_token)
        context.set_tenant("default_api_version", default_waba.api_version)
    
    if default_phone:
        context.set_tenant("default_phone_id", default_phone.id)
        context.set_tenant("default_phone_number", default_phone.display_number)
    
    # Compute and cache the default API URL
    if default_waba and default_phone:
        api_url = f"https://graph.facebook.com/{default_waba.api_version}/{default_phone.id}/messages"
        context.set_tenant("default_api_url", api_url)
    
    logger.info(f"Initialized multi-tenant settings with {len(tenant_settings.wabas)} WABAs")
    return tenant_settings

def get_tenant_settings() -> Optional[Dict[str, Any]]:
    """Get the current tenant settings for the active session."""
    context = get_current_context()
    if not context:
        logger.warning("No context available for current request")
        # Fall back to default settings if no context
        return get_default_tenant_settings().model_dump()
    
    # Get the full settings dictionary
    tenant_settings = context.tenant("tenant_settings")
    if not tenant_settings:
        # If not found, initialize it
        tenant_settings = initialize_tenant_settings(context).model_dump()
    
    return tenant_settings

def get_waba_for_phone(phone_id: str) -> Optional[Dict[str, Any]]:
    """Get the WABA settings for a specific phone number."""
    context = get_current_context()
    if not context:
        # Fall back to default
        tenant = get_default_tenant_settings()
        waba = tenant.get_waba_for_phone(phone_id)
        return waba.model_dump() if waba else None
    
    # Try to get from context
    tenant_data = context.tenant("tenant_settings")
    if not tenant_data:
        return None
    
    # Create tenant model to use its helper methods
    tenant = TenantSettings(**tenant_data)
    waba = tenant.get_waba_for_phone(phone_id)
    return waba.model_dump() if waba else None

def get_api_url_for_phone(phone_id: str) -> str:
    """Get the API URL for a specific phone number."""
    # Get the WABA for this phone
    waba_data = get_waba_for_phone(phone_id)
    if not waba_data:
        # Fall back to default
        context = get_current_context()
        if context:
            return context.tenant("default_api_url", get_default_api_url())
        return get_default_api_url()
    
    # Construct URL from WABA data
    return f"https://graph.facebook.com/{waba_data.get('api_version', 'v18.0')}/{phone_id}/messages"

def get_api_token_for_phone(phone_id: str) -> str:
    """Get the API token for a specific phone number."""
    # Get the WABA for this phone
    waba_data = get_waba_for_phone(phone_id)
    if not waba_data:
        # Fall back to default
        context = get_current_context()
        if context:
            return context.tenant("default_api_token", settings.WHATSAPP_API_TOKEN)
        return settings.WHATSAPP_API_TOKEN
    
    # Get token from WABA data
    return waba_data.get("api_token", settings.WHATSAPP_API_TOKEN)

def get_default_api_url() -> str:
    """Get the default WhatsApp API URL."""
    context = get_current_context()
    if context:
        default_url = context.tenant("default_api_url")
        if default_url:
            return default_url
    
    # Construct from settings if not in context
    tenant = get_default_tenant_settings()
    default_waba = tenant.get_default_waba()
    default_phone = tenant.get_default_phone()
    
    if default_waba and default_phone:
        return f"https://graph.facebook.com/{default_waba.api_version}/{default_phone.id}/messages"
    
    # Ultimate fallback using settings
    return f"https://graph.facebook.com/{settings.META_API_VERSION}/{settings.BUSINESS_PHONE_NUMBER_ID}/messages"

def get_tenant_api_url() -> str:
    """Get the default WhatsApp API URL for the current tenant."""
    return get_default_api_url()

def get_tenant_api_token() -> str:
    """Get the default WhatsApp API token for the current tenant."""
    context = get_current_context()
    if context:
        token = context.tenant("default_api_token")
        if token:
            return token
    
    return settings.WHATSAPP_API_TOKEN

def get_tenant_phone_id() -> str:
    """Get the default business phone number ID for the current tenant."""
    context = get_current_context()
    if context:
        phone_id = context.tenant("default_phone_id")
        if phone_id:
            return phone_id
    
    return settings.BUSINESS_PHONE_NUMBER_ID

def get_tenant_business_phone() -> str:
    """Get the default business phone number for the current tenant."""
    context = get_current_context()
    if context:
        phone = context.tenant("default_phone_number")
        if phone:
            return phone
    
    # Format phone ID as phone number if not in context
    phone_id = settings.BUSINESS_PHONE_NUMBER_ID
    return f"+{phone_id}" if not phone_id.startswith("+") else phone_id 