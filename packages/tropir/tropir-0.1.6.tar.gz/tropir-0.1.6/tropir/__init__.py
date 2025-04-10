"""
Tropir.
"""

from .wrapper import patch_openai

def initialize():
    patch_openai() 