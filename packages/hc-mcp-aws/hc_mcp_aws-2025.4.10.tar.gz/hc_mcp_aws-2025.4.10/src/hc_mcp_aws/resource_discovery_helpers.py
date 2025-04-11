"""
Helper functions for AWS resource discovery.
"""
import logging
from typing import Dict, Any, List, Optional

from .common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_ec2_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover EC2 resources."""
    ec2 = get_aws_client('ec2', profile_name=profile_name)
    
    if not resource_type or resource_type == "instance":
        # Get EC2 instances
        response = ec2.describe_instances()
        instances = []
        
        for reservation in response.get('Reservations', []):
            instances.extend(reservation.get('Instances', []))
        
        # Limit to max_items
        instances = instances[:max_items]
        
        # Extract key information
        instance_info = []
        for instance in instances:
            name = "Unnamed"
            for tag in instance.get('Tags', []):
                if tag.get('Key') == 'Name':
                    name = tag.get('Value')
                    break
            
            instance_info.append({
                'InstanceId': instance.get('InstanceId'),
                'Name': name,
                'InstanceType': instance.get('InstanceType'),
                'State': instance.get('State', {}).get('Name'),
                'PrivateIpAddress': instance.get('PrivateIpAddress'),
                'PublicIpAddress': instance.get('PublicIpAddress'),
                'LaunchTime': instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None,
                'VpcId': instance.get('VpcId'),
                'SubnetId': instance.get('SubnetId'),
                'Tags': instance.get('Tags')
            })
        
        return {
            'service': 'ec2',
            'resourceType': 'instance',
            'resources': instance_info,
            'count': len(instance_info)
        }
    
    elif resource_type == "volume":
        # Get EBS volumes
        response = ec2.describe_volumes()
        volumes = response.get('Volumes', [])
        
        # Limit to max_items
        volumes = volumes[:max_items]
        
        # Extract key information
        volume_info = []
        for volume in volumes:
            name = "Unnamed"
            for tag in volume.get('Tags', []):
                if tag.get('Key') == 'Name':
                    name = tag.get('Value')
                    break
            
            volume_info.append({
                'VolumeId': volume.get('VolumeId'),
                'Name': name,
                'Size': volume.get('Size'),
                'State': volume.get('State'),
                'VolumeType': volume.get('VolumeType'),
                'AvailabilityZone': volume.get('AvailabilityZone'),
                'Attachments': volume.get('Attachments'),
                'Tags': volume.get('Tags')
            })
        
        return {
            'service': 'ec2',
            'resourceType': 'volume',
            'resources': volume_info,
            'count': len(volume_info)
        }
    
    elif resource_type == "security-group":
        # Get security groups
        response = ec2.describe_security_groups()
        security_groups = response.get('SecurityGroups', [])
        
        # Limit to max_items
        security_groups = security_groups[:max_items]
        
        return {
            'service': 'ec2',
            'resourceType': 'security-group',
            'resources': security_groups,
            'count': len(security_groups)
        }
    
    else:
        # Get multiple resource types
        instances_response = ec2.describe_instances()
        volumes_response = ec2.describe_volumes()
        security_groups_response = ec2.describe_security_groups()
        
        instances = []
        for reservation in instances_response.get('Reservations', []):
            instances.extend(reservation.get('Instances', []))
        
        volumes = volumes_response.get('Volumes', [])
        security_groups = security_groups_response.get('SecurityGroups', [])
        
        # Count resources by type
        resource_counts = {
            'instance': len(instances),
            'volume': len(volumes),
            'security-group': len(security_groups)
        }
        
        return {
            'service': 'ec2',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }

def discover_s3_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover S3 resources."""
    s3 = get_aws_client('s3', profile_name=profile_name)
    
    if not resource_type or resource_type == "bucket":
        # Get S3 buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        
        # Limit to max_items
        buckets = buckets[:max_items]
        
        # Get additional information for each bucket
        bucket_info = []
        for bucket in buckets:
            bucket_name = bucket.get('Name')
            
            try:
                # Get bucket location
                location_response = s3.get_bucket_location(Bucket=bucket_name)
                location = location_response.get('LocationConstraint', 'us-east-1')
                
                # Get bucket policy status
                try:
                    policy_status_response = s3.get_bucket_policy_status(Bucket=bucket_name)
                    is_public = policy_status_response.get('PolicyStatus', {}).get('IsPublic', False)
                except Exception:
                    is_public = False
                
                bucket_info.append({
                    'Name': bucket_name,
                    'CreationDate': bucket.get('CreationDate').isoformat() if bucket.get('CreationDate') else None,
                    'Region': location,
                    'IsPublic': is_public
                })
            except Exception as e:
                logger.warning(f"Error getting details for bucket {bucket_name}: {str(e)}")
                bucket_info.append({
                    'Name': bucket_name,
                    'CreationDate': bucket.get('CreationDate').isoformat() if bucket.get('CreationDate') else None,
                    'Error': str(e)
                })
        
        return {
            'service': 's3',
            'resourceType': 'bucket',
            'resources': bucket_info,
            'count': len(bucket_info)
        }
    
    else:
        # Get buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        
        return {
            'service': 's3',
            'resourceCounts': {
                'bucket': len(buckets)
            },
            'totalCount': len(buckets),
            'availableTypes': ['bucket']
        }

