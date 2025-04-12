"""
Tropir.
"""

from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching
import os
import sys

def initialize():
    # Create a fancy terminal message
    terminal_width = os.get_terminal_size().columns
    message = "TROPIR ENABLED"
    padding_len = (terminal_width - len(message) - 4) // 2
    
    # Color codes for cyan/green theme
    cyan = "\033[1;36m"      # Bright cyan
    green = "\033[1;32m"     # Bright green
    bold_white = "\033[1;37m"
    reset = "\033[0m"
    
    # Create padding with the cyan color
    padding = cyan + "=" * padding_len + reset
    
    # Print the fancy message with the green message
    print(padding + bold_white + "[ " + green + message + bold_white + " ]" + padding)
    
    setup_openai_patching() 
    setup_bedrock_patching()
    setup_anthropic_patching()