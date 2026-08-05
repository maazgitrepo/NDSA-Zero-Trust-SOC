# User Guide

# NDSA Zero Trust Security Operations Center (SOC)

## Introduction

The NDSA Zero Trust SOC platform enables security analysts to monitor, manage, and respond to security alerts through a centralized interface. This guide explains the basic operations that an end user can perform within the system.

---

# Accessing the Application

Before using the application, ensure the backend, frontend, PostgreSQL, and Keycloak services are running.

Default URLs:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8001 |
| Swagger UI | http://localhost:8001/docs |
| Keycloak | http://localhost:8081 |

---

# Authentication

Users must authenticate through Keycloak before accessing protected API endpoints.

After successful authentication, a JWT access token is issued and must be included in API requests.

---

# Managing Security Alerts

Users can perform the following operations:

- View all alerts
- Create new alerts
- Search alerts by title
- Filter alerts by severity
- Update alert status
- Delete alerts
- Resolve all open alerts

---

# Viewing Statistics

The platform provides security monitoring features including:

- Total Alerts
- Open Alert Count
- Severity Summary
- Alert Statistics

These features help security analysts quickly understand the current security posture.

---

# API Testing

The application provides an interactive Swagger interface.

```
http://localhost:8001/docs
```

Users can test API endpoints directly from the browser after authentication.

---

# Best Practices

- Always authenticate before accessing protected APIs.
- Use strong credentials for administrative accounts.
- Review alerts regularly.
- Resolve completed incidents promptly.
- Verify alert severity before taking action.

---

# Troubleshooting

If the application cannot be accessed:

- Verify Docker containers are running.
- Confirm PostgreSQL is available.
- Ensure Keycloak is operational.
- Check that the FastAPI backend is running.

---

# Conclusion

The NDSA Zero Trust SOC platform provides a secure and user-friendly environment for managing cybersecurity alerts while following Zero Trust security principles.
