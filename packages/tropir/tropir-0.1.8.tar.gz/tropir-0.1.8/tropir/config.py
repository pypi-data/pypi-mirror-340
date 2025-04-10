"""
Configuration settings for the Tropir Agent.
"""

import os

# API configuration
DEFAULT_API_URL = "https://tropir.fly.dev/api/log"

# Default configuration
DEFAULTS = {
    "enabled": True,
    "api_url": DEFAULT_API_URL,
}

def get_config():
    """
    Get configuration from environment variables or defaults.
    """
    return {
        "enabled": os.getenv("TROPIR_ENABLED", "1") == "1",
        "api_url": os.getenv("TROPIR_API_URL", DEFAULT_API_URL),
        "api_key": os.getenv("TROPIR_API_KEY"),
        "local": os.getenv("TROPIR_LOCAL", "0") == "1",
    } 