"""
AWS Security functionality for the HC MCP AWS server.
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .common import get_aws_client
from .organization import resolve_account_identifier

logger = logging.getLogger("hc_mcp_aws")

# Input schemas for tools
class GetSecurityHubFindingsArguments(BaseModel):
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")
    filters: Optional[Dict[str, List[Dict[str, str]]]] = Field(default=None, description="Security Hub finding filters")
    max_results: int = Field(default=50, description="Maximum number of findings to return")

class GetFindingDetailsArguments(BaseModel):
    finding_id: str = Field(description="The ARN or ID of the Security Hub finding")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetInspectorFindingsArguments(BaseModel):
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")
    filter_criteria: Optional[Dict[str, Any]] = Field(default=None, description="Inspector v2 finding filter criteria")
    max_results: int = Field(default=50, description="Maximum number of findings to return")

# Module-level functions for direct import
def get_security_hub_findings(
    account_identifier: Optional[str] = None,
    filters: Optional[Dict[str, List[Dict[str, str]]]] = None,
    max_results: int = 50
) -> Dict[str, Any]:
    """
    Fetches findings from AWS Security Hub, optionally applying filters.
    Uses profile-based authentication if account_identifier is provided.

    Args:
        account_identifier (str, optional): AWS account ID, name, or OU path.
        filters (Dict[str, List[Dict[str, str]]], optional): Security Hub finding filters. 
            Example: {"SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}], 
                      "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]}
        max_results (int): Maximum number of findings to return (default: 50).

    Returns:
        Dictionary with Security Hub findings or an error message.
    """
    logger.info(f"Getting Security Hub findings for account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        securityhub = get_aws_client('securityhub', profile_name=profile_name)
        
        # Prepare filters
        if not filters:
            filters = {
                "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]
            }
        
        # Get findings
        response = securityhub.get_findings(
            Filters=filters,
            MaxResults=max_results
        )
        
        findings = response.get('Findings', [])
        
        # Group findings by severity
        severity_groups = {}
        for finding in findings:
            severity = finding.get('Severity', {}).get('Label', 'UNKNOWN')
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(finding)
        
        # Group findings by resource type
        resource_groups = {}
        for finding in findings:
            resources = finding.get('Resources', [])
            for resource in resources:
                resource_type = resource.get('Type', 'UNKNOWN')
                if resource_type not in resource_groups:
                    resource_groups[resource_type] = []
                resource_groups[resource_type].append(finding)
        
        return {
            'findings': findings,
            'findingCount': len(findings),
            'severityGroups': {
                severity: len(findings) for severity, findings in severity_groups.items()
            },
            'resourceGroups': {
                resource_type: len(findings) for resource_type, findings in resource_groups.items()
            },
            'filters': filters
        }
    except Exception as e:
        error_msg = f"Error getting Security Hub findings: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_finding_details(finding_id: str, account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches comprehensive details about a specific Security Hub finding.
    Returns the complete finding data including remediation recommendations.
    Uses profile-based authentication if account_identifier is provided.

    Args:
        finding_id (str): The ARN or ID of the Security Hub finding
        account_identifier (str, optional): AWS account ID, name, or OU path

    Returns:
        Dictionary with detailed finding information or an error message
    """
    logger.info(f"Getting details for finding: {finding_id} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        securityhub = get_aws_client('securityhub', profile_name=profile_name)
        
        # Check if finding_id is a full ARN or just an ID
        if not finding_id.startswith('arn:'):
            # Try to get the finding by ID
            filters = {
                "Id": [{"Value": finding_id, "Comparison": "EQUALS"}]
            }
            
            response = securityhub.get_findings(Filters=filters)
            findings = response.get('Findings', [])
            
            if not findings:
                return {"error": f"Finding with ID {finding_id} not found"}
            
            finding = findings[0]
        else:
            # Finding ID is an ARN, use it directly
            filters = {
                "Id": [{"Value": finding_id, "Comparison": "EQUALS"}]
            }
            
            response = securityhub.get_findings(Filters=filters)
            findings = response.get('Findings', [])
            
            if not findings:
                return {"error": f"Finding with ARN {finding_id} not found"}
            
            finding = findings[0]
        
        # Extract remediation information
        remediation = finding.get('Remediation', {})
        recommendation = finding.get('Recommendation', {})
        
        # Get related findings if available
        related_findings = []
        try:
            related_filters = {
                "RelatedFindingsId": [{"Value": finding['Id'], "Comparison": "EQUALS"}]
            }
            
            related_response = securityhub.get_findings(Filters=related_filters)
            related_findings = related_response.get('Findings', [])
        except Exception as e:
            logger.warning(f"Error getting related findings: {str(e)}")
        
        return {
            'finding': finding,
            'remediation': remediation,
            'recommendation': recommendation,
            'relatedFindings': related_findings,
            'relatedFindingCount': len(related_findings)
        }
    except Exception as e:
        error_msg = f"Error getting finding details: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_inspector_findings(
    account_identifier: Optional[str] = None,
    filter_criteria: Optional[Dict[str, Any]] = None,
    max_results: int = 50
) -> Dict[str, Any]:
    """
    Fetches vulnerability findings from AWS Inspector v2, optionally applying filters.
    Uses profile-based authentication if account_identifier is provided.

    Args:
        account_identifier (str, optional): AWS account ID, name, or OU path.
        filter_criteria (Dict[str, Any], optional): Inspector v2 finding filter criteria.
            Example: {"severity": [{"comparison": "EQUALS", "value": "HIGH"}],
                      "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]}
        max_results (int): Maximum number of findings to return (default: 50).

    Returns:
        Dictionary with Inspector v2 findings or an error message.
    """
    logger.info(f"Getting Inspector findings for account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        inspector = get_aws_client('inspector2', profile_name=profile_name)
        
        # Prepare filter criteria
        if not filter_criteria:
            filter_criteria = {
                "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
            }
        
        # Get findings
        response = inspector.list_findings(
            filterCriteria=filter_criteria,
            maxResults=max_results
        )
        
        finding_arns = response.get('findingArns', [])
        
        if not finding_arns:
            return {
                'findings': [],
                'findingCount': 0,
                'message': "No findings match the specified criteria"
            }
        
        # Get detailed findings
        findings_response = inspector.batch_get_findings(
            findingArns=finding_arns
        )
        
        findings = findings_response.get('findings', [])
        
        # Group findings by severity
        severity_groups = {}
        for finding in findings:
            severity = finding.get('severity', 'UNKNOWN')
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(finding)
        
        # Group findings by resource type
        resource_groups = {}
        for finding in findings:
            resources = finding.get('resources', [])
            for resource in resources:
                resource_type = resource.get('type', 'UNKNOWN')
                if resource_type not in resource_groups:
                    resource_groups[resource_type] = []
                resource_groups[resource_type].append(finding)
        
        # Group findings by vulnerability type
        vulnerability_groups = {}
        for finding in findings:
            vulnerability = finding.get('type', 'UNKNOWN')
            if vulnerability not in vulnerability_groups:
                vulnerability_groups[vulnerability] = []
            vulnerability_groups[vulnerability].append(finding)
        
        return {
            'findings': findings,
            'findingCount': len(findings),
            'severityGroups': {
                severity: len(findings) for severity, findings in severity_groups.items()
            },
            'resourceGroups': {
                resource_type: len(findings) for resource_type, findings in resource_groups.items()
            },
            'vulnerabilityGroups': {
                vulnerability: len(findings) for vulnerability, findings in vulnerability_groups.items()
            },
            'filterCriteria': filter_criteria
        }
    except Exception as e:
        error_msg = f"Error getting Inspector findings: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def register_resources(server):
    """Register security resources with the MCP server."""
    logger.info("Registering security resources")
    # No resources for security currently

def register_tools(server):
    """Register security tools with the MCP server."""
    logger.info("Registering security tools")
    
    server.tool("get_security_hub_findings", "Fetches findings from AWS Security Hub, optionally applying filters.")(get_security_hub_findings)
    server.tool("get_finding_details", "Fetches comprehensive details about a specific Security Hub finding.")(get_finding_details)
    server.tool("get_inspector_findings", "Fetches vulnerability findings from AWS Inspector v2, optionally applying filters.")(get_inspector_findings)

def register_prompts(server):
    """Register security prompts with the MCP server."""
    logger.info("Registering security prompts")
    
    @server.prompt()
    def aws_security() -> str:
        """Prompt for AWS Security functionality."""
        return """
        # AWS Security
        
        AWS provides several security services to help you protect your cloud resources and data. This module provides tools to interact with AWS Security Hub and Inspector, which are key services for security monitoring and vulnerability management.
        
        ## Available Tools
        
        - `get_security_hub_findings`: Fetches findings from AWS Security Hub, optionally applying filters.
        - `get_finding_details`: Fetches comprehensive details about a specific Security Hub finding.
        - `get_inspector_findings`: Fetches vulnerability findings from AWS Inspector v2, optionally applying filters.
        
        ## Examples
        
        ```python
        # Get active Security Hub findings with HIGH severity
        findings = use_mcp_tool("aws_monitoring", "get_security_hub_findings", {
            "filters": {
                "SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}],
                "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]
            }
        })
        
        # Get details for a specific finding
        finding_details = use_mcp_tool("aws_monitoring", "get_finding_details", {
            "finding_id": "arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0/IAM.1/finding/12345678-1234-1234-1234-123456789012"
        })
        
        # Get active Inspector findings with HIGH severity
        inspector_findings = use_mcp_tool("aws_monitoring", "get_inspector_findings", {
            "filter_criteria": {
                "severity": [{"comparison": "EQUALS", "value": "HIGH"}],
                "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
            }
        })
        ```
        
        ## Cross-Account Access
        
        All security tools support cross-account access using the `account_identifier` parameter. You can specify an account ID, name, or OU path to access resources in a different account.
        
        ```python
        # Get Security Hub findings from a specific account
        findings = use_mcp_tool("aws_monitoring", "get_security_hub_findings", {
            "account_identifier": "123456789012"
        })
        ```
        """
