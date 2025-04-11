"""
S3 resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

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
