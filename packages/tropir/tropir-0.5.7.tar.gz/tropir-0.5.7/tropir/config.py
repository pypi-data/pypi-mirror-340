"""
Configuration settings for the Tropir Agent.
"""

import os

# API configuration
DEFAULT_API_URL = "https://traceback-production.up.railway.app/"
DEFAULT_LOCAL_URL = "http://localhost:8080/"

# Default configuration
DEFAULTS = {
    "enabled": True,
    "api_url": DEFAULT_API_URL + "log",
}

def get_config():
    """
    Get configuration from environment variables or defaults.
    """
    return {
        "enabled": os.getenv("TROPIR_ENABLED", "1") == "1",
        "api_url": os.getenv("TROPIR_API_URL", DEFAULT_API_URL) + "api/log",
        "api_key": os.getenv("TROPIR_API_KEY"),
        "local": os.getenv("TROPIR_LOCAL", "0") == "1",
    } 

def validate_config():
    """
    Validate that the required configuration is present.
    
    Raises:
        ValueError: If TROPIR_API_KEY is not set
    """
    config = get_config()
    if not config["api_key"]:
        raise ValueError("TROPIR_API_KEY environment variable not set. Operations aborted.")
    return config 