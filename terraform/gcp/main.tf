terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "cloudsecops-terraform-state"
    prefix = "scanner/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "scanner" {
  name     = "cloudsecops-scanner"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/cloudsecops-scanner:latest"

        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }

        env {
          name  = "DATABASE_URL"
          value = "postgresql://${google_sql_user.scanner.name}:${random_password.db_password.result}@${google_sql_database_instance.scanner.connection_name}/${google_sql_database.scanner.name}"
        }

        env {
          name = "GOOGLE_APPLICATION_CREDENTIALS"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.gcp_credentials.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_sql_database_instance" "scanner" {
  name             = "cloudsecops-scanner-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.vpc.id
    }

    backup_configuration {
      enabled    = true
      start_time = "02:00"
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "scanner" {
  name     = "cloudsecops"
  instance = google_sql_database_instance.scanner.name
}

resource "google_sql_user" "scanner" {
  name     = "scanner"
  instance = google_sql_database_instance.scanner.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_compute_network" "vpc" {
  name                    = "cloudsecops-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "cloudsecops-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_compute_firewall" "allow_internal" {
  name    = "cloudsecops-allow-internal"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_ranges = ["10.0.0.0/24"]
}

resource "google_secret_manager_secret" "gcp_credentials" {
  secret_id = "gcp-credentials"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "gcp_credentials" {
  secret = google_secret_manager_secret.gcp_credentials.id
  secret_data = var.gcp_credentials_json
}

resource "google_service_account" "scanner" {
  account_id   = "cloudsecops-scanner"
  display_name = "CloudSecOps Scanner Service Account"
}

resource "google_project_iam_member" "scanner_viewer" {
  project = var.project_id
  role    = "roles/viewer"
  member  = "serviceAccount:${google_service_account.scanner.email}"
}

resource "google_project_iam_member" "scanner_security_reviewer" {
  project = var.project_id
  role    = "roles/iam.securityReviewer"
  member  = "serviceAccount:${google_service_account.scanner.email}"
}

output "cloud_run_url" {
  value = google_cloud_run_service.scanner.status[0].url
}

output "database_connection_name" {
  value = google_sql_database_instance.scanner.connection_name
}
