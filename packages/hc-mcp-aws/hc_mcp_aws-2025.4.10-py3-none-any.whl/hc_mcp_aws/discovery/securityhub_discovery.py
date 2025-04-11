"""
SecurityHub resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_securityhub_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover Security Hub resources."""
    securityhub = get_aws_client('securityhub', profile_name=profile_name)
    
    if not resource_type or resource_type == "finding":
        # Get Security Hub findings
        filters = {
            "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]
        }
        
        response = securityhub.get_findings(
            Filters=filters,
            MaxResults=max_items
        )
        
        findings = response.get('Findings', [])
        
        return {
            'service': 'securityhub',
            'resourceType': 'finding',
            'resources': findings,
            'count': len(findings)
        }
    
    elif resource_type == "insight":
        # Get Security Hub insights
        response = securityhub.get_insights(MaxResults=max_items)
        insights = response.get('Insights', [])
        
        return {
            'service': 'securityhub',
            'resourceType': 'insight',
            'resources': insights,
            'count': len(insights)
        }
    
    else:
        # Get multiple resource types
        findings_response = securityhub.get_findings(
            Filters={"RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]},
            MaxResults=1
        )
        
        insights_response = securityhub.get_insights(MaxResults=1)
        
        findings_count = len(findings_response.get('Findings', []))
        insights_count = len(insights_response.get('Insights', []))
        
        # Get enabled standards
        try:
            standards_response = securityhub.get_enabled_standards()
            standards_count = len(standards_response.get('StandardsSubscriptions', []))
        except Exception:
            standards_count = 0
        
        # Count resources by type
        resource_counts = {
            'finding': findings_count,
            'insight': insights_count,
            'standard': standards_count
        }
        
        return {
            'service': 'securityhub',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
