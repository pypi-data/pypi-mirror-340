"""
DynamoDB resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

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
