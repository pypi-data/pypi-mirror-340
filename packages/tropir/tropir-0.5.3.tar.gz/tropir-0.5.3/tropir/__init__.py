"""
Tropir.
"""

import sys
import threading
import os
from pathlib import Path
from loguru import logger
from .utils import get_user_id
from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching

def _ensure_env_vars():
    """
    Ensure environment variables are loaded from .env files
    in common locations.
    """
    try:
        from dotenv import load_dotenv
        
        # Try to load from common .env locations
        # Try current directory
        load_dotenv()
        
        # Try parent directories (up to 3 levels)
        current = Path.cwd()
        for _ in range(3):
            parent = current.parent
            env_file = parent / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                break
            current = parent
            
    except ImportError:
        logger.debug("python-dotenv not installed, skipping .env file loading")

def initialize():
    """
    Initialize Tropir patching for various LLM providers.
    
    Exits program if TROPIR_API_KEY is invalid.
    """
    # Ensure environment variables are loaded
    _ensure_env_vars()
    
    try:
        # Check if the API key is valid by trying to get the user_id
        get_user_id()
    except ValueError as e:
        logger.error(f"Tropir initialization failed: {str(e)}")
        logger.error("Exiting program - Invalid TROPIR_API_KEY")
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