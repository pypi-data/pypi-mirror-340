"""
AWS Resource Discovery functionality for the HC MCP AWS server.
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .common import get_aws_client
from .organization import resolve_account_identifier
from .discovery import (
    discover_ec2_resources,
    discover_s3_resources,
    discover_lambda_resources,
    discover_rds_resources,
    discover_cloudwatch_resources,
    discover_waf_resources,
    discover_securityhub_resources,
    discover_inspector_resources,
    discover_iam_resources,
    discover_vpc_resources,
    discover_dynamodb_resources,
    discover_sns_resources,
    discover_sqs_resources,
    discover_cloudfront_resources,
    discover_route53_resources,
    discover_apigateway_resources
)

logger = logging.getLogger("hc_mcp_aws")

# Input schemas for tools
class DiscoverAwsResourcesArguments(BaseModel):
    service_name: str = Field(description="The AWS service to discover resources for (e.g., 'ec2', 's3', 'waf', 'cloudwatch')")
    resource_type: Optional[str] = Field(default=None, description="Specific resource type within the service (e.g., 'instance' for EC2, 'bucket' for S3)")
    max_items: int = Field(default=100, description="Maximum number of resources to return")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

# Module-level functions for direct import
def discover_aws_resources(
    service_name: str,
    resource_type: Optional[str] = None,
    max_items: int = 100,
    account_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Discovers AWS resources for a specific service, providing a comprehensive view similar to the AWS console.
    This tool helps bridge the gap between what's visible in the AWS console and what's accessible via the MCP tools.
    
    Args:
        service_name (str): The AWS service to discover resources for (e.g., "ec2", "s3", "waf", "cloudwatch")
        resource_type (str, optional): Specific resource type within the service (e.g., "instance" for EC2, "bucket" for S3)
        max_items (int): Maximum number of resources to return (default: 100)
        account_identifier (str, optional): AWS account ID, name, or OU path
        
    Returns:
        Dictionary with discovered resources or an error message
    """
    logger.info(f"Discovering AWS resources for service: {service_name}, type: {resource_type} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        # Normalize service name
        service_name = service_name.lower()
        
        # Service-specific discovery logic
        if service_name == "ec2":
            return discover_ec2_resources(resource_type, max_items, profile_name)
        elif service_name == "s3":
            return discover_s3_resources(resource_type, max_items, profile_name)
        elif service_name == "lambda":
            return discover_lambda_resources(resource_type, max_items, profile_name)
        elif service_name == "rds":
            return discover_rds_resources(resource_type, max_items, profile_name)
        elif service_name == "cloudwatch":
            return discover_cloudwatch_resources(resource_type, max_items, profile_name)
        elif service_name == "waf" or service_name == "wafv2":
            return discover_waf_resources(resource_type, max_items, profile_name)
        elif service_name == "securityhub":
            return discover_securityhub_resources(resource_type, max_items, profile_name)
        elif service_name == "inspector" or service_name == "inspector2":
            return discover_inspector_resources(resource_type, max_items, profile_name)
        elif service_name == "iam":
            return discover_iam_resources(resource_type, max_items, profile_name)
        elif service_name == "vpc":
            return discover_vpc_resources(resource_type, max_items, profile_name)
        elif service_name == "dynamodb":
            return discover_dynamodb_resources(resource_type, max_items, profile_name)
        elif service_name == "sns":
            return discover_sns_resources(resource_type, max_items, profile_name)
        elif service_name == "sqs":
            return discover_sqs_resources(resource_type, max_items, profile_name)
        elif service_name == "cloudfront":
            return discover_cloudfront_resources(resource_type, max_items, profile_name)
        elif service_name == "route53":
            return discover_route53_resources(resource_type, max_items, profile_name)
        elif service_name == "apigateway":
            return discover_apigateway_resources(resource_type, max_items, profile_name)
        else:
            return {"error": f"Service {service_name} is not supported for resource discovery"}
    except Exception as e:
        error_msg = f"Error discovering AWS resources: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def register_resources(server):
    """Register resource discovery resources with the MCP server."""
    logger.info("Registering resource discovery resources")
    # No resources for resource discovery currently

def register_tools(server):
    """Register resource discovery tools with the MCP server."""
    logger.info("Registering resource discovery tools")
    
    server.tool("discover_aws_resources", "Discovers AWS resources for a specific service, providing a comprehensive view similar to the AWS console.")(discover_aws_resources)

def register_prompts(server):
    """Register resource discovery prompts with the MCP server."""
    logger.info("Registering resource discovery prompts")
    
    @server.prompt()
    def aws_resource_discovery() -> str:
        """Prompt for AWS Resource Discovery functionality."""
        return """
        # AWS Resource Discovery
        
        AWS Resource Discovery provides a comprehensive view of your AWS resources across various services. This module helps bridge the gap between what's visible in the AWS console and what's accessible via the MCP tools.
        
        ## Available Tools
        
        - `discover_aws_resources`: Discovers AWS resources for a specific service, providing a comprehensive view similar to the AWS console.
        
        ## Supported Services
        
        - EC2 (ec2): Instances, security groups, volumes, etc.
        - S3 (s3): Buckets, objects, etc.
        - Lambda (lambda): Functions, layers, etc.
        - RDS (rds): Databases, clusters, etc.
        - CloudWatch (cloudwatch): Dashboards, alarms, metrics, etc.
        - WAF (waf): Web ACLs, IP sets, etc.
        - Security Hub (securityhub): Findings, insights, etc.
        - Inspector (inspector): Findings, assessment templates, etc.
        - IAM (iam): Users, roles, policies, etc.
        - VPC (vpc): VPCs, subnets, security groups, etc.
        - DynamoDB (dynamodb): Tables, streams, etc.
        - SNS (sns): Topics, subscriptions, etc.
        - SQS (sqs): Queues, etc.
        - CloudFront (cloudfront): Distributions, etc.
        - Route 53 (route53): Hosted zones, records, etc.
        - API Gateway (apigateway): APIs, stages, etc.
        
        ## Examples
        
        ```python
        # Discover EC2 instances
        ec2_resources = use_mcp_tool("aws_monitoring", "discover_aws_resources", {
            "service_name": "ec2",
            "resource_type": "instance"
        })
        
        # Discover S3 buckets
        s3_resources = use_mcp_tool("aws_monitoring", "discover_aws_resources", {
            "service_name": "s3"
        })
        
        # Discover CloudWatch dashboards
        cloudwatch_resources = use_mcp_tool("aws_monitoring", "discover_aws_resources", {
            "service_name": "cloudwatch",
            "resource_type": "dashboard"
        })
        ```
        
        ## Cross-Account Access
        
        Resource discovery supports cross-account access using the `account_identifier` parameter. You can specify an account ID, name, or OU path to discover resources in a different account.
        
        ```python
        # Discover EC2 instances in a specific account
        ec2_resources = use_mcp_tool("aws_monitoring", "discover_aws_resources", {
            "service_name": "ec2",
            "account_identifier": "123456789012"
        })
        ```
        """
