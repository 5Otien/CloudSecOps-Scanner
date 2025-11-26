#!/usr/bin/env python3
"""
CloudSecOps Scanner - Main Scanner Module
Enterprise-grade cloud security scanning orchestrator
"""

import asyncio
import argparse
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from config import Config, load_config
from connectors.gcp_connector import GCPConnector
from connectors.aws_connector import AWSConnector
from connectors.azure_connector import AzureConnector
from scanners.iam_scanner import IAMScanner
from scanners.network_scanner import NetworkScanner
from scanners.storage_scanner import StorageScanner
from analyzers.risk_analyzer import RiskAnalyzer
from reporters.json_reporter import JSONReporter
from reporters.html_reporter import HTMLReporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScanResults:
    """Container for scan results with severity filtering"""

    def __init__(self):
        self.findings: List[Dict] = []
        self.scan_timestamp = datetime.utcnow()
        self.total_resources_scanned = 0

    def add_finding(self, finding: Dict):
        """Add a security finding"""
        self.findings.append(finding)

    @property
    def critical_findings(self) -> List[Dict]:
        return [f for f in self.findings if f['severity'] == 'critical']

    @property
    def high_findings(self) -> List[Dict]:
        return [f for f in self.findings if f['severity'] == 'high']

    @property
    def medium_findings(self) -> List[Dict]:
        return [f for f in self.findings if f['severity'] == 'medium']

    @property
    def low_findings(self) -> List[Dict]:
        return [f for f in self.findings if f['severity'] == 'low']

    def get_summary(self) -> Dict:
        """Get scan summary statistics"""
        return {
            'timestamp': self.scan_timestamp.isoformat(),
            'total_findings': len(self.findings),
            'critical': len(self.critical_findings),
            'high': len(self.high_findings),
            'medium': len(self.medium_findings),
            'low': len(self.low_findings),
            'resources_scanned': self.total_resources_scanned
        }


class CloudSecOpsScanner:
    """Main scanner orchestrator for multi-cloud security scanning"""

    def __init__(self, config: Config):
        self.config = config
        self.results = ScanResults()
        self.connector = None
        self._initialize_connector()

    def _initialize_connector(self):
        """Initialize cloud provider connector"""
        provider = self.config.provider.lower()

        if provider == 'gcp':
            self.connector = GCPConnector(self.config)
        elif provider == 'aws':
            self.connector = AWSConnector(self.config)
        elif provider == 'azure':
            self.connector = AzureConnector(self.config)
        else:
            raise ValueError(f"Unsupported cloud provider: {provider}")

        logger.info(f"Initialized {provider.upper()} connector")

    async def scan(self) -> ScanResults:
        """Execute comprehensive security scan"""
        logger.info(f"Starting security scan for {self.config.provider}")

        try:
            # Initialize scanners
            iam_scanner = IAMScanner(self.connector)
            network_scanner = NetworkScanner(self.connector)
            storage_scanner = StorageScanner(self.connector)

            # Run scans in parallel
            scan_tasks = [
                self._run_iam_scan(iam_scanner),
                self._run_network_scan(network_scanner),
                self._run_storage_scan(storage_scanner)
            ]

            findings_list = await asyncio.gather(*scan_tasks)

            # Aggregate findings
            for findings in findings_list:
                for finding in findings:
                    self.results.add_finding(finding)

            # Analyze risks
            risk_analyzer = RiskAnalyzer()
            self.results.findings = risk_analyzer.analyze(self.results.findings)

            logger.info(f"Scan completed. Found {len(self.results.findings)} issues")
            return self.results

        except Exception as e:
            logger.error(f"Scan failed: {str(e)}")
            raise

    async def _run_iam_scan(self, scanner: IAMScanner) -> List[Dict]:
        """Run IAM policy scan"""
        logger.info("Scanning IAM policies...")
        findings = await scanner.scan()
        logger.info(f"IAM scan completed: {len(findings)} findings")
        return findings

    async def _run_network_scan(self, scanner: NetworkScanner) -> List[Dict]:
        """Run network security scan"""
        logger.info("Scanning network configuration...")
        findings = await scanner.scan()
        logger.info(f"Network scan completed: {len(findings)} findings")
        return findings

    async def _run_storage_scan(self, scanner: StorageScanner) -> List[Dict]:
        """Run storage security scan"""
        logger.info("Scanning storage resources...")
        findings = await scanner.scan()
        logger.info(f"Storage scan completed: {len(findings)} findings")
        return findings

    def export_results(self, format: str = 'json', output_path: str = None):
        """Export scan results in specified format"""
        if format == 'json':
            reporter = JSONReporter()
            output = reporter.generate(self.results)
        elif format == 'html':
            reporter = HTMLReporter()
            output = reporter.generate(self.results)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(output)
            logger.info(f"Results exported to {output_path}")

        return output


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CloudSecOps Scanner - Multi-cloud security scanning tool'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Run security scan')
    scan_parser.add_argument('--provider', required=True,
                            choices=['gcp', 'aws', 'azure'],
                            help='Cloud provider')
    scan_parser.add_argument('--project-id', help='GCP project ID')
    scan_parser.add_argument('--profile', help='AWS profile name')
    scan_parser.add_argument('--subscription-id', help='Azure subscription ID')
    scan_parser.add_argument('--compliance',
                            choices=['cis-1.4', 'cis-1.5', 'gdpr', 'iso-27001'],
                            help='Compliance framework')
    scan_parser.add_argument('--severity',
                            default='critical,high,medium,low',
                            help='Severity levels to report')
    scan_parser.add_argument('--output', default='json',
                            choices=['json', 'html'],
                            help='Output format')
    scan_parser.add_argument('--report-path',
                            default='./scan-results',
                            help='Report output path')

    args = parser.parse_args()

    if args.command == 'scan':
        # Load configuration
        config = Config(
            provider=args.provider,
            project_id=args.project_id,
            aws_profile=args.profile,
            azure_subscription_id=args.subscription_id,
            compliance=args.compliance,
            severity=args.severity.split(',')
        )

        # Initialize scanner
        scanner = CloudSecOpsScanner(config)

        # Run scan
        results = await scanner.scan()

        # Print summary
        summary = results.get_summary()
        print("\n" + "="*60)
        print("SCAN SUMMARY")
        print("="*60)
        print(f"Timestamp: {summary['timestamp']}")
        print(f"Total Findings: {summary['total_findings']}")
        print(f"  Critical: {summary['critical']}")
        print(f"  High: {summary['high']}")
        print(f"  Medium: {summary['medium']}")
        print(f"  Low: {summary['low']}")
        print(f"Resources Scanned: {summary['resources_scanned']}")
        print("="*60 + "\n")

        # Export results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{args.report_path}/scan_{args.provider}_{timestamp}.{args.output}"
        scanner.export_results(format=args.output, output_path=output_file)

        print(f"Report saved to: {output_file}")

        # Exit code based on findings
        if summary['critical'] > 0:
            exit(2)
        elif summary['high'] > 0:
            exit(1)
        else:
            exit(0)
    else:
        parser.print_help()


if __name__ == '__main__':
    asyncio.run(main())
