"""
Tropir.
"""

import sys
from loguru import logger
from .config import validate_config
from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching

def initialize():
    """
    Initialize Tropir patching for various LLM providers.
    Validates configuration before proceeding with patching.
    
    Exits program if TROPIR_API_KEY is not set.
    """
    try:
        # Validate configuration first
        validate_config()
    except ValueError as e:
        logger.error(f"Tropir initialization failed: {str(e)}")
        logger.error("Exiting program - TROPIR_API_KEY must be set to continue")
        sys.exit(1)
    
    # Only proceed with patching if validation passes
    setup_openai_patching() 
    setup_bedrock_patching()
    setup_anthropic_patching()