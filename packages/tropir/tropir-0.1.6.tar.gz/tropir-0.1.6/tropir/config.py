"""
Configuration settings for the Tropir Agent.
"""

import os

# API configuration
DEFAULT_API_URL = "https://tropir.fly.dev/api/log"
LOCAL_API_URL = "http://0.0.0.0:8080/api/log"

# Default configuration
DEFAULTS = {
    "enabled": True,
    "api_url": DEFAULT_API_URL,
}

def get_config():
    """
    Get configuration from environment variables or defaults.
    """
    is_local = os.getenv("TROPIR_LOCAL", "0") == "1"
    api_url = LOCAL_API_URL if is_local else DEFAULT_API_URL
    
    return {
        "enabled": os.getenv("TROPIR_ENABLED", "1") == "1",
        "api_url": os.getenv("TROPIR_API_URL", api_url),
        "api_key": os.getenv("TROPIR_API_KEY"),
        "local": is_local,
    } 