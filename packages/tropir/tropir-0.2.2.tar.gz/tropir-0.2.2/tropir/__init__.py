"""
Tropir.
"""

from .patching.bedrock_patch import setup_bedrock_patching
from .patching.openai_patch import setup_openai_patching

def initialize():
    setup_openai_patching() 
    setup_bedrock_patching()