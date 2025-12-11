"""
Configuration management for CloudSecOps Scanner
"""

from dataclasses import dataclass
from typing import List, Optional
import os
import yaml


@dataclass
class Config:
    """Scanner configuration"""

    provider: str
    project_id: Optional[str] = None
    aws_profile: Optional[str] = None
    azure_subscription_id: Optional[str] = None
    compliance: Optional[str] = None
    severity: List[str] = None

    gcp_credentials_path: str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    aws_access_key: str = os.getenv('AWS_ACCESS_KEY_ID', '')
    aws_secret_key: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    azure_tenant_id: str = os.getenv('AZURE_TENANT_ID', '')

    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///cloudsecops.db')

    slack_webhook_url: str = os.getenv('SLACK_WEBHOOK_URL', '')
    smtp_server: str = os.getenv('SMTP_SERVER', '')
    smtp_username: str = os.getenv('SMTP_USERNAME', '')
    smtp_password: str = os.getenv('SMTP_PASSWORD', '')

    def __post_init__(self):
        if self.severity is None:
            self.severity = ['critical', 'high', 'medium', 'low']


def load_config(config_path: str = 'config/config.yaml') -> Config:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            return Config(**config_data)
    except FileNotFoundError:
        return Config(provider='gcp')
