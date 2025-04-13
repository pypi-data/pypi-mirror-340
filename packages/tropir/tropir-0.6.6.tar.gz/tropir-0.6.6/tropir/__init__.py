"""
Tropir.
"""

from .bedrock_patch import setup_bedrock_patching
from .openai_patch import setup_openai_patching
from .anthropic_patch import setup_anthropic_patching
import os
import sys

def initialize():
    # Load only TROPIR_API_KEY from .env file if available
    try:
        import re
        from pathlib import Path
        
        # Only load if not already set
        if not os.environ.get("TROPIR_API_KEY"):
            env_path = Path('.env')
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Look for TROPIR_API_KEY specifically
                            if match := re.match(r'^TROPIR_API_KEY\s*=\s*(.*)$', line):
                                value = match.group(1).strip()
                                # Remove quotes if present
                                if (value[0] == value[-1] == '"' or value[0] == value[-1] == "'"):
                                    value = value[1:-1]
                                os.environ["TROPIR_API_KEY"] = value
                                print("Successfully loaded TROPIR_API_KEY from environment variables.")
                                break
    except Exception as e:
        print(f"Warning: Could not load TROPIR_API_KEY: {e}")
    
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