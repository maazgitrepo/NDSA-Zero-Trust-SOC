# Administrator Guide

# NDSA Zero Trust Security Operations Center (SOC)

## Introduction

This guide is intended for system administrators responsible for deploying, maintaining, monitoring, and securing the NDSA Zero Trust Security Operations Center (SOC) environment. It outlines administrative responsibilities, maintenance tasks, backup procedures, and troubleshooting recommendations.

---

# Administrator Responsibilities

The administrator is responsible for:

- Managing application services
- Monitoring system health
- Maintaining PostgreSQL databases
- Managing Keycloak authentication
- Deploying Docker containers
- Managing Kubernetes resources
- Maintaining Terraform configurations
- Applying security updates
- Monitoring application logs

---

# Service Management

## Start Backend

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

## Start Frontend

```bash
cd frontend
npm run dev
```

---

## Start Docker Services

```bash
docker compose up -d
```

View running containers:

```bash
docker ps
```

Stop services:

```bash
docker compose down
```

---

# Kubernetes Administration

View cluster information:

```bash
kubectl cluster-info
```

Check cluster nodes:

```bash
kubectl get nodes
```

List all resources:

```bash
kubectl get all -A
```

View project namespace resources:

```bash
kubectl get all -n ndsa
```

---

# Terraform Administration

Initialize Terraform:

```bash
terraform init
```

Validate configuration:

```bash
terraform validate
```

Review planned changes:

```bash
terraform plan
```

Deploy infrastructure:

```bash
terraform apply
```

---

# Backup Recommendations

Administrators should regularly back up:

- PostgreSQL database
- Project source code
- Terraform state file
- Docker Compose configuration
- Kubernetes manifests

---

# Monitoring

Regularly monitor:

- Backend availability
- Database connectivity
- Docker containers
- Kubernetes pods
- Authentication services
- API health

---

# Troubleshooting

If a service becomes unavailable:

1. Verify the process is running.
2. Review application logs.
3. Restart the affected service.
4. Verify database connectivity.
5. Confirm network accessibility.

---

# Security Recommendations

- Use strong administrator credentials.
- Rotate secrets periodically.
- Protect JWT tokens.
- Keep Docker images updated.
- Restrict unnecessary network access.
- Review system logs regularly.

---

# Conclusion

Following the procedures described in this guide helps maintain a stable, secure, and reliable Zero Trust Security Operations Center environment.
