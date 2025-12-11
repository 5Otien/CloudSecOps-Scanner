# CloudSecOps Scanner

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-enabled-2496ED.svg)](https://www.docker.com/)

Multi-cloud security scanning and compliance automation tool for GCP, AWS, and Azure environments.

## Overview

CloudSecOps Scanner is a **modular framework** for building automated security assessments across cloud infrastructure. This project provides the foundation and architecture for implementing custom security scanners that detect misconfigurations, compliance violations, and vulnerabilities in multi-cloud environments.

**Current Status:** Framework Implementation
**Project Type:** Extensible Security Scanner Architecture

> **Note:** This is a professional framework designed to be extended with custom scanning logic based on specific security requirements. The core architecture, CI/CD pipeline, testing infrastructure, and containerization are fully implemented and production-ready.

## Features

### ✅ Implemented Core Infrastructure
- **Modular Architecture** - Extensible scanner framework with clean separation of concerns
- **Multi-Cloud Connectors** - Ready-to-extend connectors for GCP, AWS, and Azure
- **Async Scanning Engine** - High-performance parallel scanning with asyncio
- **Risk Analysis Framework** - Pluggable risk scoring and severity classification
- **Multi-Format Reporting** - JSON and HTML report generation
- **Docker Containerization** - Production-ready containerized deployment
- **CI/CD Pipeline** - Automated testing, linting, and security scanning (GitHub Actions)
- **Infrastructure as Code** - Terraform templates for GCP deployment
- **Comprehensive Testing** - Unit tests with pytest and coverage reporting
- **Security Tooling** - Integrated Bandit, Safety, and Trivy scanning

### 🔧 Ready for Implementation
- **IAM Policy Analysis** - Framework ready for custom permission detection logic
- **Network Security Checks** - Connector methods prepared for firewall rule analysis
- **Storage Security Assessment** - Structure in place for bucket configuration auditing
- **Compliance Frameworks** - Extensible design for CIS, GDPR, ISO-27001 validation
- **Custom Rule Engine** - Add organization-specific security policies

## Architecture

```
CloudSecOps Scanner
├── Multi-cloud connectors (GCP, AWS, Azure)
├── Scanning engine (IAM, Network, Storage)
├── Risk analysis and scoring
├── Reporting (JSON, HTML)
└── Monitoring integration (Prometheus)
```

## Technology Stack

- **Backend:** Python 3.9+ (asyncio, aiohttp)
- **Cloud SDKs:** google-cloud-sdk, boto3, azure-sdk
- **API:** FastAPI, Pydantic
- **Container:** Docker, Docker Compose
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus, Grafana
- **Database:** PostgreSQL

## Quick Start

### Prerequisites
- Python 3.9 or higher
- Docker (optional)
- Cloud provider credentials (GCP/AWS/Azure)

### Installation

#### Using Docker
```bash
docker build -t cloudsecops-scanner .

docker run --rm \
  -e GOOGLE_APPLICATION_CREDENTIALS=/creds/gcp-key.json \
  -v $(pwd)/creds:/creds \
  cloudsecops-scanner scan --provider gcp --project-id YOUR_PROJECT
```

#### Using Python
```bash
git clone https://github.com/5Otien/CloudSecOps-Scanner.git
cd CloudSecOps-Scanner

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python src/scanner.py scan --provider gcp --project-id YOUR_PROJECT
```

### Basic Usage

```bash
# Scan GCP project
python src/scanner.py scan --provider gcp --project-id my-project

# Scan AWS account
python src/scanner.py scan --provider aws --profile production

# Scan Azure subscription
python src/scanner.py scan --provider azure --subscription-id xxx
```

## Configuration

### Environment Variables
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp-creds.json
export AWS_PROFILE=your-profile
export AZURE_SUBSCRIPTION_ID=your-subscription-id
```

### Configuration File
Create `config/config.yaml`:
```yaml
scanner:
  providers:
    - gcp
    - aws
    - azure

  compliance:
    - cis-1.4
    - gdpr

reporting:
  formats:
    - json
    - html
  output_dir: ./reports
```

## Project Structure

```
CloudSecOps-Scanner/
├── src/
│   ├── scanner.py              # Main orchestrator
│   ├── config.py               # Configuration management
│   ├── connectors/             # Cloud provider integrations
│   ├── scanners/               # Security scanners
│   ├── analyzers/              # Risk analysis
│   └── reporters/              # Report generation
├── tests/                      # Test suite
├── terraform/                  # Infrastructure as Code
├── .github/workflows/          # CI/CD pipelines
├── Dockerfile                  # Container build
├── docker-compose.yml          # Local development
└── requirements.txt            # Dependencies
```

## Extending the Framework

This project is designed to be extended with custom scanning implementations. The framework provides:

### Core Components Ready to Extend

1. **Connectors** (`src/connectors/`) - Cloud provider API integrations
   - Implement methods to fetch resources from GCP/AWS/Azure APIs
   - Use official SDKs (google-cloud-sdk, boto3, azure-sdk)

2. **Scanners** (`src/scanners/`) - Security scanning logic
   - `iam_scanner.py` - Analyze IAM policies and permissions
   - `network_scanner.py` - Check firewall rules and network configs
   - `storage_scanner.py` - Audit storage bucket security

3. **Analyzers** (`src/analyzers/`) - Risk scoring and analysis
   - Implement custom risk calculation algorithms
   - Add compliance framework checks (CIS, GDPR, ISO-27001)

4. **Reporters** (`src/reporters/`) - Output formatting
   - Extend JSON/HTML reporters with custom templates
   - Add new output formats (PDF, CSV, SARIF)

### Example: Implementing a Scanner

```python
# src/scanners/iam_scanner.py
async def scan(self) -> List[Dict]:
    findings = []
    policies = await self.connector.list_iam_policies()

    for policy in policies:
        if self._is_overly_permissive(policy):
            findings.append({
                'severity': 'critical',
                'title': 'Overly permissive IAM role detected',
                'resource_id': policy['user'],
                'recommendation': 'Apply least privilege principle'
            })

    return findings
```

## Development

### Running Tests
```bash
pip install -r requirements-dev.txt

pytest tests/ --cov=src
```

### Code Quality
```bash
flake8 src/
mypy src/
```

### Local Development Stack
```bash
docker-compose up -d
```

This starts:
- Scanner service
- PostgreSQL database
- Prometheus monitoring
- Grafana dashboards

## Deployment

### Terraform (GCP)
```bash
cd terraform/gcp

terraform init
terraform plan -var="project_id=my-project"
terraform apply
```

## CI/CD Pipeline

GitHub Actions workflow includes:
- Multi-version Python testing (3.9, 3.10, 3.11)
- Code linting and type checking
- Security scanning (Bandit, Trivy)
- Docker image build and push
- Automated testing with coverage reporting

## Extension Opportunities

This framework can be extended with:

- **Scanner Implementations** - Add actual cloud API integrations and security checks
- **Enhanced Compliance** - Implement CIS Benchmarks, NIST, HIPAA validators
- **ML-Based Detection** - Integrate anomaly detection for unusual access patterns
- **Auto-Remediation** - Add automated fix capabilities for common issues
- **Additional Providers** - Extend to Oracle Cloud, DigitalOcean, etc.
- **Web Dashboard** - Build a React/Vue frontend for visualization
- **Real-Time Monitoring** - Continuous scanning with alerting integration
- **Custom Policies** - Organization-specific security rule engines

## Contributing

Contributions are welcome. Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- New features include tests
- Documentation is updated

## License

MIT License - See [LICENSE](LICENSE) for details

## Author

**5Otien**

## Acknowledgments

- CIS Benchmarks for security configuration standards
- OWASP for security best practices
- Cloud Security Alliance for guidance

---

**Note:** This is an educational and development project. Use in production environments requires thorough security review and testing.
