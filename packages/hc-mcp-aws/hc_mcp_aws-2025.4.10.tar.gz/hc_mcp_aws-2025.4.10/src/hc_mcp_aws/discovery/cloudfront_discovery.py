"""
CloudFront resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_cloudfront_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover CloudFront resources."""
    cloudfront = get_aws_client('cloudfront', profile_name=profile_name)
    
    if not resource_type or resource_type == "distribution":
        # Get CloudFront distributions
        response = cloudfront.list_distributions()
        distribution_list = response.get('DistributionList', {})
        distributions = distribution_list.get('Items', [])
        
        # Limit to max_items
        distributions = distributions[:max_items]
        
        return {
            'service': 'cloudfront',
            'resourceType': 'distribution',
            'resources': distributions,
            'count': len(distributions)
        }
    
    elif resource_type == "origin-access-identity":
        # Get CloudFront origin access identities
        response = cloudfront.list_cloud_front_origin_access_identities()
        oai_list = response.get('CloudFrontOriginAccessIdentityList', {})
        oais = oai_list.get('Items', [])
        
        # Limit to max_items
        oais = oais[:max_items]
        
        return {
            'service': 'cloudfront',
            'resourceType': 'origin-access-identity',
            'resources': oais,
            'count': len(oais)
        }
    
    elif resource_type == "function":
        # Get CloudFront functions
        response = cloudfront.list_functions()
        function_list = response.get('FunctionList', {})
        functions = function_list.get('Items', [])
        
        # Limit to max_items
        functions = functions[:max_items]
        
        return {
            'service': 'cloudfront',
            'resourceType': 'function',
            'resources': functions,
            'count': len(functions)
        }
    
    else:
        # Get multiple resource types
        distributions_response = cloudfront.list_distributions()
        oai_response = cloudfront.list_cloud_front_origin_access_identities()
        functions_response = cloudfront.list_functions()
        
        distribution_list = distributions_response.get('DistributionList', {})
        oai_list = oai_response.get('CloudFrontOriginAccessIdentityList', {})
        function_list = functions_response.get('FunctionList', {})
        
        distributions = distribution_list.get('Items', [])
        oais = oai_list.get('Items', [])
        functions = function_list.get('Items', [])
        
        # Count resources by type
        resource_counts = {
            'distribution': len(distributions),
            'origin-access-identity': len(oais),
            'function': len(functions)
        }
        
        return {
            'service': 'cloudfront',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
