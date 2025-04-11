"""
Route53 resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_route53_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover Route53 resources."""
    route53 = get_aws_client('route53', profile_name=profile_name)
    
    if not resource_type or resource_type == "hosted-zone":
        # Get Route53 hosted zones
        response = route53.list_hosted_zones()
        hosted_zones = response.get('HostedZones', [])
        
        # Limit to max_items
        hosted_zones = hosted_zones[:max_items]
        
        # Get record sets for each hosted zone
        for zone in hosted_zones:
            zone_id = zone.get('Id')
            if zone_id:
                try:
                    # Strip '/hostedzone/' prefix from zone ID
                    if zone_id.startswith('/hostedzone/'):
                        zone_id = zone_id[12:]
                    
                    # Get record sets
                    record_sets_response = route53.list_resource_record_sets(HostedZoneId=zone_id)
                    record_sets = record_sets_response.get('ResourceRecordSets', [])
                    
                    # Add record sets to zone
                    zone['ResourceRecordSets'] = record_sets[:10]  # Limit to 10 records per zone
                    zone['ResourceRecordSetCount'] = len(record_sets)
                except Exception as e:
                    logger.warning(f"Error getting record sets for zone {zone_id}: {str(e)}")
                    zone['Error'] = str(e)
        
        return {
            'service': 'route53',
            'resourceType': 'hosted-zone',
            'resources': hosted_zones,
            'count': len(hosted_zones)
        }
    
    elif resource_type == "health-check":
        # Get Route53 health checks
        response = route53.list_health_checks()
        health_checks = response.get('HealthChecks', [])
        
        # Limit to max_items
        health_checks = health_checks[:max_items]
        
        return {
            'service': 'route53',
            'resourceType': 'health-check',
            'resources': health_checks,
            'count': len(health_checks)
        }
    
    elif resource_type == "domain":
        # Get Route53 domains
        route53domains = get_aws_client('route53domains', profile_name=profile_name)
        response = route53domains.list_domains()
        domains = response.get('Domains', [])
        
        # Limit to max_items
        domains = domains[:max_items]
        
        return {
            'service': 'route53',
            'resourceType': 'domain',
            'resources': domains,
            'count': len(domains)
        }
    
    else:
        # Get multiple resource types
        hosted_zones_response = route53.list_hosted_zones()
        health_checks_response = route53.list_health_checks()
        
        hosted_zones = hosted_zones_response.get('HostedZones', [])
        health_checks = health_checks_response.get('HealthChecks', [])
        
        # Try to get domains if route53domains is available
        try:
            route53domains = get_aws_client('route53domains', profile_name=profile_name)
            domains_response = route53domains.list_domains()
            domains = domains_response.get('Domains', [])
        except Exception:
            domains = []
        
        # Count resources by type
        resource_counts = {
            'hosted-zone': len(hosted_zones),
            'health-check': len(health_checks),
            'domain': len(domains)
        }
        
        return {
            'service': 'route53',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
