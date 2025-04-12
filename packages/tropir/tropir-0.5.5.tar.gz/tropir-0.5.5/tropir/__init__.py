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


def initialize():
    """
    Initialize Tropir patching for various LLM providers.
    """
    def run_patching():
        logger.info("Starting background patching of LLM providers...")
        setup_openai_patching() 
        setup_bedrock_patching()
        setup_anthropic_patching()
        logger.info("Background patching complete")
    
    patching_thread = threading.Thread(target=run_patching, daemon=True)
    patching_thread.start()
    logger.info("Tropir initialization complete - patching running in background")