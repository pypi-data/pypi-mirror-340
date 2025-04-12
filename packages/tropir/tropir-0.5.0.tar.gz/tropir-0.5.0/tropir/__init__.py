"""
Tropir.
"""

import sys
import threading
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
        # Validate configuration first - this runs synchronously
        validate_config()
    except ValueError as e:
        logger.error(f"Tropir initialization failed: {str(e)}")
        logger.error("Exiting program - TROPIR_API_KEY must be set to continue")
        sys.exit(1)
    
    # Run patching in a background thread to not block main execution
    def run_patching():
        logger.info("Starting background patching of LLM providers...")
        setup_openai_patching() 
        setup_bedrock_patching()
        setup_anthropic_patching()
        logger.info("Background patching complete")
    
    patching_thread = threading.Thread(target=run_patching, daemon=True)
    patching_thread.start()
    logger.info("Tropir initialization complete - patching running in background")