"""
Tests for cloud connectors
"""
from src.connectors.gcp_connector import GCPConnector
from src.connectors.aws_connector import AWSConnector
from src.connectors.azure_connector import AzureConnector
from src.config import Config


class TestGCPConnector:
    """Test GCP connector"""

    def test_gcp_connector_init(self):
        """Test GCP connector initialization"""
        config = Config(provider='gcp', project_id='test-project')
        connector = GCPConnector(config)
        assert connector.project_id == 'test-project'
        assert connector.config.provider == 'gcp'


class TestAWSConnector:
    """Test AWS connector"""

    def test_aws_connector_init(self):
        """Test AWS connector initialization"""
        config = Config(provider='aws')
        connector = AWSConnector(config)
        assert connector.config.provider == 'aws'


class TestAzureConnector:
    """Test Azure connector"""

    def test_azure_connector_init(self):
        """Test Azure connector initialization"""
        config = Config(provider='azure')
        connector = AzureConnector(config)
        assert connector.config.provider == 'azure'
