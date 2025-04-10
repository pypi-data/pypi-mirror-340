"""
Command-line interface for the Tropir Agent.
"""

import os
import sys
import importlib.util
import runpy
import argparse

from . import initialize


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Tropir Agent CLI")
    parser.add_argument('command', help='Command to run with Tropir agent enabled')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command')
    
    args = parser.parse_args()
    
    # Enable Tropir tracking
    os.environ["TROPIR_ENABLED"] = "1"
    
    # Initialize the agent
    initialize()
    
    # Run the command
    if args.command == "python":
        if len(args.args) > 0:
            if args.args[0] == "-m":
                # Handle module execution
                if len(args.args) > 1:
                    module_name = args.args[1]
                    sys.argv = [args.args[0]] + args.args[1:]
                    runpy.run_module(module_name, run_name="__main__")
                else:
                    print("Missing module name")
                    sys.exit(1)
            else:
                # Handle script execution
                script_path = args.args[0]
                sys.argv = args.args
                runpy.run_path(script_path, run_name="__main__")
        else:
            print("Missing python script or module")
            sys.exit(1)
    else:
        print(f"Unsupported command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 