def discover_lambda_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover Lambda resources."""
    lambda_client = get_aws_client('lambda', profile_name=profile_name)
    
    if not resource_type or resource_type == "function":
        # Get Lambda functions
        response = lambda_client.list_functions(MaxItems=max_items)
        functions = response.get('Functions', [])
        
        # Extract key information
        function_info = []
        for function in functions:
            function_info.append({
                'FunctionName': function.get('FunctionName'),
                'Runtime': function.get('Runtime'),
                'Handler': function.get('Handler'),
                'CodeSize': function.get('CodeSize'),
                'Description': function.get('Description'),
                'Timeout': function.get('Timeout'),
                'MemorySize': function.get('MemorySize'),
                'LastModified': function.get('LastModified'),
                'Role': function.get('Role'),
                'Environment': function.get('Environment'),
                'TracingConfig': function.get('TracingConfig'),
                'RevisionId': function.get('RevisionId')
            })
        
        return {
            'service': 'lambda',
            'resourceType': 'function',
            'resources': function_info,
            'count': len(function_info)
        }
    
    else:
        # Get functions
        response = lambda_client.list_functions()
        functions = response.get('Functions', [])
        
        return {
            'service': 'lambda',
            'resourceCounts': {
                'function': len(functions)
            },
            'totalCount': len(functions),
            'availableTypes': ['function']
        }

def discover_rds_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover RDS resources."""
    rds = get_aws_client('rds', profile_name=profile_name)
    
    if not resource_type or resource_type == "db-instance":
        # Get RDS instances
        response = rds.describe_db_instances()
        instances = response.get('DBInstances', [])
        
        # Limit to max_items
        instances = instances[:max_items]
        
        return {
            'service': 'rds',
            'resourceType': 'db-instance',
            'resources': instances,
            'count': len(instances)
        }
    
    elif resource_type == "db-cluster":
        # Get RDS clusters
        response = rds.describe_db_clusters()
        clusters = response.get('DBClusters', [])
        
        # Limit to max_items
        clusters = clusters[:max_items]
        
        return {
            'service': 'rds',
            'resourceType': 'db-cluster',
            'resources': clusters,
            'count': len(clusters)
        }
    
    else:
        # Get multiple resource types
        instances_response = rds.describe_db_instances()
        clusters_response = rds.describe_db_clusters()
        
        instances = instances_response.get('DBInstances', [])
        clusters = clusters_response.get('DBClusters', [])
        
        # Count resources by type
        resource_counts = {
            'db-instance': len(instances),
            'db-cluster': len(clusters)
        }
        
        return {
            'service': 'rds',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }

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

