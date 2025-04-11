"""
Common utilities and classes for the HC MCP AWS server.
"""
import os
import logging
import datetime
import boto3
from logging.handlers import RotatingFileHandler

# Version in YYYY.MM.DD format
VERSION = "2025.04.10"

def setup_logging(log_dir="logs", log_file="hc_mcp_aws.log", log_level=logging.INFO):
    """
    Set up logging for the HC MCP AWS server.
    
    Args:
        log_dir (str): Directory to store log files
        log_file (str): Name of the log file
        log_level (int): Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logger
    logger = logging.getLogger("hc_mcp_aws")
    logger.setLevel(log_level)
    
    # Clear existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create file handler with rotation
    log_path = os.path.join(log_dir, log_file)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=5*1024*1024, backupCount=5
    )
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger

def get_aws_client(service_name, region_name=None, profile_name=None):
    """
    Get an AWS client for the specified service.
    
    Args:
        service_name (str): AWS service name (e.g., 'ec2', 's3')
        region_name (str, optional): AWS region name
        profile_name (str, optional): AWS profile name
        
    Returns:
        boto3.client: AWS client
    """
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    return session.client(service_name)

class OrganizationCache:
    """
    Singleton class to cache AWS Organization structure.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrganizationCache, cls).__new__(cls)
            cls._instance.accounts = {}
            cls._instance.organizational_units = {}
            cls._instance.last_refresh = None
            cls._instance.refresh_interval = 3600  # 1 hour
        return cls._instance
    
    def needs_refresh(self):
        """Check if the cache needs to be refreshed."""
        if self.last_refresh is None:
            return True
        
        now = datetime.datetime.now()
        elapsed = (now - self.last_refresh).total_seconds()
        return elapsed > self.refresh_interval
    
    def refresh(self, force=False):
        """
        Refresh the organization cache.
        
        Args:
            force (bool): Force refresh even if not needed
            
        Returns:
            bool: True if refreshed, False otherwise
        """
        if not force and not self.needs_refresh():
            return False
        
        logger = logging.getLogger("hc_mcp_aws")
        logger.info("Refreshing organization cache")
        
        try:
            # Get organization client
            org_client = get_aws_client('organizations')
            
            # Get all accounts
            accounts = []
            paginator = org_client.get_paginator('list_accounts')
            for page in paginator.paginate():
                accounts.extend(page['Accounts'])
            
            # Update accounts cache
            self.accounts = {
                account['Id']: account for account in accounts
            }
            
            # Get all organizational units
            ous = []
            roots = org_client.list_roots()['Roots']
            
            for root in roots:
                root_id = root['Id']
                ous.append({
                    'Id': root_id,
                    'Name': 'Root',
                    'Path': '/'
                })
                
                # Get all OUs recursively
                self._get_ous_recursive(org_client, root_id, '/', ous)
            
            # Update OUs cache
            self.organizational_units = {
                ou['Id']: ou for ou in ous
            }
            
            self.last_refresh = datetime.datetime.now()
            logger.info(f"Organization cache refreshed with {len(self.accounts)} accounts and {len(self.organizational_units)} OUs")
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing organization cache: {e}")
            return False
    
    def _get_ous_recursive(self, client, parent_id, parent_path, ous_list):
        """
        Recursively get all OUs under a parent.
        
        Args:
            client: AWS organizations client
            parent_id (str): Parent OU ID
            parent_path (str): Parent OU path
            ous_list (list): List to append OUs to
        """
        paginator = client.get_paginator('list_organizational_units_for_parent')
        
        for page in paginator.paginate(ParentId=parent_id):
            for ou in page['OrganizationalUnits']:
                ou_path = f"{parent_path}{ou['Name']}/"
                ou_info = {
                    'Id': ou['Id'],
                    'Name': ou['Name'],
                    'Path': ou_path
                }
                ous_list.append(ou_info)
                
                # Recursively get child OUs
                self._get_ous_recursive(client, ou['Id'], ou_path, ous_list)
    
    def get_account_by_id(self, account_id):
        """Get account details by ID."""
        return self.accounts.get(account_id)
    
    def get_account_by_name(self, account_name):
        """Get account details by name."""
        for account in self.accounts.values():
            if account['Name'] == account_name:
                return account
        return None
    
    def get_accounts_in_ou(self, ou_path):
        """Get all accounts in an OU."""
        # Find the OU ID from path
        ou_id = None
        for ou in self.organizational_units.values():
            if ou['Path'] == ou_path:
                ou_id = ou['Id']
                break
        
        if not ou_id:
            return []
        
        # Get accounts in this OU
        try:
            org_client = get_aws_client('organizations')
            accounts = []
            paginator = org_client.get_paginator('list_accounts_for_parent')
            
            for page in paginator.paginate(ParentId=ou_id):
                accounts.extend(page['Accounts'])
            
            return accounts
        except Exception:
            return []
