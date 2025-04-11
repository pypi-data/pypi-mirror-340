"""
SNS resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_sns_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover SNS resources."""
    sns = get_aws_client('sns', profile_name=profile_name)
    
    if not resource_type or resource_type == "topic":
        # Get SNS topics
        response = sns.list_topics()
        topics = response.get('Topics', [])
        
        # Limit to max_items
        topics = topics[:max_items]
        
        # Get additional information for each topic
        topic_details = []
        for topic in topics:
            topic_arn = topic.get('TopicArn')
            if topic_arn:
                try:
                    # Get topic attributes
                    attributes_response = sns.get_topic_attributes(TopicArn=topic_arn)
                    attributes = attributes_response.get('Attributes', {})
                    
                    topic_details.append({
                        'TopicArn': topic_arn,
                        'TopicName': topic_arn.split(':')[-1],
                        'Attributes': attributes
                    })
                except Exception as e:
                    logger.warning(f"Error getting attributes for topic {topic_arn}: {str(e)}")
                    topic_details.append({
                        'TopicArn': topic_arn,
                        'TopicName': topic_arn.split(':')[-1],
                        'Error': str(e)
                    })
        
        return {
            'service': 'sns',
            'resourceType': 'topic',
            'resources': topic_details,
            'count': len(topic_details)
        }
    
    elif resource_type == "subscription":
        # Get SNS subscriptions
        response = sns.list_subscriptions()
        subscriptions = response.get('Subscriptions', [])
        
        # Limit to max_items
        subscriptions = subscriptions[:max_items]
        
        return {
            'service': 'sns',
            'resourceType': 'subscription',
            'resources': subscriptions,
            'count': len(subscriptions)
        }
    
    else:
        # Get multiple resource types
        topics_response = sns.list_topics()
        subscriptions_response = sns.list_subscriptions()
        
        topics = topics_response.get('Topics', [])
        subscriptions = subscriptions_response.get('Subscriptions', [])
        
        # Count resources by type
        resource_counts = {
            'topic': len(topics),
            'subscription': len(subscriptions)
        }
        
        return {
            'service': 'sns',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
