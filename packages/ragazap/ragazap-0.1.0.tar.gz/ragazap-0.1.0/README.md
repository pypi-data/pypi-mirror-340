# Ragazap

A WhatsApp Multi-Capability Protocol (MCP) server that integrates the WhatsApp Cloud API with AI capabilities.

## Features

- Receive and process WhatsApp messages via webhook
- Expose MCP WebSocket endpoint for AI agent connections
- Send messages to WhatsApp contacts
- Store and retrieve conversation history in Redis
- Support for text messages
- Tools for AI agents to interact with WhatsApp
- Two operation modes: Standalone and Client

## Operation Modes

### Standalone Mode
In standalone mode, the server operates independently with its own WhatsApp Business API credentials. This mode is useful for:
- Direct integration with WhatsApp
- Testing and development
- Single-tenant deployments

### Client Mode
In client mode, the server expects WhatsApp credentials to be provided by the client through the MCP protocol. This mode is useful for:
- Multi-tenant deployments
- Managed service providers
- Clients managing their own WhatsApp Business accounts

## Installation

### From PyPI (Recommended)

The package is available on PyPI and can be installed using pip:

```bash
# Install the latest stable version
pip install ragazap
```

### Direct Installation from GitHub

For development or the latest version:

```bash
# Clone the repository
git clone https://github.com/jquant/whatsapp-mcp-server.git
cd whatsapp-mcp-server

# Install the package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### System Requirements

- Python 3.8 or higher
- Redis (optional, for conversation history)
- WhatsApp Business API access (for standalone mode)

## Usage

### Environment Variables

Create a `.env` file with the following variables:

```env
# Mode Configuration
STANDALONE_MODE=false  # Set to true for standalone mode

# WhatsApp API Configuration (Required in standalone mode)
META_API_VERSION=v22.0
META_APP_SECRET=your_app_secret
WHATSAPP_API_TOKEN=your_api_token
WEBHOOK_VERIFY_TOKEN=your_verify_token
BUSINESS_PHONE_NUMBER_ID=your_phone_number_id

# Server Configuration (Required in both modes)
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000

# Redis Configuration (Optional in both modes)
UPSTASH_REDIS_URL=your_redis_url
UPSTASH_REDIS_TOKEN=your_redis_token

# Optional Configuration
MAX_CONVERSATION_HISTORY_LENGTH=100
CONVERSATION_EXPIRATION_DAYS=7
LOG_LEVEL=INFO
```

### Running the Server

```bash
# Using the CLI command (if installed via pip)
ragazap

# Or directly with Python
python -m app.main
```

### API Endpoints

- Webhook: `POST /api/v1/webhook`
- MCP WebSocket: `ws://host:port/api/v1/mcp`
- Health Check: `GET /`

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Building the Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Publish to Test PyPI (for testing)
python scripts/publish_to_pypi.py --test

# Publish to PyPI
python scripts/publish_to_pypi.py
```

This will create both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.
