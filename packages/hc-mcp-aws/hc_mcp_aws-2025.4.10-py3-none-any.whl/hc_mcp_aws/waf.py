"""
AWS WAF functionality for the HC MCP AWS server.
"""
import logging
import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .common import get_aws_client
from .organization import resolve_account_identifier

logger = logging.getLogger("hc_mcp_aws")

# Input schemas for tools
class ListWafWebAclsArguments(BaseModel):
    scope: str = Field(default="REGIONAL", description="The scope of the Web ACLs to retrieve. Valid values: 'REGIONAL' or 'CLOUDFRONT'")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetWafWebAclDetailsArguments(BaseModel):
    web_acl_id: str = Field(description="The ID of the Web ACL to retrieve")
    web_acl_name: str = Field(description="The name of the Web ACL to retrieve")
    scope: str = Field(default="REGIONAL", description="The scope of the Web ACL. Valid values: 'REGIONAL' or 'CLOUDFRONT'")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetWafSampledRequestsArguments(BaseModel):
    web_acl_id: str = Field(description="The ID of the Web ACL")
    web_acl_name: str = Field(description="The name of the Web ACL")
    scope: str = Field(default="REGIONAL", description="The scope of the Web ACL. Valid values: 'REGIONAL' or 'CLOUDFRONT'")
    rule_name: Optional[str] = Field(default=None, description="Filter requests by a specific rule name")
    max_items: int = Field(default=100, description="Maximum number of requests to return")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetWafIpSetsArguments(BaseModel):
    scope: str = Field(default="REGIONAL", description="The scope of the IP sets to retrieve. Valid values: 'REGIONAL' or 'CLOUDFRONT'")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetWafMetricsArguments(BaseModel):
    web_acl_name: str = Field(description="The name of the Web ACL")
    days: int = Field(default=1, description="Number of days of metrics to retrieve")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

