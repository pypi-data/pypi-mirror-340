"""
AWS Organizations functionality for the HC MCP AWS server.
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .common import get_aws_client, OrganizationCache

logger = logging.getLogger("hc_mcp_aws")

# Input schemas for tools
class GetOrganizationStructureArguments(BaseModel):
    refresh: bool = Field(default=False, description="Force refresh the organization cache")

class ResolveAccountIdentifierArguments(BaseModel):
    identifier: str = Field(description="Account name, ID, or OU path")

# Resource URIs
ORGANIZATION_STRUCTURE_URI = "aws://account/structure"
ACCOUNT_DETAILS_URI = "aws://account/details"
ACCOUNT_ACCESS_MAP_URI = "aws://account/access-map"

# Module-level functions for direct import
def get_organization_structure(refresh: bool = False) -> Dict[str, Any]:
    """
    Retrieves the AWS organization structure, including accounts and OUs.
    Uses cached data unless refresh is specified. Uses default credentials.
    
    Args:
        refresh (bool): Force refresh the organization cache
        
    Returns:
        Dict[str, Any]: Organization structure with accounts and OUs
    """
    logger.info(f"Getting organization structure (refresh={refresh})")
    
    cache = OrganizationCache()
    if refresh:
        cache.refresh(force=True)
    else:
        cache.refresh()
    
    return {
        "accounts": list(cache.accounts.values()),
        "organizational_units": list(cache.organizational_units.values())
    }

def resolve_account_identifier(identifier: str) -> Dict[str, Any]:
    """
    Resolves an account name, ID, or OU path to account details using the Organization Cache.
    Uses default credentials to refresh cache if needed.
    
    Args:
        identifier (str): Account name, ID, or OU path
        
    Returns:
        Dict[str, Any]: Resolved account details
    """
    logger.info(f"Resolving account identifier: {identifier}")
    
    cache = OrganizationCache()
    cache.refresh()
    
    # Check if identifier is an account ID
    account = cache.get_account_by_id(identifier)
    if account:
        logger.info(f"Resolved account ID {identifier} to {account['Name']}")
        return {
            "account": account,
            "resolution_method": "account_id",
            "profile_name": f"AdministratorAccess@{account['Name'].replace(' ', '_')}"
        }
    
    # Check if identifier is an account name
    account = cache.get_account_by_name(identifier)
    if account:
        logger.info(f"Resolved account name {identifier} to {account['Id']}")
        return {
            "account": account,
            "resolution_method": "account_name",
            "profile_name": f"AdministratorAccess@{account['Name'].replace(' ', '_')}"
        }
    
    # Check if identifier is an OU path
    if identifier.startswith('/') and identifier.endswith('/'):
        accounts = cache.get_accounts_in_ou(identifier)
        if accounts:
            logger.info(f"Resolved OU path {identifier} to {len(accounts)} accounts")
            return {
                "accounts": accounts,
                "resolution_method": "ou_path",
                "ou_path": identifier
            }
    
    # No match found
    logger.warning(f"Could not resolve account identifier: {identifier}")
    return {
        "error": f"Could not resolve account identifier: {identifier}",
        "resolution_method": "none"
    }

def register_resources(server):
    """Register organization resources with the MCP server."""
    logger.info("Registering organization resources")
    
    # Register the organization structure resource
    @server.resource(ORGANIZATION_STRUCTURE_URI)
    def get_organization_structure_resource():
        """Get the AWS organization structure."""
        return get_organization_structure(refresh=False)
    
    # Register the account details resource
    @server.resource(ACCOUNT_DETAILS_URI)
    def get_account_details():
        """Get details of all AWS accounts."""
        cache = OrganizationCache()
        cache.refresh()
        
        return {
            "accounts": list(cache.accounts.values())
        }
    
    # Register the account access map resource
    @server.resource(ACCOUNT_ACCESS_MAP_URI)
    def get_account_access_map():
        """Get a map of AWS accounts and their access profiles."""
        cache = OrganizationCache()
        cache.refresh()
        
        access_map = {}
        for account_id, account in cache.accounts.items():
            profile_name = f"AdministratorAccess@{account['Name'].replace(' ', '_')}"
            access_map[account_id] = {
                "account_id": account_id,
                "account_name": account["Name"],
                "profile_name": profile_name
            }
        
        return access_map

# Tool functions for direct import
def get_organization_structure_tool(refresh: bool = False) -> Dict[str, Any]:
    """
    Retrieves the AWS organization structure, including accounts and OUs.
    Uses cached data unless refresh is specified. Uses default credentials.
    
    Args:
        refresh (bool): Force refresh the organization cache
        
    Returns:
        Dict[str, Any]: Organization structure with accounts and OUs
    """
    return get_organization_structure(refresh)

def resolve_account_identifier_tool(identifier: str) -> Dict[str, Any]:
    """
    Resolves an account name, ID, or OU path to account details using the Organization Cache.
    Uses default credentials to refresh cache if needed.
    
    Args:
        identifier (str): Account name, ID, or OU path
        
    Returns:
        Dict[str, Any]: Resolved account details
    """
    return resolve_account_identifier(identifier)

def register_tools(server):
    """Register organization tools with the MCP server."""
    logger.info("Registering organization tools")
    
    # Register the get_organization_structure tool
    server.tool("get_organization_structure", "Retrieves the AWS organization structure, including accounts and OUs.")(get_organization_structure_tool)
    
    # Register the resolve_account_identifier tool
    server.tool("resolve_account_identifier", "Resolves an account name, ID, or OU path to account details.")(resolve_account_identifier_tool)

def register_prompts(server):
    """Register organization prompts with the MCP server."""
    logger.info("Registering organization prompts")
    
    @server.prompt()
    def aws_organizations() -> str:
        """Prompt for AWS Organizations functionality."""
        return """
        # AWS Organizations
        
        The AWS Organizations service helps you centrally manage and govern your environment as you grow and scale your AWS resources. You can use AWS Organizations to create new AWS accounts, manage account access, and organize accounts to meet your budgeting, security, and compliance needs.
        
        ## Available Tools
        
        - `get_organization_structure`: Retrieves the AWS organization structure, including accounts and OUs.
        - `resolve_account_identifier`: Resolves an account name, ID, or OU path to account details.
        
        ## Available Resources
        
        - `aws://account/structure`: The organization structure with accounts and OUs.
        - `aws://account/details`: Details of all AWS accounts.
        - `aws://account/access-map`: Map of AWS accounts and their access profiles.
        
        ## Examples
        
        ```python
        # Get the organization structure
        org_structure = use_mcp_tool("aws_monitoring", "get_organization_structure", {"refresh": True})
        
        # Resolve an account identifier
        account = use_mcp_tool("aws_monitoring", "resolve_account_identifier", {"identifier": "123456789012"})
        account = use_mcp_tool("aws_monitoring", "resolve_account_identifier", {"identifier": "My Account"})
        accounts = use_mcp_tool("aws_monitoring", "resolve_account_identifier", {"identifier": "/MyOU/"})
        ```
        """
