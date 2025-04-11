"""
WAF resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_waf_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover WAF resources."""
    wafv2 = get_aws_client('wafv2', profile_name=profile_name)
    
    if not resource_type or resource_type == "web-acl":
        # Get WAF Web ACLs (both regional and CloudFront)
        regional_response = wafv2.list_web_acls(Scope='REGIONAL')
        cloudfront_response = wafv2.list_web_acls(Scope='CLOUDFRONT')
        
        regional_web_acls = regional_response.get('WebACLs', [])
        cloudfront_web_acls = cloudfront_response.get('WebACLs', [])
        
        # Add scope information
        for web_acl in regional_web_acls:
            web_acl['Scope'] = 'REGIONAL'
        
        for web_acl in cloudfront_web_acls:
            web_acl['Scope'] = 'CLOUDFRONT'
        
        # Combine and limit to max_items
        web_acls = regional_web_acls + cloudfront_web_acls
        web_acls = web_acls[:max_items]
        
        return {
            'service': 'wafv2',
            'resourceType': 'web-acl',
            'resources': web_acls,
            'count': len(web_acls)
        }
    
    elif resource_type == "ip-set":
        # Get WAF IP sets (both regional and CloudFront)
        regional_response = wafv2.list_ip_sets(Scope='REGIONAL')
        cloudfront_response = wafv2.list_ip_sets(Scope='CLOUDFRONT')
        
        regional_ip_sets = regional_response.get('IPSets', [])
        cloudfront_ip_sets = cloudfront_response.get('IPSets', [])
        
        # Add scope information
        for ip_set in regional_ip_sets:
            ip_set['Scope'] = 'REGIONAL'
        
        for ip_set in cloudfront_ip_sets:
            ip_set['Scope'] = 'CLOUDFRONT'
        
        # Combine and limit to max_items
        ip_sets = regional_ip_sets + cloudfront_ip_sets
        ip_sets = ip_sets[:max_items]
        
        return {
            'service': 'wafv2',
            'resourceType': 'ip-set',
            'resources': ip_sets,
            'count': len(ip_sets)
        }
    
    elif resource_type == "rule-group":
        # Get WAF rule groups (both regional and CloudFront)
        regional_response = wafv2.list_rule_groups(Scope='REGIONAL')
        cloudfront_response = wafv2.list_rule_groups(Scope='CLOUDFRONT')
        
        regional_rule_groups = regional_response.get('RuleGroups', [])
        cloudfront_rule_groups = cloudfront_response.get('RuleGroups', [])
        
        # Add scope information
        for rule_group in regional_rule_groups:
            rule_group['Scope'] = 'REGIONAL'
        
        for rule_group in cloudfront_rule_groups:
            rule_group['Scope'] = 'CLOUDFRONT'
        
        # Combine and limit to max_items
        rule_groups = regional_rule_groups + cloudfront_rule_groups
        rule_groups = rule_groups[:max_items]
        
        return {
            'service': 'wafv2',
            'resourceType': 'rule-group',
            'resources': rule_groups,
            'count': len(rule_groups)
        }
    
    else:
        # Get multiple resource types
        regional_web_acls_response = wafv2.list_web_acls(Scope='REGIONAL')
        cloudfront_web_acls_response = wafv2.list_web_acls(Scope='CLOUDFRONT')
        regional_ip_sets_response = wafv2.list_ip_sets(Scope='REGIONAL')
        cloudfront_ip_sets_response = wafv2.list_ip_sets(Scope='CLOUDFRONT')
        regional_rule_groups_response = wafv2.list_rule_groups(Scope='REGIONAL')
        cloudfront_rule_groups_response = wafv2.list_rule_groups(Scope='CLOUDFRONT')
        
        regional_web_acls = regional_web_acls_response.get('WebACLs', [])
        cloudfront_web_acls = cloudfront_web_acls_response.get('WebACLs', [])
        regional_ip_sets = regional_ip_sets_response.get('IPSets', [])
        cloudfront_ip_sets = cloudfront_ip_sets_response.get('IPSets', [])
        regional_rule_groups = regional_rule_groups_response.get('RuleGroups', [])
        cloudfront_rule_groups = cloudfront_rule_groups_response.get('RuleGroups', [])
        
        # Count resources by type
        resource_counts = {
            'web-acl': len(regional_web_acls) + len(cloudfront_web_acls),
            'ip-set': len(regional_ip_sets) + len(cloudfront_ip_sets),
            'rule-group': len(regional_rule_groups) + len(cloudfront_rule_groups)
        }
        
        return {
            'service': 'wafv2',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
