"""CloudSecOps Scanner - Multi-cloud security scanning tool"""

__version__ = '1.0.0'
__author__ = '5Otien'

from .scanner import CloudSecOpsScanner, ScanResults
from .config import Config, load_config

__all__ = ['CloudSecOpsScanner', 'ScanResults', 'Config', 'load_config']