def discover_iam_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover IAM resources."""
    iam = get_aws_client('iam', profile_name=profile_name)
    
    if not resource_type or resource_type == "user":
        # Get IAM users
        response = iam.list_users()
        users = response.get('Users', [])
        
        # Limit to max_items
        users = users[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'user',
            'resources': users,
            'count': len(users)
        }
    
    elif resource_type == "role":
        # Get IAM roles
        response = iam.list_roles()
        roles = response.get('Roles', [])
        
        # Limit to max_items
        roles = roles[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'role',
            'resources': roles,
            'count': len(roles)
        }
    
    elif resource_type == "group":
        # Get IAM groups
        response = iam.list_groups()
        groups = response.get('Groups', [])
        
        # Limit to max_items
        groups = groups[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'group',
            'resources': groups,
            'count': len(groups)
        }
    
    elif resource_type == "policy":
        # Get IAM policies
        response = iam.list_policies(Scope='Local')
        policies = response.get('Policies', [])
        
        # Limit to max_items
        policies = policies[:max_items]
        
        return {
            'service': 'iam',
            'resourceType': 'policy',
            'resources': policies,
            'count': len(policies)
        }
    
    else:
        # Get multiple resource types
        users_response = iam.list_users()
        roles_response = iam.list_roles()
        groups_response = iam.list_groups()
        policies_response = iam.list_policies(Scope='Local')
        
        users = users_response.get('Users', [])
        roles = roles_response.get('Roles', [])
        groups = groups_response.get('Groups', [])
        policies = policies_response.get('Policies', [])
        
        # Count resources by type
        resource_counts = {
            'user': len(users),
            'role': len(roles),
            'group': len(groups),
            'policy': len(policies)
        }
        
        return {
            'service': 'iam',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }

def discover_vpc_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover VPC resources."""
    ec2 = get_aws_client('ec2', profile_name=profile_name)
    
    if not resource_type or resource_type == "vpc":
        # Get VPCs
        response = ec2.describe_vpcs()
        vpcs = response.get('Vpcs', [])
        
        # Limit to max_items
        vpcs = vpcs[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'vpc',
            'resources': vpcs,
            'count': len(vpcs)
        }
    
    elif resource_type == "subnet":
        # Get subnets
        response = ec2.describe_subnets()
        subnets = response.get('Subnets', [])
        
        # Limit to max_items
        subnets = subnets[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'subnet',
            'resources': subnets,
            'count': len(subnets)
        }
    
    elif resource_type == "route-table":
        # Get route tables
        response = ec2.describe_route_tables()
        route_tables = response.get('RouteTables', [])
        
        # Limit to max_items
        route_tables = route_tables[:max_items]
        
        return {
            'service': 'vpc',
            'resourceType': 'route-table',
            'resources': route_tables,
            'count': len(route_tables)
        }
    
    else:
        # Get multiple resource types
        vpcs_response = ec2.describe_vpcs()
        subnets_response = ec2.describe_subnets()
        route_tables_response = ec2.describe_route_tables()
        
        vpcs = vpcs_response.get('Vpcs', [])
        subnets = subnets_response.get('Subnets', [])
        route_tables = route_tables_response.get('RouteTables', [])
        
        # Count resources by type
        resource_counts = {
            'vpc': len(vpcs),
            'subnet': len(subnets),
            'route-table': len(route_tables)
        }
        
        return {
            'service': 'vpc',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }

def discover_dynamodb_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover DynamoDB resources."""
    dynamodb = get_aws_client('dynamodb', profile_name=profile_name)
    
    if not resource_type or resource_type == "table":
        # Get DynamoDB tables
        response = dynamodb.list_tables()
        tables = response.get('TableNames', [])
        
        # Limit to max_items
        tables = tables[:max_items]
        
        # Get details for each table
        table_details = []
        for table_name in tables:
            try:
                table_response = dynamodb.describe_table(TableName=table_name)
                table_details.append(table_response.get('Table', {}))
            except Exception as e:
                logger.warning(f"Error getting details for table {table_name}: {str(e)}")
        
        return {
            'service': 'dynamodb',
            'resourceType': 'table',
            'resources': table_details,
            'count': len(table_details)
        }
    
    else:
        # Get tables
        response = dynamodb.list_tables()
        tables = response.get('TableNames', [])
        
        return {
            'service': 'dynamodb',
            'resourceCounts': {
                'table': len(tables)
            },
            'totalCount': len(tables),
            'availableTypes': ['table']
        }

def discover_sns_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover SNS resources."""
    sns = get_aws_client('sns', profile_name=profile_name)
    
    if not resource_type or resource_type == "topic":
        # Get SNS topics
        response = sns.list_topics()
        topics = response.get('Topics', [])
        
        # Limit to max_items
        topics = topics[:max_items]
        
        return {
            'service': 'sns',
            'resourceType': 'topic',
            'resources': topics,
            'count': len(topics)
        }
    
    else:
        # Get topics
        response = sns.list
