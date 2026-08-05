# NDSA Zero Trust Security Operations Center (SOC)

## Project Overview

The NDSA Zero Trust SOC project is a cybersecurity platform developed to demonstrate Zero Trust Architecture using FastAPI, PostgreSQL, and Keycloak. The project provides secure REST APIs for alert management with authentication and authorization.

---

## Features

- Keycloak Authentication
- JWT Bearer Token Authorization
- Alert Management APIs
- Alert Statistics
- Open Alert Count
- Severity Summary
- Search Alerts
- Filter Alerts
- Resolve All Alerts
- Swagger API Documentation

---

## Technology Stack

- FastAPI
- PostgreSQL
- Keycloak
- Python
- Docker
- Git
- GitHub

---

## Project Structure

```
backend/
database/
api/
auth/
docs/
frontend/
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /alerts | Create Alert |
| GET | /alerts | Get All Alerts |
| GET | /alerts/{alert_id} | Get Single Alert |
| PATCH | /alerts/{alert_id} | Update Alert Status |
| PATCH | /alerts/resolve-all | Resolve All Open Alerts |
| GET | /alerts/stats | Alert Statistics |
| GET | /alerts/open-count | Open Alert Count |
| GET | /alerts/severity-summary | Severity Summary |
| GET | /alerts/filter | Filter Alerts |
| GET | /alerts/severity/{severity} | Search by Severity |
| GET | /alerts/search/title | Search by Title |
| DELETE | /alerts/{alert_id} | Delete Alert |

---

## Authentication

Authentication is implemented using Keycloak.

All protected endpoints require:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## Running the Project

1. Start PostgreSQL
2. Start Keycloak
3. Activate Python virtual environment
4. Run FastAPI

```
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

## API Documentation

Swagger UI

```
http://localhost:8001/docs
```

---

## Future Improvements

- React Dashboard
- Threat Detection Engine
- Vulnerability Management
- Incident Response Dashboard
- SIEM Integration

---

## Author

**Maaz Farrukh**

NDSA Zero Trust Security Operations Center Project
