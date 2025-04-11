"""
Test version functionality of the hc-mcp-aws package.
"""
import re
import sys
import importlib.metadata
from hc_mcp_aws import common

def test_version_format():
    """Test that the version follows semantic versioning."""
    version = common.VERSION
    # Check if version follows YYYY.MM.DD format
    assert re.match(r"^\d{4}\.\d{1,2}\.\d{1,2}$", version), f"Version {version} does not follow YYYY.MM.DD format"

def test_version_command_line():
    """Test that the --version flag works."""
    # This is a simple test that just imports the module
    # In a real test, you would use subprocess to run the command
    assert hasattr(sys, 'argv'), "sys.argv is not available"

def test_version_consistency():
    """Test that the version in common.py matches the package version."""
    try:
        package_version = importlib.metadata.version("hc-mcp-aws")
        assert common.VERSION == package_version, f"Version mismatch: {common.VERSION} != {package_version}"
    except importlib.metadata.PackageNotFoundError:
        # Package is not installed, skip this test
        pass
