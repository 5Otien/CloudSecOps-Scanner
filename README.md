# CloudSecOps Scanner

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-enabled-2496ED.svg)](https://www.docker.com/)

Multi-cloud security scanning and compliance automation tool for GCP, AWS, and Azure environments.

## Overview

CloudSecOps Scanner is a DevSecOps project focused on automating security assessments across cloud infrastructure. The tool performs automated scans for common misconfigurations, compliance violations, and security vulnerabilities in cloud environments.

**Current Status:** Active Development

## Features

### Security Scanning
- IAM policy analysis and privilege detection
- Network security configuration checks
- Storage bucket security assessment
- Compliance framework validation (CIS Benchmarks, GDPR)
- Automated vulnerability scanning

### Cloud Provider Support
- Google Cloud Platform (GCP)
- Amazon Web Services (AWS)
- Microsoft Azure

### DevOps Integration
- Docker containerization
- CI/CD pipeline (GitHub Actions)
- Infrastructure as Code (Terraform)
- Automated testing
- Security scanning integration

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

## Roadmap

- [ ] Enhanced compliance framework support
- [ ] Machine learning-based anomaly detection
- [ ] Auto-remediation capabilities
- [ ] Extended cloud provider coverage
- [ ] Web dashboard interface

## Contributing

Contributions are welcome. Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- New features include tests
- Documentation is updated

## License

MIT License - See [LICENSE](LICENSE) for details

## Author

**Bilal Mostefi**
Cybersecurity Engineering Student at EPITA
Email: bilal.mostefi@epita.fr
Portfolio: [portfolio-mostefi-bilal.org](https://www.portfolio-mostefi-bilal.org)

## Acknowledgments

- CIS Benchmarks for security configuration standards
- OWASP for security best practices
- Cloud Security Alliance for guidance

---

**Note:** This is an educational and development project. Use in production environments requires thorough security review and testing.
