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
    "api_url": DEFAULT_API_URL + "api/log",
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