"""
SQS resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_sqs_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover SQS resources."""
    sqs = get_aws_client('sqs', profile_name=profile_name)
    
    if not resource_type or resource_type == "queue":
        # Get SQS queues
        response = sqs.list_queues()
        queue_urls = response.get('QueueUrls', [])
        
        # Limit to max_items
        queue_urls = queue_urls[:max_items]
        
        # Get additional information for each queue
        queue_details = []
        for queue_url in queue_urls:
            try:
                # Get queue attributes
                attributes_response = sqs.get_queue_attributes(
                    QueueUrl=queue_url,
                    AttributeNames=['All']
                )
                attributes = attributes_response.get('Attributes', {})
                
                # Extract queue name from URL
                queue_name = queue_url.split('/')[-1]
                
                queue_details.append({
                    'QueueUrl': queue_url,
                    'QueueName': queue_name,
                    'Attributes': attributes
                })
            except Exception as e:
                logger.warning(f"Error getting attributes for queue {queue_url}: {str(e)}")
                queue_details.append({
                    'QueueUrl': queue_url,
                    'QueueName': queue_url.split('/')[-1],
                    'Error': str(e)
                })
        
        return {
            'service': 'sqs',
            'resourceType': 'queue',
            'resources': queue_details,
            'count': len(queue_details)
        }
    
    else:
        # Get queues
        response = sqs.list_queues()
        queue_urls = response.get('QueueUrls', [])
        
        return {
            'service': 'sqs',
            'resourceCounts': {
                'queue': len(queue_urls)
            },
            'totalCount': len(queue_urls),
            'availableTypes': ['queue']
        }
