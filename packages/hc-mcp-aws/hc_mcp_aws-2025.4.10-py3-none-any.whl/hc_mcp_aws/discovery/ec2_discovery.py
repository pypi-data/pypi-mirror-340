"""
EC2 resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

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
