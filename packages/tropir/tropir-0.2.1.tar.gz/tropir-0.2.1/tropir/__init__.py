"""
Tropir.
"""

from .openai_patch import setup_openai_patching

def initialize():
    setup_openai_patching() 