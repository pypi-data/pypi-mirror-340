"""Completions support for the WhatsApp MCP Server"""
from typing import List, Dict, Any, Optional
from loguru import logger
import re

# Contact IDs completion helper
async def complete_contact_wa_id(current_value: str) -> List[str]:
    """Provide completions for WhatsApp contact IDs.
    
    This implementation would normally fetch from a database of contacts.
    For demo purposes, we're returning some sample values.
    """
    # Sample contacts (in production, fetch from database)
    sample_contacts = [
        "1234567890",
        "1234567891",
        "9876543210",
        "2345678901",
        "5551234567",
        "5559876543"
    ]
    
    # Filter based on the current value
    if not current_value:
        return sample_contacts[:5]  # Return first 5 if empty
    
    matches = [contact for contact in sample_contacts if contact.startswith(current_value)]
    return matches[:10]  # Return up to 10 matches

# Message template completions
async def complete_message_template(current_value: str) -> List[str]:
    """Provide completions for message templates."""
    templates = [
        "Hello, thank you for contacting us.",
        "We appreciate your business.",
        "I'll look into that right away.",
        "Is there anything else I can help you with?",
        "Our business hours are 9am-5pm Monday through Friday.",
        "Let me transfer you to our support team.",
        "Your order has been processed.",
        "Your appointment is confirmed."
    ]
    
    # Filter based on current value
    if not current_value:
        return templates[:5]
    
    # Simple fuzzy matching
    matches = []
    for template in templates:
        if current_value.lower() in template.lower():
            matches.append(template)
    
    return matches[:10]

# Resource URI completions
async def complete_resource_uri(uri_prefix: str, current_value: str) -> List[str]:
    """Complete resource URIs based on the provided prefix and current value."""
    if uri_prefix == "whatsapp://conversations/":
        # Complete contact IDs for conversation history
        contact_ids = await complete_contact_wa_id(current_value)
        return [f"{uri_prefix}{contact_id}" for contact_id in contact_ids]
    
    return []

# Map of argument names to completion providers
COMPLETION_PROVIDERS = {
    "contact_wa_id": complete_contact_wa_id,
    "message_text": complete_message_template,
}

async def handle_completion_request(ref_type: str, ref_name: str, arg_name: str, current_value: str) -> Dict[str, Any]:
    """Handle a completion request from the MCP client.
    
    Args:
        ref_type: The type of reference (ref/prompt or ref/resource)
        ref_name: The name of the prompt or the URI of the resource
        arg_name: The argument name to complete
        current_value: The current value of the argument
        
    Returns:
        A completion result dictionary
    """
    logger.debug(f"Handling completion request: {ref_type}, {ref_name}, {arg_name}, value='{current_value}'")
    
    values = []
    
    try:
        # Handle resource URI completions
        if ref_type == "ref/resource" and ref_name.startswith("whatsapp://"):
            # Extract the URI prefix
            prefix_match = re.match(r"(whatsapp://[^/]+/)", ref_name)
            if prefix_match:
                uri_prefix = prefix_match.group(1)
                # Get completions for the URI
                values = await complete_resource_uri(uri_prefix, current_value)
        
        # Handle tool argument completions
        elif ref_type == "ref/tool":
            if arg_name in COMPLETION_PROVIDERS:
                provider = COMPLETION_PROVIDERS[arg_name]
                values = await provider(current_value)
        
        # Handle prompt argument completions
        elif ref_type == "ref/prompt":
            # For now, we'll just use the same providers as tools
            if arg_name in COMPLETION_PROVIDERS:
                provider = COMPLETION_PROVIDERS[arg_name]
                values = await provider(current_value)
    
    except Exception as e:
        logger.error(f"Error handling completion request: {e}")
        values = []
    
    # Return the completion result
    return {
        "values": values[:100],  # Limit to 100 items per spec
        "total": len(values),
        "hasMore": len(values) > 100
    }

# Register completion handlers with the MCP server
def register_completion_handlers(mcp_server):
    """Register completion handlers with the MCP server instance."""
    logger.info("Registering completion handlers with MCP server")
    
    # If the server has a direct completion registration method, use it
    if hasattr(mcp_server, "completion") and callable(getattr(mcp_server, "completion")):
        # Register handlers for specific argument names
        for arg_name in COMPLETION_PROVIDERS:
            logger.debug(f"Registering completion handler for argument: {arg_name}")
            
            # This pattern depends on the actual MCP SDK API
            # The specifics might need adjustment based on the SDK version
            @mcp_server.completion(arg_name)
            async def complete_arg(value: str, arg: str = arg_name):
                provider = COMPLETION_PROVIDERS.get(arg)
                if provider:
                    return await provider(value)
                return []
    
    logger.info("Completion handlers registered successfully") 