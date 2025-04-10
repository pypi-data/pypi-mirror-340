# TradeVPS Python Client

The official Python client for TradeVPS APIs.

## Installation

```bash
pip install tradevps
```

## Quick Start

```python
from tradevps import Client
from tradevps.exceptions import AuthenticationError, APIError

# Initialize client
client = Client()

# Method 1: Login with email/password
try:
    auth = client.login("your-email@example.com", "your-password")
    print(f"Logged in as: {auth.user.name}")
    
    # Token is automatically set after login
    # You can also set it manually:
    client.set_api_key(auth.token)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")

# Method 2: Initialize with API key directly
client = Client(api_key="your-api-key")

# Handle API errors
try:
    # Your API calls here
    pass
except APIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
```

## Development

1. Clone the repository
2. Install dependencies: `pdm install`
3. Run tests: `pdm run pytest`

## License

MIT License
