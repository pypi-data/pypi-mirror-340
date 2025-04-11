"""
AWS MCP Server implementation.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from .organization import (
    get_organization_structure,
    resolve_account_identifier,
    OrganizationCache,
    get_organization_structure_tool,
    resolve_account_identifier_tool
)
from .cloudwatch import (
    list_cloudwatch_dashboards,
    get_cloudwatch_alarms_for_service,
    fetch_cloudwatch_logs_for_service,
    get_dashboard_summary,
    list_log_groups,
    analyze_log_group
)
from .security import (
    get_security_hub_findings,
    get_finding_details,
    get_inspector_findings
)
from .waf import (
    list_waf_web_acls,
    get_waf_web_acl_details,
    get_waf_sampled_requests,
    get_waf_ip_sets,
    get_waf_metrics
)
from .resource_discovery import (
    discover_aws_resources
)

# Configure logging
# Ensure logs directory exists
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging to file only
log_file_path = os.path.join(logs_dir, 'aws_mcp.log')

# Create logger
logger = logging.getLogger('hc_mcp_aws')
logger.setLevel(logging.INFO)

# Create formatter and handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler - rotates logs at 5MB, keeps 5 backups
file_handler = RotatingFileHandler(
    log_file_path, 
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5
)
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

# Prevent propagation to root logger to avoid duplicate logs
logger.propagate = False

# Log startup information
logger.info(f"AWS MCP server starting up. Log file: {log_file_path}")

# Create MCP server
aws_server = FastMCP("AWS-MCP-Server")

# Define MCP resources for account context
@aws_server.resource("aws://account/structure")
def get_account_structure_resource() -> Dict[str, Any]:
    """
    Resource that provides the AWS organization structure with accounts and OUs.
    """
    return get_organization_structure(refresh=False)

@aws_server.resource("aws://account/details")
def get_account_details_resource() -> Dict[str, Any]:
    """
    Resource that provides detailed information about all AWS accounts.
    """
    try:
        # Get organization cache
        org_cache = OrganizationCache()
        
        # Check if cache needs refresh
        if org_cache.needs_refresh():
            org_cache.refresh()
        
        # Build response with details for all accounts
        accounts_details = {}
        
        for account_id, account_details in org_cache.accounts.items():
            # Try to get additional account details
            try:
                # Get account tags
                tags_response = org_cache.get_account_tags(account_id)
                tags = tags_response.get('Tags', [])
                
                # Get parent OU
                parent_info = org_cache.get_account_parent(account_id)
            except Exception as e:
                logger.warning(f"Error getting additional details for account {account_id}: {e}")
                tags = []
                parent_info = None
            
            # Add account details to response
            accounts_details[account_id] = {
                "id": account_id,
                "name": account_details.get("Name"),
                "email": account_details.get("Email"),
                "status": account_details.get("Status"),
                "joined_method": account_details.get("JoinedMethod"),
                "joined_timestamp": account_details.get("JoinedTimestamp").isoformat() if account_details.get("JoinedTimestamp") else None,
                "tags": tags,
                "parent": parent_info
            }
        
        return {
            "status": "success",
            "accounts": accounts_details,
            "account_count": len(accounts_details)
        }
        
    except Exception as e:
        logger.error(f"Error getting account details: {e}")
        return {"status": "error", "message": str(e)}

@aws_server.resource("aws://account/access-map")
def get_cross_account_access_map_resource() -> Dict[str, Any]:
    """
    Resource that shows which accounts can be accessed with current credentials.
    """
    try:
        # Get organization cache
        org_cache = OrganizationCache()
        
        # Check if cache needs refresh
        if org_cache.needs_refresh():
            org_cache.refresh()
        
        # Test access to each account
        accessible_accounts = []
        inaccessible_accounts = []
        
        for account_id, details in org_cache.accounts.items():
            account_name = details.get("Name", "Unknown")
            
            # Skip if account is not active
            if details.get("Status") != "ACTIVE":
                inaccessible_accounts.append({
                    "id": account_id,
                    "name": account_name,
                    "reason": f"Account status is {details.get('Status')}"
                })
                continue
            
            # Test if profile exists and has access
            profile_name = f"AdministratorAccess@{account_name.replace(' ', '_')}"
            
            try:
                # Test access using the profile
                caller_identity = org_cache.test_account_access(profile_name)
                
                accessible_accounts.append({
                    "id": account_id,
                    "name": account_name,
                    "profile": profile_name,
                    "caller_identity": caller_identity
                })
            except Exception as e:
                inaccessible_accounts.append({
                    "id": account_id,
                    "name": account_name,
                    "profile": profile_name,
                    "reason": str(e)
                })
        
        return {
            "status": "success",
            "accessible_account_count": len(accessible_accounts),
            "inaccessible_account_count": len(inaccessible_accounts),
            "accessible_accounts": accessible_accounts,
            "inaccessible_accounts": inaccessible_accounts
        }
        
    except Exception as e:
        logger.error(f"Error getting cross account access map: {e}")
        return {"status": "error", "message": str(e)}

# Register tools with the server
def register_tools():
    """Register all tools with the MCP server."""
    # Register organization tools directly
    from .organization import (
        get_organization_structure_tool,
        resolve_account_identifier_tool,
        GetOrganizationStructureArguments,
        ResolveAccountIdentifierArguments
    )
    aws_server.tool("get_organization_structure", "Retrieves the AWS organization structure, including accounts and OUs.")(get_organization_structure_tool)
    aws_server.tool("resolve_account_identifier", "Resolves an account name, ID, or OU path to account details.")(resolve_account_identifier_tool)
    
    # Import cloudwatch module tools
    from .cloudwatch import register_tools as register_cloudwatch_tools
    register_cloudwatch_tools(aws_server)
    
    # Import security module tools
    from .security import register_tools as register_security_tools
    register_security_tools(aws_server)
    
    # Import WAF module tools
    from .waf import register_tools as register_waf_tools
    register_waf_tools(aws_server)
    
    # Import resource discovery module tools
    from .resource_discovery import register_tools as register_resource_discovery_tools
    register_resource_discovery_tools(aws_server)

# Register prompts with the server
def register_prompts():
    """Register all prompts with the MCP server."""
    # Import organization module prompts
    from .organization import register_prompts as register_organization_prompts
    register_organization_prompts(aws_server)
    
    # Import cloudwatch module prompts
    from .cloudwatch import register_prompts as register_cloudwatch_prompts
    register_cloudwatch_prompts(aws_server)
    
    # Import security module prompts
    from .security import register_prompts as register_security_prompts
    register_security_prompts(aws_server)
    
    # Import WAF module prompts
    from .waf import register_prompts as register_waf_prompts
    register_waf_prompts(aws_server)
    
    # Add main AWS resources analysis prompt
    @aws_server.prompt()
    def analyze_aws_resources() -> str:
        """Prompt to analyze AWS resources, including CloudWatch logs, alarms, dashboards, Security Hub, and Inspector findings using profile-based authentication."""
        return """
        You are the monitoring agent responsible for analyzing AWS resources, including CloudWatch logs, alarms, and dashboards. Your tasks include:

        IMPORTANT:
            Follow the instructions carefully and use the tools as needed:
            - Your first question should be to ask the user for which account they want to monitor: their own or a specific target account.
            - If the user says "my account" or doesn't specify, use the default account/credentials (no `account_identifier` needed for tools).
            - If the user specifies a target account, ask for the account identifier (ID, name, or OU path).
            - Access to target accounts relies on pre-configured AWS profiles named 'AdministratorAccess@<Account_Name>' (with spaces in the name replaced by underscores). Ensure these profiles exist in the AWS credentials/config file.
            - Use the `account_identifier` parameter in the tools you call ONLY when a target account is specified.
            - If the user doesn't provide an account identifier when needed, always ask for this. Do NOT guess or assume an identifier.
            
        **Monitoring & Logging Tools:**

        1. **List CloudWatch Dashboards:**
           - Use `list_cloudwatch_dashboards` to retrieve dashboards in the specified account.
           - Provide the user with the names and descriptions of these dashboards.

        2. **Fetch CloudWatch Logs:**
           - Use `fetch_cloudwatch_logs_for_service` for a specific service (e.g., EC2, Lambda).
           - Summarize findings, errors, warnings.

        3. **Get CloudWatch Alarms:**
           - Use `get_cloudwatch_alarms_for_service` to fetch alarms, optionally filtered by service.
           - Report state and metrics of active alarms.

        4. **Summarize CloudWatch Dashboard:**
           - Use `get_dashboard_summary` for a specific dashboard.
           - Detail widgets and their types.

        5. **List CloudWatch Log Groups:**
           - Use `list_log_groups`, optionally filtering by prefix.

        6. **Analyze Log Group:**
           - Use `analyze_log_group` for detailed insights into a specific log group.
           - Summarize event counts, error rates, common patterns.

        **Security Tools:**

        7. **Get Security Hub Findings:**
           - Use `get_security_hub_findings` to retrieve security findings.
           - You can filter by severity, status, etc. using the `filters` argument (see tool description for format). Example: `filters={"SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}], "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]}`
           - Summarize the findings, focusing on title, severity, resource, and state.

        8. **Get Finding Details:**
           - Use `get_finding_details` to get comprehensive information about a specific finding.
           - Works with any Security Hub finding, with special handling for AWS Health events.
           - Provide the finding ID (ARN) from Security Hub findings.
           - Returns complete details including remediation recommendations.

        9. **Get Inspector Findings:**
           - Use `get_inspector_findings` to retrieve vulnerability findings from Inspector v2.
           - You can filter using the `filter_criteria` argument (see tool description for format). Example: `filter_criteria={"severity": [{"comparison": "EQUALS", "value": "HIGH"}], "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]}`
           - Summarize findings, focusing on title, severity, status, and affected resource.

        **Organization & Access:**

        9. **Organization Info (Informational):**
           - Use `get_organization_structure` (uses default credentials) to list accounts/OUs.
           - Use `resolve_account_identifier` (uses default credentials) to resolve names/OUs to IDs.

        10. **Target Account Access (Profile-Based):**
            - Support monitoring across accounts via named profiles (`AdministratorAccess@<Account_Name>`).
            - Ask for the `account_identifier` (ID, name, or OU path) for target accounts.
            - Pass the `account_identifier` to monitoring and security tools when needed.
            - Report access issues (profile not found, permissions) clearly.

        **Guidelines:**

        - Always begin by asking the USER FOR WHICH ACCOUNT THEY WANT TO MONITOR: THEIR OWN ACCOUNT OR A SPECIFIC TARGET ACCOUNT.
        - If the user wants to monitor their own account, call tools WITHOUT the `account_identifier` parameter.
        - If the user wants to monitor a target account:
          - Ask for the account identifier (ID, name, or OU path).
          - Use the organization tools (`get_organization_structure`, `resolve_account_identifier`) with default credentials if needed to help find the correct identifier.
          - Call monitoring tools WITH the `account_identifier` parameter set to the user-provided value.
        - When analyzing logs or alarms, be thorough yet concise.
        - Base your analysis strictly on the data retrieved from AWS tools.
        - If a tool call fails due to profile issues (e.g., `ProfileNotFound`, `CredentialsError`), report this specific error back to the user.

        **Resource Discovery:**

        11. **Discover AWS Resources:**
            - Use `discover_aws_resources` to get a comprehensive view of resources for a specific AWS service.
            - This tool bridges the gap between what's visible in the AWS console and what's accessible via MCP.
            - Specify the service name (e.g., "ec2", "s3", "waf") and optionally filter by resource type.
            - Returns detailed information about resources in a format similar to the AWS console.
            - Example: `discover_aws_resources(service_name="waf", scope="REGIONAL")` to discover WAF resources.

        **Available AWS Services for Monitoring:**

        - **EC2/Compute Instances** [ec2] - Instances, security groups
        - **Lambda Functions** [lambda]
        - **RDS Databases** [rds]
        - **EKS Kubernetes** [eks]
        - **API Gateway** [apigateway]
        - **CloudTrail** [cloudtrail] - Trails
        - **S3 Storage** [s3] - Buckets
        - **VPC Networking** [vpc] - VPCs, subnets
        - **WAF Web Security** [waf] - Web ACLs, IP sets, rules
        - **CloudWatch** [cloudwatch] - Dashboards, alarms
        - **Logs** [logs] - Log groups
        - **Bedrock** [bedrock/generative AI]
        - **IAM Logs** [iam] (Use this option when users inquire about security logs or events.)
        - **Security Hub** [securityhub] (Use `get_security_hub_findings`)
        - **Inspector** [inspector] (Use `get_inspector_findings`)
        - Any other AWS service the user requests - the system will attempt to create a dynamic mapping for logs

        **Target Account Monitoring Instructions:**
        
        When a user wants to monitor resources in a different AWS account:
        1. Ask for the AWS account identifier (ID, name, or OU path).
           - You can use `get_organization_structure` or `resolve_account_identifier` (using default credentials) to help the user find the identifier if they are unsure.
        2. Once the identifier is provided, use it in the `account_identifier` parameter when calling the monitoring tools (`list_cloudwatch_dashboards`, `fetch_cloudwatch_logs_for_service`, etc.).
        3. The system relies on a pre-configured AWS profile: `AdministratorAccess@<Resolved_Account_Name>` (spaces replaced by underscores).
        4. Always specify which account you're reporting on in your analysis.
        5. If access fails, provide the specific error message (e.g., "ProfileNotFound", "AccessDenied") and suggest checking:
           - That the account identifier resolves to the correct account name.
           - That the profile `AdministratorAccess@<Resolved_Account_Name>` exists in the AWS config/credentials file.
           - That the credentials associated with the profile have the necessary permissions in the target account.

        Your role is to assist users in monitoring and analyzing their AWS resources (logs, alarms, security findings) effectively using profile-based authentication.
        """

# Register all tools and prompts
register_tools()
register_prompts()

def run_server():
    """Run the MCP server."""
    aws_server.run(transport='stdio')

if __name__ == "__main__":
    run_server()
