"""
Lambda resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_lambda_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover Lambda resources."""
    lambda_client = get_aws_client('lambda', profile_name=profile_name)
    
    if not resource_type or resource_type == "function":
        # Get Lambda functions
        response = lambda_client.list_functions(MaxItems=max_items)
        functions = response.get('Functions', [])
        
        # Extract key information
        function_info = []
        for function in functions:
            function_info.append({
                'FunctionName': function.get('FunctionName'),
                'Runtime': function.get('Runtime'),
                'Handler': function.get('Handler'),
                'CodeSize': function.get('CodeSize'),
                'Description': function.get('Description'),
                'Timeout': function.get('Timeout'),
                'MemorySize': function.get('MemorySize'),
                'LastModified': function.get('LastModified'),
                'Role': function.get('Role'),
                'Environment': function.get('Environment'),
                'TracingConfig': function.get('TracingConfig'),
                'RevisionId': function.get('RevisionId')
            })
        
        return {
            'service': 'lambda',
            'resourceType': 'function',
            'resources': function_info,
            'count': len(function_info)
        }
    
    else:
        # Get functions
        response = lambda_client.list_functions()
        functions = response.get('Functions', [])
        
        return {
            'service': 'lambda',
            'resourceCounts': {
                'function': len(functions)
            },
            'totalCount': len(functions),
            'availableTypes': ['function']
        }
