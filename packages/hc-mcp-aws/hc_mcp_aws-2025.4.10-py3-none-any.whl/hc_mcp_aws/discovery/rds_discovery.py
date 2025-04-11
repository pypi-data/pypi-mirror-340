"""
RDS resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_rds_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover RDS resources."""
    rds = get_aws_client('rds', profile_name=profile_name)
    
    if not resource_type or resource_type == "db-instance":
        # Get RDS instances
        response = rds.describe_db_instances()
        instances = response.get('DBInstances', [])
        
        # Limit to max_items
        instances = instances[:max_items]
        
        return {
            'service': 'rds',
            'resourceType': 'db-instance',
            'resources': instances,
            'count': len(instances)
        }
    
    elif resource_type == "db-cluster":
        # Get RDS clusters
        response = rds.describe_db_clusters()
        clusters = response.get('DBClusters', [])
        
        # Limit to max_items
        clusters = clusters[:max_items]
        
        return {
            'service': 'rds',
            'resourceType': 'db-cluster',
            'resources': clusters,
            'count': len(clusters)
        }
    
    else:
        # Get multiple resource types
        instances_response = rds.describe_db_instances()
        clusters_response = rds.describe_db_clusters()
        
        instances = instances_response.get('DBInstances', [])
        clusters = clusters_response.get('DBClusters', [])
        
        # Count resources by type
        resource_counts = {
            'db-instance': len(instances),
            'db-cluster': len(clusters)
        }
        
        return {
            'service': 'rds',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
