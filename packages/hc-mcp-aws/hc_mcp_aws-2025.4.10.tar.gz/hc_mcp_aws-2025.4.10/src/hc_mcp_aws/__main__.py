"""
Main entry point for the HC MCP AWS server.
This module simply imports and calls the main function from the package.
"""
import sys
from . import main

if __name__ == "__main__":
    sys.exit(main())
