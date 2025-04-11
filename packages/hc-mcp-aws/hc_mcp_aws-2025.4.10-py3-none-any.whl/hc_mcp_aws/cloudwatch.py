"""
AWS CloudWatch functionality for the HC MCP AWS server.
"""
import logging
import json
import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .common import get_aws_client
from .organization import resolve_account_identifier

logger = logging.getLogger("hc_mcp_aws")

# Input schemas for tools
class ListCloudWatchDashboardsArguments(BaseModel):
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetDashboardSummaryArguments(BaseModel):
    dashboard_name: str = Field(description="The name of the CloudWatch dashboard")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class GetCloudWatchAlarmsForServiceArguments(BaseModel):
    service_name: Optional[str] = Field(default=None, description="The name of the service to filter alarms for")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class FetchCloudWatchLogsForServiceArguments(BaseModel):
    service_name: str = Field(description="The name of the service to fetch logs for (e.g., 'ec2', 'lambda', 'rds')")
    days: int = Field(default=3, description="Number of days of logs to fetch")
    filter_pattern: str = Field(default="", description="Optional CloudWatch Logs filter pattern")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class ListLogGroupsArguments(BaseModel):
    prefix: str = Field(default="", description="Optional prefix to filter log groups")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

class AnalyzeLogGroupArguments(BaseModel):
    log_group_name: str = Field(description="The name of the log group to analyze")
    days: int = Field(default=1, description="Number of days of logs to analyze")
    max_events: int = Field(default=1000, description="Maximum number of events to retrieve for analysis")
    filter_pattern: str = Field(default="", description="Optional CloudWatch Logs filter pattern")
    account_identifier: Optional[str] = Field(default=None, description="AWS account ID, name, or OU path")

