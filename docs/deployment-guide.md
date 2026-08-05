# Deployment Guide

# NDSA Zero Trust Security Operations Center (SOC)

## Overview

This document explains how the NDSA Zero Trust SOC project is deployed using Docker Compose, Kubernetes, and Terraform. The deployment process is designed to provide a consistent and repeatable environment for development and testing.

---

# Deployment Architecture

The project consists of the following components:

- FastAPI Backend
- React Frontend
- PostgreSQL Database
- Keycloak Authentication Server
- Docker Compose Services
- Kubernetes Resources
- Terraform Infrastructure

---

# Docker Deployment

Docker Compose is used to start the required application services.

Start all services:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

Stop services:

```bash
docker compose down
```

---

# Kubernetes Deployment

Kubernetes manifests are stored inside the **kubernetes/** directory.

Deploy all resources:

```bash
kubectl apply -f kubernetes/
```

Verify deployment:

```bash
kubectl get all -n ndsa
```

Check pods:

```bash
kubectl get pods -n ndsa
```

View service information:

```bash
kubectl get svc -n ndsa
```

---

# Terraform Deployment

Terraform is used for Infrastructure as Code (IaC).

Initialize Terraform:

```bash
terraform init
```

Validate configuration:

```bash
terraform validate
```

Preview infrastructure changes:

```bash
terraform plan
```

Apply configuration:

```bash
terraform apply
```

---

# Deployment Verification

Confirm the following services are accessible:

| Service | Default Port |
|----------|-------------:|
| FastAPI | 8001 |
| PostgreSQL | 5432 |
| Keycloak | 8081 |
| Frontend | 5173 |

---

# Maintenance

To monitor the deployment:

Docker

```bash
docker ps
```

Kubernetes

```bash
kubectl get nodes
kubectl get pods -A
```

Terraform

```bash
terraform state list
```

---

# Rollback

If deployment fails:

- Stop Docker services.
- Remove failed Kubernetes resources.
- Restore the previous Terraform state if required.
- Redeploy after resolving the issue.

---

# Conclusion

The deployment process ensures that all application components are configured consistently and can be reproduced whenever required.
