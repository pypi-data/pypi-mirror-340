"""
VPC resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_vpc_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover VPC resources."""
    ec2 = get_aws_client('ec2', profile_name=profile_name)
    
    if not resource_type or resource_type == "vpc":
        # Get VPCs
        response = ec2.describe_vpcs()
        vpcs = response.get('Vpcs', [])
        
        # Limit to max_items
        vpcs = vpcs[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'vpc',
            'resources': vpcs,
            'count': len(vpcs)
        }
    
    elif resource_type == "subnet":
        # Get subnets
        response = ec2.describe_subnets()
        subnets = response.get('Subnets', [])
        
        # Limit to max_items
        subnets = subnets[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'subnet',
            'resources': subnets,
            'count': len(subnets)
        }
    
    elif resource_type == "route-table":
        # Get route tables
        response = ec2.describe_route_tables()
        route_tables = response.get('RouteTables', [])
        
        # Limit to max_items
        route_tables = route_tables[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'route-table',
            'resources': route_tables,
            'count': len(route_tables)
        }
    
    else:
        # Get multiple resource types
        vpcs_response = ec2.describe_vpcs()
        subnets_response = ec2.describe_subnets()
        route_tables_response = ec2.describe_route_tables()
        
        vpcs = vpcs_response.get('Vpcs', [])
        subnets = subnets_response.get('Subnets', [])
        route_tables = route_tables_response.get('RouteTables', [])
        
        # Count resources by type
        resource_counts = {
            'vpc': len(vpcs),
            'subnet': len(subnets),
            'route-table': len(route_tables)
        }
        
        return {
            'service': 'vpc',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
