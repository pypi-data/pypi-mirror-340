"""
CloudWatch resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_cloudwatch_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover CloudWatch resources."""
    cloudwatch = get_aws_client('cloudwatch', profile_name=profile_name)
    logs = get_aws_client('logs', profile_name=profile_name)
    
    if not resource_type or resource_type == "dashboard":
        # Get CloudWatch dashboards
        response = cloudwatch.list_dashboards()
        dashboards = response.get('DashboardEntries', [])
        
        # Limit to max_items
        dashboards = dashboards[:max_items]
        
        return {
            'service': 'cloudwatch',
            'resourceType': 'dashboard',
            'resources': dashboards,
            'count': len(dashboards)
        }
    
    elif resource_type == "alarm":
        # Get CloudWatch alarms
        response = cloudwatch.describe_alarms(MaxRecords=max_items)
        alarms = response.get('MetricAlarms', [])
        composite_alarms = response.get('CompositeAlarms', [])
        
        return {
            'service': 'cloudwatch',
            'resourceType': 'alarm',
            'resources': {
                'metricAlarms': alarms,
                'compositeAlarms': composite_alarms
            },
            'count': len(alarms) + len(composite_alarms)
        }
    
    elif resource_type == "log-group":
        # Get CloudWatch log groups
        response = logs.describe_log_groups(limit=max_items)
        log_groups = response.get('logGroups', [])
        
        return {
            'service': 'cloudwatch',
            'resourceType': 'log-group',
            'resources': log_groups,
            'count': len(log_groups)
        }
    
    else:
        # Get multiple resource types
        dashboards_response = cloudwatch.list_dashboards()
        alarms_response = cloudwatch.describe_alarms()
        log_groups_response = logs.describe_log_groups()
        
        dashboards = dashboards_response.get('DashboardEntries', [])
        metric_alarms = alarms_response.get('MetricAlarms', [])
        composite_alarms = alarms_response.get('CompositeAlarms', [])
        log_groups = log_groups_response.get('logGroups', [])
        
        # Count resources by type
        resource_counts = {
            'dashboard': len(dashboards),
            'alarm': len(metric_alarms) + len(composite_alarms),
            'log-group': len(log_groups)
        }
        
        return {
            'service': 'cloudwatch',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
