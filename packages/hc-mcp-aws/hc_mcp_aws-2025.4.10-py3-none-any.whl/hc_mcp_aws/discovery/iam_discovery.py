"""
IAM resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_iam_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover IAM resources."""
    iam = get_aws_client('iam', profile_name=profile_name)
    
    if not resource_type or resource_type == "user":
        # Get IAM users
        response = iam.list_users()
        users = response.get('Users', [])
        
        # Limit to max_items
        users = users[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'user',
            'resources': users,
            'count': len(users)
        }
    
    elif resource_type == "role":
        # Get IAM roles
        response = iam.list_roles()
        roles = response.get('Roles', [])
        
        # Limit to max_items
        roles = roles[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'role',
            'resources': roles,
            'count': len(roles)
        }
    
    elif resource_type == "group":
        # Get IAM groups
        response = iam.list_groups()
        groups = response.get('Groups', [])
        
        # Limit to max_items
        groups = groups[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'group',
            'resources': groups,
            'count': len(groups)
        }
    
    elif resource_type == "policy":
        # Get IAM policies
        response = iam.list_policies(Scope='Local')
        policies = response.get('Policies', [])
        
        # Limit to max_items
        policies = policies[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'policy',
            'resources': policies,
            'count': len(policies)
        }
    
    else:
        # Get multiple resource types
        users_response = iam.list_users()
        roles_response = iam.list_roles()
        groups_response = iam.list_groups()
        policies_response = iam.list_policies(Scope='Local')
        
        users = users_response.get('Users', [])
        roles = roles_response.get('Roles', [])
        groups = groups_response.get('Groups', [])
        policies = policies_response.get('Policies', [])
        
        # Count resources by type
        resource_counts = {
            'user': len(users),
            'role': len(roles),
            'group': len(groups),
            'policy': len(policies)
        }
        
        return {
            'service': 'iam',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
