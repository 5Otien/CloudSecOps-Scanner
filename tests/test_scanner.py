"""
Basic tests for CloudSecOps Scanner
"""
import pytest
from src.scanner import ScanResults, CloudSecOpsScanner
from src.config import Config


class TestScanResults:
    """Test the ScanResults class"""

    def test_scan_results_init(self):
        """Test ScanResults initialization"""
        results = ScanResults()
        assert results.findings == []
        assert results.total_resources_scanned == 0

    def test_add_finding(self):
        """Test adding a finding"""
        results = ScanResults()
        finding = {
            'severity': 'high',
            'title': 'Test finding',
            'resource_id': 'test-resource'
        }
        results.add_finding(finding)
        assert len(results.findings) == 1
        assert results.findings[0]['severity'] == 'high'

    def test_critical_findings_filter(self):
        """Test filtering critical findings"""
        results = ScanResults()
        results.add_finding({'severity': 'critical', 'title': 'Critical issue'})
        results.add_finding({'severity': 'high', 'title': 'High issue'})
        results.add_finding({'severity': 'critical', 'title': 'Another critical'})

        assert len(results.critical_findings) == 2
        assert len(results.high_findings) == 1

    def test_get_summary(self):
        """Test getting scan summary"""
        results = ScanResults()
        results.add_finding({'severity': 'critical', 'title': 'Test'})
        results.add_finding({'severity': 'high', 'title': 'Test'})
        results.add_finding({'severity': 'medium', 'title': 'Test'})

        summary = results.get_summary()
        assert summary['total_findings'] == 3
        assert summary['critical'] == 1
        assert summary['high'] == 1
        assert summary['medium'] == 1
        assert summary['low'] == 0


class TestConfig:
    """Test the Config class"""

    def test_config_creation(self):
        """Test creating a config"""
        config = Config(provider='gcp', project_id='test-project')
        assert config.provider == 'gcp'
        assert config.project_id == 'test-project'

    def test_config_default_severity(self):
        """Test default severity levels"""
        config = Config(provider='aws')
        assert 'critical' in config.severity
        assert 'high' in config.severity
        assert 'medium' in config.severity
        assert 'low' in config.severity


class TestCloudSecOpsScanner:
    """Test the main scanner class"""

    def test_scanner_init_gcp(self):
        """Test scanner initialization with GCP"""
        config = Config(provider='gcp', project_id='test')
        scanner = CloudSecOpsScanner(config)
        assert scanner.config.provider == 'gcp'
        assert scanner.connector is not None

    def test_scanner_init_aws(self):
        """Test scanner initialization with AWS"""
        config = Config(provider='aws')
        scanner = CloudSecOpsScanner(config)
        assert scanner.config.provider == 'aws'

    def test_scanner_init_azure(self):
        """Test scanner initialization with Azure"""
        config = Config(provider='azure')
        scanner = CloudSecOpsScanner(config)
        assert scanner.config.provider == 'azure'

    def test_scanner_unsupported_provider(self):
        """Test scanner with unsupported provider"""
        config = Config(provider='invalid')
        with pytest.raises(ValueError, match="Unsupported cloud provider"):
            CloudSecOpsScanner(config)
