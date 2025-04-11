"""
API Gateway resource discovery functionality.
"""
import logging
from typing import Dict, Any, Optional

from ..common import get_aws_client

logger = logging.getLogger("hc_mcp_aws")

def discover_apigateway_resources(resource_type: Optional[str], max_items: int, profile_name: Optional[str]) -> Dict[str, Any]:
    """Discover API Gateway resources."""
    apigateway = get_aws_client('apigateway', profile_name=profile_name)
    apigatewayv2 = get_aws_client('apigatewayv2', profile_name=profile_name)
    
    if not resource_type or resource_type == "rest-api":
        # Get REST APIs
        response = apigateway.get_rest_apis()
        rest_apis = response.get('items', [])
        
        # Limit to max_items
        rest_apis = rest_apis[:max_items]
        
        # Get additional information for each API
        for api in rest_apis:
            api_id = api.get('id')
            if api_id:
                try:
                    # Get stages
                    stages_response = apigateway.get_stages(restApiId=api_id)
                    stages = stages_response.get('item', [])
                    
                    # Get resources
                    resources_response = apigateway.get_resources(restApiId=api_id)
                    resources = resources_response.get('items', [])
                    
                    # Add to API
                    api['Stages'] = stages
                    api['Resources'] = resources
                    api['ResourceCount'] = len(resources)
                except Exception as e:
                    logger.warning(f"Error getting details for REST API {api_id}: {str(e)}")
                    api['Error'] = str(e)
        
        return {
            'service': 'apigateway',
            'resourceType': 'rest-api',
            'resources': rest_apis,
            'count': len(rest_apis)
        }
    
    elif resource_type == "http-api":
        # Get HTTP APIs
        response = apigatewayv2.get_apis()
        http_apis = response.get('Items', [])
        
        # Filter to only HTTP APIs
        http_apis = [api for api in http_apis if api.get('ProtocolType') == 'HTTP']
        
        # Limit to max_items
        http_apis = http_apis[:max_items]
        
        # Get additional information for each API
        for api in http_apis:
            api_id = api.get('ApiId')
            if api_id:
                try:
                    # Get stages
                    stages_response = apigatewayv2.get_stages(ApiId=api_id)
                    stages = stages_response.get('Items', [])
                    
                    # Get routes
                    routes_response = apigatewayv2.get_routes(ApiId=api_id)
                    routes = routes_response.get('Items', [])
                    
                    # Add to API
                    api['Stages'] = stages
                    api['Routes'] = routes
                    api['RouteCount'] = len(routes)
                except Exception as e:
                    logger.warning(f"Error getting details for HTTP API {api_id}: {str(e)}")
                    api['Error'] = str(e)
        
        return {
            'service': 'apigateway',
            'resourceType': 'http-api',
            'resources': http_apis,
            'count': len(http_apis)
        }
    
    elif resource_type == "websocket-api":
        # Get WebSocket APIs
        response = apigatewayv2.get_apis()
        websocket_apis = response.get('Items', [])
        
        # Filter to only WebSocket APIs
        websocket_apis = [api for api in websocket_apis if api.get('ProtocolType') == 'WEBSOCKET']
        
        # Limit to max_items
        websocket_apis = websocket_apis[:max_items]
        
        # Get additional information for each API
        for api in websocket_apis:
            api_id = api.get('ApiId')
            if api_id:
                try:
                    # Get stages
                    stages_response = apigatewayv2.get_stages(ApiId=api_id)
                    stages = stages_response.get('Items', [])
                    
                    # Get routes
                    routes_response = apigatewayv2.get_routes(ApiId=api_id)
                    routes = routes_response.get('Items', [])
                    
                    # Add to API
                    api['Stages'] = stages
                    api['Routes'] = routes
                    api['RouteCount'] = len(routes)
                except Exception as e:
                    logger.warning(f"Error getting details for WebSocket API {api_id}: {str(e)}")
                    api['Error'] = str(e)
        
        return {
            'service': 'apigateway',
            'resourceType': 'websocket-api',
            'resources': websocket_apis,
            'count': len(websocket_apis)
        }
    
    else:
        # Get multiple resource types
        rest_apis_response = apigateway.get_rest_apis()
        apis_response = apigatewayv2.get_apis()
        
        rest_apis = rest_apis_response.get('items', [])
        apis = apis_response.get('Items', [])
        
        # Split APIs by type
        http_apis = [api for api in apis if api.get('ProtocolType') == 'HTTP']
        websocket_apis = [api for api in apis if api.get('ProtocolType') == 'WEBSOCKET']
        
        # Count resources by type
        resource_counts = {
            'rest-api': len(rest_apis),
            'http-api': len(http_apis),
            'websocket-api': len(websocket_apis)
        }
        
        return {
            'service': 'apigateway',
            'resourceCounts': resource_counts,
            'totalCount': sum(resource_counts.values()),
            'availableTypes': list(resource_counts.keys())
        }