# Module-level functions for direct import
def list_waf_web_acls(scope: str = "REGIONAL", account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all AWS WAF Web ACLs in the specified scope.
    
    Args:
        scope (str): The scope of the Web ACLs to retrieve. Valid values: "REGIONAL" or "CLOUDFRONT".
        account_identifier (str, optional): AWS account ID, name, or OU path.
        
    Returns:
        Dictionary with Web ACL information or an error message.
    """
    logger.info(f"Listing WAF Web ACLs with scope: {scope} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Validate scope
        if scope not in ["REGIONAL", "CLOUDFRONT"]:
            return {"error": "Invalid scope. Valid values are 'REGIONAL' or 'CLOUDFRONT'"}
        
        # Get WAFv2 client
        wafv2 = get_aws_client('wafv2', profile_name=profile_name)
        
        # List Web ACLs
        response = wafv2.list_web_acls(Scope=scope)
        web_acls = response.get('WebACLs', [])
        
        # Get associated resources for each Web ACL
        for web_acl in web_acls:
            try:
                resources_response = wafv2.list_resources_for_web_acl(
                    WebACLArn=web_acl['ARN'],
                    ResourceType='APPLICATION_LOAD_BALANCER' if scope == 'REGIONAL' else 'CLOUDFRONT'
                )
                web_acl['AssociatedResources'] = resources_response.get('ResourceArns', [])
            except Exception as e:
                logger.warning(f"Error getting associated resources for Web ACL {web_acl['Name']}: {str(e)}")
                web_acl['AssociatedResources'] = []
        
        return {
            'webAcls': web_acls,
            'count': len(web_acls),
            'scope': scope
        }
    except Exception as e:
        error_msg = f"Error listing WAF Web ACLs: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_waf_web_acl_details(
    web_acl_id: str, 
    web_acl_name: str, 
    scope: str = "REGIONAL", 
    account_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gets detailed information about a specific AWS WAF Web ACL, including its rules.
    
    Args:
        web_acl_id (str): The ID of the Web ACL to retrieve.
        web_acl_name (str): The name of the Web ACL to retrieve.
        scope (str): The scope of the Web ACL. Valid values: "REGIONAL" or "CLOUDFRONT".
        account_identifier (str, optional): AWS account ID, name, or OU path.
        
    Returns:
        Dictionary with detailed Web ACL information or an error message.
    """
    logger.info(f"Getting WAF Web ACL details for {web_acl_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Validate scope
        if scope not in ["REGIONAL", "CLOUDFRONT"]:
            return {"error": "Invalid scope. Valid values are 'REGIONAL' or 'CLOUDFRONT'"}
        
        # Get WAFv2 client
        wafv2 = get_aws_client('wafv2', profile_name=profile_name)
        
        # Get Web ACL details
        response = wafv2.get_web_acl(
            Name=web_acl_name,
            Id=web_acl_id,
            Scope=scope
        )
        
        web_acl = response.get('WebACL', {})
        
        # Get associated resources
        try:
            resources_response = wafv2.list_resources_for_web_acl(
                WebACLArn=web_acl['ARN'],
                ResourceType='APPLICATION_LOAD_BALANCER' if scope == 'REGIONAL' else 'CLOUDFRONT'
            )
            web_acl['AssociatedResources'] = resources_response.get('ResourceArns', [])
        except Exception as e:
            logger.warning(f"Error getting associated resources for Web ACL {web_acl_name}: {str(e)}")
            web_acl['AssociatedResources'] = []
        
        # Extract rules
        rules = web_acl.get('Rules', [])
        
        # Group rules by action
        rule_actions = {}
        for rule in rules:
            action = "Unknown"
            
            # Check for standard actions
            if 'Action' in rule:
                for action_type in ['Allow', 'Block', 'Count']:
                    if action_type.lower() in rule['Action']:
                        action = action_type
                        break
            
            # Check for override actions in rule group references
            if 'OverrideAction' in rule:
                for action_type in ['None', 'Count']:
                    if action_type.lower() in rule['OverrideAction']:
                        action = f"RuleGroup-{action_type}"
                        break
            
            if action not in rule_actions:
                rule_actions[action] = []
            
            rule_actions[action].append(rule)
        
        # Extract logging configuration if available
        logging_config = None
        try:
            logging_response = wafv2.get_logging_configuration(
                ResourceArn=web_acl['ARN']
            )
            logging_config = logging_response.get('LoggingConfiguration')
        except Exception as e:
            logger.warning(f"Error getting logging configuration for Web ACL {web_acl_name}: {str(e)}")
        
        return {
            'webAcl': web_acl,
            'rules': rules,
            'ruleCount': len(rules),
            'ruleActions': {action: len(rules) for action, rules in rule_actions.items()},
            'loggingConfiguration': logging_config,
            'scope': scope
        }
    except Exception as e:
        error_msg = f"Error getting WAF Web ACL details: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_waf_sampled_requests(
    web_acl_id: str, 
    web_acl_name: str, 
    scope: str = "REGIONAL", 
    rule_name: Optional[str] = None, 
    max_items: int = 100, 
    account_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gets sampled web requests that were inspected by a specific AWS WAF Web ACL.
    
    Args:
        web_acl_id (str): The ID of the Web ACL.
        web_acl_name (str): The name of the Web ACL.
        scope (str): The scope of the Web ACL. Valid values: "REGIONAL" or "CLOUDFRONT".
        rule_name (str, optional): Filter requests by a specific rule name.
        max_items (int): Maximum number of requests to return (default: 100).
        account_identifier (str, optional): AWS account ID, name, or OU path.
        
    Returns:
        Dictionary with sampled web requests or an error message.
    """
    logger.info(f"Getting WAF sampled requests for {web_acl_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Validate scope
        if scope not in ["REGIONAL", "CLOUDFRONT"]:
            return {"error": "Invalid scope. Valid values are 'REGIONAL' or 'CLOUDFRONT'"}
        
        # Get WAFv2 client
        wafv2 = get_aws_client('wafv2', profile_name=profile_name)
        
        # Get Web ACL ARN
        web_acl_response = wafv2.get_web_acl(
            Name=web_acl_name,
            Id=web_acl_id,
            Scope=scope
        )
        
        web_acl = web_acl_response.get('WebACL', {})
        web_acl_arn = web_acl.get('ARN')
        
        if not web_acl_arn:
            return {"error": f"Web ACL {web_acl_name} not found"}
        
        # Calculate time range (last hour)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=1)
        
        # Get sampled requests
        response = wafv2.get_sampled_requests(
            WebAclArn=web_acl_arn,
            RuleMetricName=rule_name if rule_name else None,
            Scope=scope,
            TimeWindow={
                'StartTime': start_time,
                'EndTime': end_time
            },
            MaxItems=max_items
        )
        
        sampled_requests = response.get('SampledRequests', [])
        
        # Group requests by action
        action_groups = {}
        for request in sampled_requests:
            action = request.get('Action', 'Unknown')
            if action not in action_groups:
                action_groups[action] = []
            action_groups[action].append(request)
        
        # Group requests by country
        country_groups = {}
        for request in sampled_requests:
            headers = request.get('Request', {}).get('Headers', [])
            country = 'Unknown'
            
            # Try to extract country from headers
            for header in headers:
                if header.get('Name', '').lower() == 'x-forwarded-for':
                    # This is a simplification, in a real implementation you would
                    # use a GeoIP database to resolve the IP to a country
                    country = 'IP-Based'
                    break
            
            if country not in country_groups:
                country_groups[country] = []
            country_groups[country].append(request)
        
        return {
            'sampledRequests': sampled_requests,
            'requestCount': len(sampled_requests),
            'actionGroups': {action: len(requests) for action, requests in action_groups.items()},
            'countryGroups': {country: len(requests) for country, requests in country_groups.items()},
            'webAclName': web_acl_name,
            'ruleName': rule_name,
            'timeWindow': {
                'startTime': start_time.isoformat(),
                'endTime': end_time.isoformat()
            }
        }
    except Exception as e:
        error_msg = f"Error getting WAF sampled requests: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_waf_ip_sets(scope: str = "REGIONAL", account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all AWS WAF IP sets in the specified scope.
    
    Args:
        scope (str): The scope of the IP sets to retrieve. Valid values: "REGIONAL" or "CLOUDFRONT".
        account_identifier (str, optional): AWS account ID, name, or OU path.
        
    Returns:
        Dictionary with IP set information or an error message.
    """
    logger.info(f"Getting WAF IP sets with scope: {scope} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Validate scope
        if scope not in ["REGIONAL", "CLOUDFRONT"]:
            return {"error": "Invalid scope. Valid values are 'REGIONAL' or 'CLOUDFRONT'"}
        
        # Get WAFv2 client
        wafv2 = get_aws_client('wafv2', profile_name=profile_name)
        
        # List IP sets
        response = wafv2.list_ip_sets(Scope=scope)
        ip_sets = response.get('IPSets', [])
        
        # Get details for each IP set
        detailed_ip_sets = []
        
        for ip_set in ip_sets:
            try:
                ip_set_response = wafv2.get_ip_set(
                    Name=ip_set['Name'],
                    Id=ip_set['Id'],
                    Scope=scope
                )
                
                detailed_ip_set = ip_set_response.get('IPSet', {})
                detailed_ip_sets.append(detailed_ip_set)
            except Exception as e:
                logger.warning(f"Error getting details for IP set {ip_set['Name']}: {str(e)}")
                detailed_ip_sets.append(ip_set)
        
        return {
            'ipSets': detailed_ip_sets,
            'count': len(detailed_ip_sets),
            'scope': scope
        }
    except Exception as e:
        error_msg = f"Error getting WAF IP sets: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_waf_metrics(web_acl_name: str, days: int = 1, account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Gets CloudWatch metrics for a specific AWS WAF Web ACL.
    
    Args:
        web_acl_name (str): The name of the Web ACL.
        days (int): Number of days of metrics to retrieve (default: 1).
        account_identifier (str, optional): AWS account ID, name, or OU path.
        
    Returns:
        Dictionary with WAF metrics or an error message.
    """
    logger.info(f"Getting WAF metrics for {web_acl_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Get CloudWatch client
        cloudwatch = get_aws_client('cloudwatch', profile_name=profile_name)
        
        # Calculate time range
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        
        # Define metrics to retrieve
        metric_names = [
            'AllowedRequests',
            'BlockedRequests',
            'CountedRequests',
            'PassedRequests',
            'CaptchaRequests',
            'RequestsWithValidCaptchaToken',
            'ChallengeRequests',
            'RequestsWithValidChallengeToken'
        ]
        
        metrics = {}
        
        for metric_name in metric_names:
            try:
                response = cloudwatch.get_metric_statistics(
                    Namespace='AWS/WAFV2',
                    MetricName=metric_name,
                    Dimensions=[
                        {
                            'Name': 'WebACL',
                            'Value': web_acl_name
                        },
                        {
                            'Name': 'Region',
                            'Value': 'us-east-1'  # This should be dynamic in a real implementation
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1 hour
                    Statistics=['Sum']
                )
                
                datapoints = response.get('Datapoints', [])
                metrics[metric_name] = datapoints
            except Exception as e:
                logger.warning(f"Error getting metric {metric_name} for Web ACL {web_acl_name}: {str(e)}")
                metrics[metric_name] = []
        
        # Calculate totals
        totals = {}
        for metric_name, datapoints in metrics.items():
            totals[metric_name] = sum(datapoint.get('Sum', 0) for datapoint in datapoints)
        
        # Calculate time series data
        time_series = {}
        for metric_name, datapoints in metrics.items():
            if datapoints:
                time_series[metric_name] = [
                    {
                        'timestamp': datapoint.get('Timestamp').isoformat(),
                        'value': datapoint.get('Sum', 0)
                    }
                    for datapoint in sorted(datapoints, key=lambda x: x.get('Timestamp'))
                ]
            else:
                time_series[metric_name] = []
        
        return {
            'metrics': metrics,
            'totals': totals,
            'timeSeries': time_series,
            'webAclName': web_acl_name,
            'timeRange': {
                'startTime': start_time.isoformat(),
                'endTime': end_time.isoformat(),
                'days': days
            }
        }
    except Exception as e:
        error_msg = f"Error getting WAF metrics: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def register_resources(server):
    """Register WAF resources with the MCP server."""
    logger.info("Registering WAF resources")
    # No resources for WAF currently

def register_tools(server):
    """Register WAF tools with the MCP server."""
    logger.info("Registering WAF tools")
    
    server.tool("list_waf_web_acls", "Lists all AWS WAF Web ACLs in the specified scope.")(list_waf_web_acls)
    server.tool("get_waf_web_acl_details", "Gets detailed information about a specific AWS WAF Web ACL, including its rules.")(get_waf_web_acl_details)
    server.tool("get_waf_sampled_requests", "Gets sampled web requests that were inspected by a specific AWS WAF Web ACL.")(get_waf_sampled_requests)
    server.tool("get_waf_ip_sets", "Lists all AWS WAF IP sets in the specified scope.")(get_waf_ip_sets)
    server.tool("get_waf_metrics", "Gets CloudWatch metrics for a specific AWS WAF Web ACL.")(get_waf_metrics)

def register_prompts(server):
    """Register WAF prompts with the MCP server."""
    logger.info("Registering WAF prompts")
    
    @server.prompt()
    def aws_waf() -> str:
        """Prompt for AWS WAF functionality."""
        return """
        # AWS WAF
        
        AWS WAF is a web application firewall that helps protect your web applications from common web exploits that could affect application availability, compromise security, or consume excessive resources. This module provides tools to interact with AWS WAF, including listing Web ACLs, getting Web ACL details, and analyzing sampled requests.
        
        ## Available Tools
        
        - `list_waf_web_acls`: Lists all AWS WAF Web ACLs in the specified scope.
        - `get_waf_web_acl_details`: Gets detailed information about a specific AWS WAF Web ACL, including its rules.
        - `get_waf_sampled_requests`: Gets sampled web requests that were inspected by a specific AWS WAF Web ACL.
        - `get_waf_ip_sets`: Lists all AWS WAF IP sets in the specified scope.
        - `get_waf_metrics`: Gets CloudWatch metrics for a specific AWS WAF Web ACL.
        
        ## Examples
        
        ```python
        # List all WAF Web ACLs in the REGIONAL scope
        web_acls = use_mcp_tool("aws_monitoring", "list_waf_web_acls", {"scope": "REGIONAL"})
        
        # Get details for a specific Web ACL
        web_acl_details = use_mcp_tool("aws_monitoring", "get_waf_web_acl_details", {
            "web_acl_id": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
            "web_acl_name": "MyWebACL",
            "scope": "REGIONAL"
        })
        
        # Get sampled requests for a Web ACL
        sampled_requests = use_mcp_tool("aws_monitoring", "get_waf_sampled_requests", {
            "web_acl_id": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
            "web_acl_name": "MyWebACL",
            "scope": "REGIONAL"
        })
        
        # List all IP sets in the REGIONAL scope
        ip_sets = use_mcp_tool("aws_monitoring", "get_waf_ip_sets", {"scope": "REGIONAL"})
        
        # Get metrics for a Web ACL
        metrics = use_mcp_tool("aws_monitoring", "get_waf_metrics", {"web_acl_name": "MyWebACL"})
        ```
        
        ## Cross-Account Access
        
        All WAF tools support cross-account access using the `account_identifier` parameter. You can specify an account ID, name, or OU path to access resources in a different account.
        
        ```python
        # List WAF Web ACLs from a specific account
        web_acls = use_mcp_tool("aws_monitoring", "list_waf_web_acls", {
            "scope": "REGIONAL",
            "account_identifier": "123456789012"
        })
        ```
        """
