"""
Pytest configuration and fixtures for hc-mcp-aws tests.
"""
import os
import pytest
from mcp.server.fastmcp import FastMCP

@pytest.fixture
def test_server():
    """
    Create a test MCP server instance.
    """
    server = FastMCP("Test-Server")
    return server

@pytest.fixture
def temp_log_dir(tmp_path):
    """
    Create a temporary log directory.
    """
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir

@pytest.fixture
def mock_aws_credentials(monkeypatch):
    """
    Mock AWS credentials for testing.
    """
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
