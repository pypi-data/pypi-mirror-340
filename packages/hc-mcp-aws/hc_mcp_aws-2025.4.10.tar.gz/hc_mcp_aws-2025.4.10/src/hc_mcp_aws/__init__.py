"""Generic MCP server initialization module for AWS monitoring.

This module provides a generic entry point for the AWS MCP server with standardized CLI arguments
for configuration and environment variable handling.
"""
import argparse
import asyncio
import importlib.metadata
import sys
from typing import Dict, List, Optional
from mcp_config_manager import add_to_config

# Import package info from metadata (single source of truth)
try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    # Fallback to version in common.py
    from .common import VERSION as __version__

# For display, convert underscores to hyphens in package name
DISPLAY_NAME = __package__.replace('_', '-')

from . import server

def main():
    """Main entry point for AWS MCP server.
    
    Provides standardized CLI arguments for:
    - Version information
    - Configuration for different MCP clients (Claude Desktop, Cline, Roo)
    - Environment variable management
    - Required environment variables listing
    """
    parser = argparse.ArgumentParser(
        prog=DISPLAY_NAME,
        description=server.__doc__ or "AWS MCP server for monitoring and management"
    )
    parser.add_argument('--version', action='version', version=f'{DISPLAY_NAME} {__version__}')
    
    # Configuration options for different MCP clients
    config_group = parser.add_argument_group('configuration')
    config_group.add_argument('--add-to-claude', action='store_true',
                          help='Add this server to Claude Desktop MCP settings and exit')
    config_group.add_argument('--add-to-cline', action='store_true',
                          help='Add this server to Cline VSCode extension settings and exit')
    config_group.add_argument('--add-to-roo', action='store_true',
                          help='Add this server to Roo VSCode extension settings and exit')
    
    # Environment variable management
    env_group = parser.add_argument_group('environment')
    env_group.add_argument('--env', action='append', nargs=1,
                        metavar='KEY=VALUE',
                        help='Environment variable to set (can be specified multiple times)')
    env_group.add_argument('--envs', action='store_true',
                        help='Print required environment variables and exit')
    
    args = parser.parse_args()

    # Define required environment variables
    REQUIRED_ENV_VARS = []

    # Print required environment variables if requested
    if args.envs:
        print("Required environment variables:")
        for var in REQUIRED_ENV_VARS:
            print(f"- {var}")
        sys.exit(0)

    # Convert env arguments to dictionary if provided
    env_vars: Optional[Dict[str, str]] = None
    if args.env:
        env_vars = {}
        for env_arg in args.env:
            try:
                key, value = env_arg[0].split('=', 1)
                env_vars[key] = value
            except ValueError:
                print(f"Error: Invalid environment variable format: {env_arg[0]}")
                print("Format should be: KEY=VALUE")
                sys.exit(1)

    # Handle configuration options
    for client_type in ['claude', 'cline', 'roo']:
        if getattr(args, f'add_to_{client_type}'):
            add_to_config(
                server_name=server.aws_server.name,
                required_env_vars=REQUIRED_ENV_VARS,
                env_vars=env_vars,
                config_type=client_type
            )
            sys.exit(0)

    # Run the server normally
    server.run_server()

__all__ = ['main', 'server']
