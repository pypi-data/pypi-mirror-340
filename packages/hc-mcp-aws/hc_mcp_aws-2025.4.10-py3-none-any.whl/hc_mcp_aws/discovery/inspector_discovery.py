"""
Inspector resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_inspector_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover Inspector resources."""
    inspector = get_aws_client('inspector2', profile_name=profile_name)
    
    if not resource_type or resource_type == "finding":
        # Get Inspector findings
        filter_criteria = {
            "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
        }
        
        response = inspector.list_findings(
            filterCriteria=filter_criteria,
            maxResults=max_items
        )
        
        finding_arns = response.get('findingArns', [])
        
        if finding_arns:
            # Get detailed findings
            findings_response = inspector.batch_get_findings(
                findingArns=finding_arns
            )
            
            findings = findings_response.get('findings', [])
        else:
            findings = []
        
        return {
            'service': 'inspector2',
            'resourceType': 'finding',
            'resources': findings,
            'count': len(findings)
        }
    
    else:
        # Get findings count
        filter_criteria = {
            "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
        }
        
        response = inspector.list_findings(
            filterCriteria=filter_criteria,
            maxResults=1
        )
        
        finding_arns = response.get('findingArns', [])
        
        # Count resources by type
        resource_counts = {
            'finding': len(finding_arns)
        }
        
        return {
            'service': 'inspector2',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
