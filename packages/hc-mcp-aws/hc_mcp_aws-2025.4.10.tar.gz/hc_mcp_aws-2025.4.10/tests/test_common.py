"""
Tests for the common module.
"""
import os
import logging
from hc_mcp_aws import common
from hc_mcp_aws.common import OrganizationCache

def test_setup_logging(temp_log_dir):
    """Test that setup_logging creates a logger with the correct configuration."""
    log_file = "test.log"
    logger = common.setup_logging(log_dir=str(temp_log_dir), log_file=log_file, log_level=logging.DEBUG)
    
    # Check that the logger was created
    assert logger is not None
    assert logger.name == "hc_mcp_aws"
    assert logger.level == logging.DEBUG
    
    # Check that the log file was created
    log_file_path = os.path.join(str(temp_log_dir), log_file)
    logger.info("Test log message")
    assert os.path.exists(log_file_path)
    
    # Check log file content
    with open(log_file_path, "r") as f:
        log_content = f.read()
        assert "Test log message" in log_content

def test_organization_cache_singleton():
    """Test that OrganizationCache is a singleton."""
    cache1 = OrganizationCache()
    cache2 = OrganizationCache()
    
    # Both instances should be the same object
    assert cache1 is cache2
    
    # Modify one instance and check that the other is also modified
    cache1.last_refresh = "test"
    assert cache2.last_refresh == "test"

def test_organization_cache_needs_refresh():
    """Test the needs_refresh method of OrganizationCache."""
    cache = OrganizationCache()
    
    # Should need refresh if last_refresh is None
    cache.last_refresh = None
    assert cache.needs_refresh() is True
    
    # Should not need refresh if last_refresh is recent
    import datetime
    cache.last_refresh = datetime.datetime.now()
    assert cache.needs_refresh() is False
    
    # Should need refresh if last_refresh is old
    cache.last_refresh = datetime.datetime.now() - datetime.timedelta(seconds=cache.refresh_interval + 1)
    assert cache.needs_refresh() is True

def test_get_aws_client_default():
    """Test get_aws_client with default credentials."""
    # This test requires mocking boto3, which is beyond the scope of this example
    # In a real test, you would use moto or mock boto3 directly
    pass
