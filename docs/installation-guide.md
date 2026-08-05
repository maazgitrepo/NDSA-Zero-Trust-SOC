# Installation Guide`

# NDSA Zero Trust Security Operations Center (SOC)

## Introduction

This document describes the complete installation procedure for the NDSA Zero Trust Security Operations Center (SOC) project. The application consists of a FastAPI backend, React frontend, PostgreSQL database, Keycloak Identity Provider, Docker services, Kubernetes manifests, and Terraform infrastructure configuration.

---

# System Requirements

Before installing the project, ensure the following software is available on the system.

| Component | Version |
|------------|----------|
| CentOS Stream | 9 |
| Python | 3.11+ |
| Node.js | Latest LTS |
| PostgreSQL | 16 |
| Docker | Installed |
| Docker Compose | Installed |
| Git | Installed |
| Kubernetes (Minikube) | Installed |
| Terraform | Installed |

---

# Clone the Repository

```bash
git clone <repository-url>
cd NDSA-Zero-Trust-SOC
```

---

# Backend Installation

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python3 -m venv .venv
```

Activate the virtual environment.

```bash
source .venv/bin/activate
```

Install all required Python packages.

```bash
pip install -r requirements.txt
```

---

# Frontend Installation

Navigate to the frontend directory.

```bash
cd frontend
```

Install all required Node.js packages.

```bash
npm install
```

---

# Database Installation

The project uses PostgreSQL through Docker Compose.

Start all required services.

```bash
docker compose up -d
```

---

# Keycloak Configuration

Keycloak is automatically deployed using Docker Compose.

Default URL:

```
http://localhost:8081
```

Create the required Realm, Client, and Users before using protected APIs.

---

# Running the Backend

Navigate to the backend directory.

```bash
cd backend
```

Activate the virtual environment.

```bash
source .venv/bin/activate
```

Run the FastAPI server.

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

# Running the Frontend

Navigate to the frontend directory.

```bash
cd frontend
```

Start the development server.

```bash
npm run dev
```

---

# Verifying the Installation

Backend API Documentation

```
http://localhost:8001/docs
```

Frontend

```
http://localhost:5173
```

Keycloak

```
http://localhost:8081
```

---

# Troubleshooting

If the backend fails to start:

- Verify PostgreSQL is running.
- Verify Docker containers are active.
- Check Python dependencies.
- Confirm the virtual environment is activated.

If the frontend fails:

- Verify Node.js packages are installed.
- Run:

```bash
npm install
```

---

# Conclusion

After completing these steps, the NDSA Zero Trust SOC environment is ready for development, testing, and deployment.
