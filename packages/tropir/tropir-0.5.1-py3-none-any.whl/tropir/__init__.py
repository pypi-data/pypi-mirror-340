"""
Tropir.
"""

import sys
import threading
import os
from pathlib import Path
from loguru import logger
from .config import validate_config
from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching
from .utils import get_user_id

def _ensure_env_vars():
    """
    Ensure environment variables are loaded from .env files
    in common locations if they're not already set.
    """
    try:
        from dotenv import load_dotenv
        
        # Try to load from common .env locations if API key isn't set
        if not os.getenv("TROPIR_API_KEY"):
            # Try current directory
            load_dotenv()
            
            # Try parent directories (up to 3 levels)
            current = Path.cwd()
            for _ in range(3):
                parent = current.parent
                env_file = parent / ".env"
                if env_file.exists():
                    load_dotenv(env_file)
                    if os.getenv("TROPIR_API_KEY"):
                        logger.info(f"Loaded API key from {env_file}")
                        break
                current = parent
                
        # Debug information
        if os.getenv("TROPIR_API_KEY"):
            logger.debug("TROPIR_API_KEY is set in environment")
        else:
            logger.debug("TROPIR_API_KEY not found in environment or .env files")
            
    except ImportError:
        logger.debug("python-dotenv not installed, skipping .env file loading")

def initialize():
    """
    Initialize Tropir patching for various LLM providers.
    Validates configuration before proceeding with patching.
    
    Exits program if TROPIR_API_KEY is not set or invalid.
    """
    # Ensure environment variables are loaded
    _ensure_env_vars()
    
    try:
        # Validate configuration first - this runs synchronously
        validate_config()
        
        # Check if the API key is valid by trying to get the user_id
        try:
            get_user_id()
        except ValueError as e:
            logger.error(f"Tropir initialization failed: {str(e)}")
            logger.error("Exiting program - Invalid TROPIR_API_KEY")
            sys.exit(1)
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