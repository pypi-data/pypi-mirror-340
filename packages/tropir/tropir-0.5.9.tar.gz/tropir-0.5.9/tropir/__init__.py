"""
Tropir.
"""

from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching

def initialize():
    setup_openai_patching() 
    setup_bedrock_patching()
    setup_anthropic_patching()