# Module-level functions for direct import
def list_cloudwatch_dashboards(account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all CloudWatch dashboards in the specified AWS account using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.

    Args:
        account_identifier (str, optional): AWS account ID, name, or OU path

    Returns:
        Dict[str, Any]: A dictionary containing the list of dashboard names and their ARNs.
    """
    logger.info(f"Listing CloudWatch dashboards for account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        cloudwatch = get_aws_client('cloudwatch', profile_name=profile_name)
        
        dashboards = []
        paginator = cloudwatch.get_paginator('list_dashboards')
        for page in paginator.paginate():
            dashboards.extend(page['DashboardEntries'])
        
        return {
            "dashboards": dashboards,
            "count": len(dashboards)
        }
    except Exception as e:
        error_msg = f"Error listing CloudWatch dashboards: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_dashboard_summary(dashboard_name: str, account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves and summarizes the configuration of a specified CloudWatch dashboard using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.

    Args:
        dashboard_name (str): The name of the CloudWatch dashboard
        account_identifier (str, optional): AWS account ID, name, or OU path

    Returns:
        Dict[str, Any]: A summary of the dashboard's widgets and their configurations.
    """
    logger.info(f"Getting dashboard summary for {dashboard_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        cloudwatch = get_aws_client('cloudwatch', profile_name=profile_name)
        
        # Get dashboard
        response = cloudwatch.get_dashboard(DashboardName=dashboard_name)
        dashboard_body = json.loads(response['DashboardBody'])
        
        # Extract widgets
        widgets = dashboard_body.get('widgets', [])
        widget_summary = []
        
        for widget in widgets:
            widget_type = widget.get('type', 'unknown')
            properties = widget.get('properties', {})
            
            widget_info = {
                'type': widget_type,
                'title': properties.get('title', 'Untitled'),
                'position': widget.get('x', 0),
                'size': {
                    'width': widget.get('width', 0),
                    'height': widget.get('height', 0)
                }
            }
            
            # Extract metrics
            if widget_type == 'metric':
                metrics = properties.get('metrics', [])
                widget_info['metrics'] = metrics
                widget_info['metric_count'] = len(metrics)
            
            # Extract alarm annotations
            if 'annotations' in properties:
                widget_info['annotations'] = properties['annotations']
            
            widget_summary.append(widget_info)
        
        return {
            'dashboard_name': dashboard_name,
            'widget_count': len(widgets),
            'widgets': widget_summary,
            'dashboard_body': dashboard_body
        }
    except Exception as e:
        error_msg = f"Error getting dashboard summary: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def get_cloudwatch_alarms_for_service(service_name: Optional[str] = None, account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches CloudWatch alarms, optionally filtering by service, using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.
    
    Args:
        service_name (str, optional): The name of the service to filter alarms for
        account_identifier (str, optional): AWS account ID, name, or OU path
        
    Returns:
        Dictionary with alarm information
    """
    logger.info(f"Getting CloudWatch alarms for service: {service_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        cloudwatch = get_aws_client('cloudwatch', profile_name=profile_name)
        
        # Get all alarms
        alarms = []
        paginator = cloudwatch.get_paginator('describe_alarms')
        for page in paginator.paginate():
            alarms.extend(page['MetricAlarms'])
            alarms.extend(page.get('CompositeAlarms', []))
        
        # Filter by service if specified
        if service_name:
            service_name = service_name.lower()
            filtered_alarms = []
            
            for alarm in alarms:
                # Check namespace
                namespace = alarm.get('Namespace', '').lower()
                if service_name in namespace:
                    filtered_alarms.append(alarm)
                    continue
                
                # Check metric name
                metric_name = alarm.get('MetricName', '').lower()
                if service_name in metric_name:
                    filtered_alarms.append(alarm)
                    continue
                
                # Check alarm name
                alarm_name = alarm.get('AlarmName', '').lower()
                if service_name in alarm_name:
                    filtered_alarms.append(alarm)
                    continue
            
            alarms = filtered_alarms
        
        # Group alarms by state
        alarm_states = {}
        for alarm in alarms:
            state = alarm.get('StateValue', 'UNKNOWN')
            if state not in alarm_states:
                alarm_states[state] = []
            alarm_states[state].append(alarm)
        
        return {
            'alarms': alarms,
            'alarm_count': len(alarms),
            'alarm_states': {state: len(alarms) for state, alarms in alarm_states.items()},
            'service_name': service_name
        }
    except Exception as e:
        error_msg = f"Error getting CloudWatch alarms: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def fetch_cloudwatch_logs_for_service(
    service_name: str, 
    days: int = 3, 
    filter_pattern: str = "", 
    account_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetches CloudWatch logs for a specified service using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.
    
    Args:
        service_name (str): The name of the service to fetch logs for (e.g., "ec2", "lambda", "rds")
        days (int): Number of days of logs to fetch (default: 3)
        filter_pattern (str): Optional CloudWatch Logs filter pattern
        account_identifier (str, optional): AWS account ID, name, or OU path
        
    Returns:
        Dictionary with log groups and their recent log events
    """
    logger.info(f"Fetching CloudWatch logs for service: {service_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        logs_client = get_aws_client('logs', profile_name=profile_name)
        
        # Get log groups for the service
        log_groups = []
        paginator = logs_client.get_paginator('describe_log_groups')
        
        # Convert service name to common prefixes
        service_prefixes = {
            'ec2': ['/aws/ec2', '/var/log'],
            'lambda': ['/aws/lambda'],
            'rds': ['/aws/rds'],
            'ecs': ['/aws/ecs'],
            'eks': ['/aws/eks'],
            'apigateway': ['/aws/apigateway'],
            'cloudtrail': ['/aws/cloudtrail'],
            'route53': ['/aws/route53'],
            'vpc': ['/aws/vpc'],
            'waf': ['/aws/waf'],
            's3': ['/aws/s3'],
            'dynamodb': ['/aws/dynamodb'],
            'elasticache': ['/aws/elasticache'],
            'elasticsearch': ['/aws/es'],
            'kinesis': ['/aws/kinesis'],
            'sqs': ['/aws/sqs'],
            'sns': ['/aws/sns'],
            'cloudfront': ['/aws/cloudfront'],
            'codebuild': ['/aws/codebuild'],
            'codepipeline': ['/aws/codepipeline'],
            'cognito': ['/aws/cognito'],
            'glue': ['/aws/glue'],
            'guardduty': ['/aws/guardduty'],
            'inspector': ['/aws/inspector'],
            'iot': ['/aws/iot'],
            'mq': ['/aws/mq'],
            'msk': ['/aws/msk'],
            'neptune': ['/aws/neptune'],
            'network-firewall': ['/aws/network-firewall'],
            'opensearch': ['/aws/opensearch'],
            'redshift': ['/aws/redshift'],
            'securityhub': ['/aws/securityhub'],
            'stepfunctions': ['/aws/stepfunctions'],
            'transfer': ['/aws/transfer'],
            'xray': ['/aws/xray']
        }
        
        prefixes = service_prefixes.get(service_name.lower(), [f'/aws/{service_name}', service_name])
        
        for prefix in prefixes:
            for page in paginator.paginate(logGroupNamePrefix=prefix):
                log_groups.extend(page['logGroups'])
        
        # If no log groups found with prefixes, try a broader search
        if not log_groups:
            for page in paginator.paginate():
                for log_group in page['logGroups']:
                    if service_name.lower() in log_group['logGroupName'].lower():
                        log_groups.append(log_group)
        
        # Calculate start time
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)
        
        # Fetch log events for each log group
        log_data = []
        
        for log_group in log_groups[:10]:  # Limit to 10 log groups to avoid timeout
            log_group_name = log_group['logGroupName']
            
            try:
                # Get log streams
                streams_response = logs_client.describe_log_streams(
                    logGroupName=log_group_name,
                    orderBy='LastEventTime',
                    descending=True,
                    limit=5  # Limit to 5 most recent streams
                )
                
                log_streams = streams_response.get('logStreams', [])
                
                # Fetch events from each stream
                events = []
                
                for stream in log_streams:
                    try:
                        if filter_pattern:
                            filter_response = logs_client.filter_log_events(
                                logGroupName=log_group_name,
                                logStreamNames=[stream['logStreamName']],
                                startTime=start_timestamp,
                                endTime=end_timestamp,
                                filterPattern=filter_pattern,
                                limit=100
                            )
                            events.extend(filter_response.get('events', []))
                        else:
                            events_response = logs_client.get_log_events(
                                logGroupName=log_group_name,
                                logStreamName=stream['logStreamName'],
                                startTime=start_timestamp,
                                endTime=end_timestamp,
                                limit=100
                            )
                            events.extend(events_response.get('events', []))
                    except Exception as e:
                        logger.warning(f"Error fetching events from stream {stream['logStreamName']}: {str(e)}")
                
                # Add log group data
                log_data.append({
                    'logGroupName': log_group_name,
                    'events': events,
                    'eventCount': len(events)
                })
                
            except Exception as e:
                logger.warning(f"Error processing log group {log_group_name}: {str(e)}")
        
        return {
            'service': service_name,
            'logGroups': log_data,
            'logGroupCount': len(log_groups),
            'processedLogGroupCount': len(log_data),
            'totalEventCount': sum(group['eventCount'] for group in log_data)
        }
        
    except Exception as e:
        error_msg = f"Error fetching CloudWatch logs: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def list_log_groups(prefix: str = "", account_identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all CloudWatch log groups, optionally filtered by a prefix, using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.
    
    Args:
        prefix (str, optional): Optional prefix to filter log groups
        account_identifier (str, optional): AWS account ID, name, or OU path
        
    Returns:
        Dictionary with list of log groups and their details
    """
    logger.info(f"Listing log groups with prefix: {prefix} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        logs_client = get_aws_client('logs', profile_name=profile_name)
        
        # Get log groups
        log_groups = []
        paginator = logs_client.get_paginator('describe_log_groups')
        
        if prefix:
            for page in paginator.paginate(logGroupNamePrefix=prefix):
                log_groups.extend(page['logGroups'])
        else:
            for page in paginator.paginate():
                log_groups.extend(page['logGroups'])
        
        # Group log groups by service
        service_groups = {}
        
        for log_group in log_groups:
            name = log_group['logGroupName']
            parts = name.split('/')
            
            # Try to determine the service
            service = "other"
            if name.startswith('/aws/'):
                service = parts[2] if len(parts) > 2 else parts[1]
            elif name.startswith('/var/log/'):
                service = "ec2"
            elif name.startswith('/'):
                service = parts[1] if len(parts) > 1 else "other"
            
            if service not in service_groups:
                service_groups[service] = []
            
            service_groups[service].append(log_group)
        
        return {
            'logGroups': log_groups,
            'logGroupCount': len(log_groups),
            'serviceGroups': {
                service: len(groups) for service, groups in service_groups.items()
            },
            'prefix': prefix
        }
        
    except Exception as e:
        error_msg = f"Error listing log groups: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def analyze_log_group(
    log_group_name: str, 
    days: int = 1, 
    max_events: int = 1000, 
    filter_pattern: str = "", 
    account_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes a specific CloudWatch log group using profile-based authentication.
    Account can be specified by ID, name, or OU path. If not specified, uses default credentials.
    
    Args:
        log_group_name (str): The name of the log group to analyze
        days (int): Number of days of logs to analyze (default: 1)
        max_events (int): Maximum number of events to retrieve for analysis (default: 1000)
        filter_pattern (str): Optional CloudWatch Logs filter pattern
        account_identifier (str, optional): AWS account ID, name, or OU path
        
    Returns:
        Dictionary with analysis and insights about the log group
    """
    logger.info(f"Analyzing log group: {log_group_name} in account: {account_identifier}")
    
    profile_name = None
    if account_identifier:
        resolved = resolve_account_identifier(account_identifier)
        if "error" in resolved:
            return {"error": resolved["error"]}
        if "profile_name" in resolved:
            profile_name = resolved["profile_name"]
    
    try:
        logs_client = get_aws_client('logs', profile_name=profile_name)
        
        # Calculate start time
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)
        
        # Get log group details
        log_group_info = logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
        if not log_group_info.get('logGroups'):
            return {"error": f"Log group {log_group_name} not found"}
        
        log_group = log_group_info['logGroups'][0]
        
        # Get log streams
        streams_response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=10  # Limit to 10 most recent streams
        )
        
        log_streams = streams_response.get('logStreams', [])
        
        # Fetch events
        events = []
        
        if filter_pattern:
            # Use filter_log_events for pattern matching
            filter_response = logs_client.filter_log_events(
                logGroupName=log_group_name,
                startTime=start_timestamp,
                endTime=end_timestamp,
                filterPattern=filter_pattern,
                limit=max_events
            )
            events = filter_response.get('events', [])
        else:
            # Get events from each stream
            for stream in log_streams:
                try:
                    events_response = logs_client.get_log_events(
                        logGroupName=log_group_name,
                        logStreamName=stream['logStreamName'],
                        startTime=start_timestamp,
                        endTime=end_timestamp,
                        limit=min(max_events // len(log_streams), 1000)  # Distribute max_events across streams
                    )
                    events.extend(events_response.get('events', []))
                except Exception as e:
                    logger.warning(f"Error fetching events from stream {stream['logStreamName']}: {str(e)}")
        
        # Limit total events
        events = events[:max_events]
        
        # Analyze events
        error_count = 0
        warning_count = 0
        info_count = 0
        
        error_keywords = ['error', 'exception', 'fail', 'fatal', 'critical']
        warning_keywords = ['warn', 'warning', 'could not', 'unable to']
        
        error_events = []
        warning_events = []
        
        for event in events:
            message = event.get('message', '').lower()
            
            # Check for errors
            if any(keyword in message for keyword in error_keywords):
                error_count += 1
                if len(error_events) < 10:  # Limit to 10 examples
                    error_events.append(event)
            
            # Check for warnings
            elif any(keyword in message for keyword in warning_keywords):
                warning_count += 1
                if len(warning_events) < 10:  # Limit to 10 examples
                    warning_events.append(event)
            
            # Count info events
            else:
                info_count += 1
        
        # Calculate time distribution
        time_distribution = {}
        
        for event in events:
            timestamp = event.get('timestamp', 0)
            event_time = datetime.datetime.fromtimestamp(timestamp / 1000)
            hour = event_time.hour
            
            if hour not in time_distribution:
                time_distribution[hour] = 0
            
            time_distribution[hour] += 1
        
        # Sort time distribution by hour
        time_distribution = {
            str(hour): time_distribution[hour] 
            for hour in sorted(time_distribution.keys())
        }
        
        return {
            'logGroupName': log_group_name,
            'logGroupDetails': log_group,
            'streamCount': len(log_streams),
            'eventCount': len(events),
            'errorCount': error_count,
            'warningCount': warning_count,
            'infoCount': info_count,
            'errorPercentage': round(error_count / len(events) * 100, 2) if events else 0,
            'warningPercentage': round(warning_count / len(events) * 100, 2) if events else 0,
            'timeDistribution': time_distribution,
            'errorSamples': error_events,
            'warningSamples': warning_events,
            'analyzedDays': days,
            'filterPattern': filter_pattern
        }
        
    except Exception as e:
        error_msg = f"Error analyzing log group: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def register_resources(server):
    """Register CloudWatch resources with the MCP server."""
    logger.info("Registering CloudWatch resources")
    # No resources for CloudWatch currently

def register_tools(server):
    """Register CloudWatch tools with the MCP server."""
    logger.info("Registering CloudWatch tools")
    
    server.tool("list_cloudwatch_dashboards", "Lists all CloudWatch dashboards in the specified AWS account.")(list_cloudwatch_dashboards)
    server.tool("get_dashboard_summary", "Retrieves and summarizes the configuration of a specified CloudWatch dashboard.")(get_dashboard_summary)
    server.tool("get_cloudwatch_alarms_for_service", "Fetches CloudWatch alarms, optionally filtering by service.")(get_cloudwatch_alarms_for_service)
    server.tool("fetch_cloudwatch_logs_for_service", "Fetches CloudWatch logs for a specified service.")(fetch_cloudwatch_logs_for_service)
    server.tool("list_log_groups", "Lists all CloudWatch log groups, optionally filtered by a prefix.")(list_log_groups)
    server.tool("analyze_log_group", "Analyzes a specific CloudWatch log group.")(analyze_log_group)

def register_prompts(server):
    """Register CloudWatch prompts with the MCP server."""
    logger.info("Registering CloudWatch prompts")
    
    @server.prompt()
    def aws_cloudwatch() -> str:
        """Prompt for AWS CloudWatch functionality."""
        return """
        # AWS CloudWatch
        
        AWS CloudWatch is a monitoring and observability service that provides data and actionable insights for AWS, hybrid, and on-premises applications and infrastructure resources. You can use CloudWatch to detect anomalous behavior in your environments, set alarms, visualize logs and metrics side by side, take automated actions, troubleshoot issues, and discover insights to keep your applications running smoothly.
        
        ## Available Tools
        
        - `list_cloudwatch_dashboards`: Lists all CloudWatch dashboards in the specified AWS account.
        - `get_dashboard_summary`: Retrieves and summarizes the configuration of a specified CloudWatch dashboard.
        - `get_cloudwatch_alarms_for_service`: Fetches CloudWatch alarms, optionally filtering by service.
        - `fetch_cloudwatch_logs_for_service`: Fetches CloudWatch logs for a specified service.
        - `list_log_groups`: Lists all CloudWatch log groups, optionally filtered by a prefix.
        - `analyze_log_group`: Analyzes a specific CloudWatch log group.
        
        ## Examples
        
        ```python
        # List all CloudWatch dashboards
        dashboards = use_mcp_tool("aws_monitoring", "list_cloudwatch_dashboards", {})
        
        # Get dashboard summary
        dashboard = use_mcp_tool("aws_monitoring", "get_dashboard_summary", {"dashboard_name": "MyDashboard"})
        
        # Get alarms for a service
        alarms = use_mcp_tool("aws_monitoring", "get_cloudwatch_alarms_for_service", {"service_name": "ec2"})
        
        # Fetch logs for a service
        logs = use_mcp_tool("aws_monitoring", "fetch_cloudwatch_logs_for_service", {"service_name": "lambda", "days": 1})
        
        # List log groups
        log_groups = use_mcp_tool("aws_monitoring", "list_log_groups", {"prefix": "/aws/lambda"})
        
        # Analyze a log group
        analysis = use_mcp_tool("aws_monitoring", "analyze_log_group", {"log_group_name": "/aws/lambda/my-function"})
        ```
        
        ## Cross-Account Access
        
        All CloudWatch tools support cross-account access using the `account_identifier` parameter. You can specify an account ID, name, or OU path to access resources in a different account.
        
        ```python
        # Get alarms from a specific account
        alarms = use_mcp_tool("aws_monitoring", "get_cloudwatch_alarms_for_service", {
            "service_name": "ec2",
            "account_identifier": "123456789012"
        })
        ```
        """
