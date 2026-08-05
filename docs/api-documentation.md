# API Documentation

# NDSA Zero Trust Security Operations Center (SOC)

## Overview

The NDSA Zero Trust SOC Backend exposes RESTful APIs developed with FastAPI. These APIs allow authenticated users to create, manage, search, filter, and analyze security alerts.

**Base URL**

```
http://localhost:8001
```

---

# Authentication

Most endpoints require a valid JWT access token issued by Keycloak.

Example:

```
Authorization: Bearer <JWT_TOKEN>
```

---

# Endpoints

## 1. Create Alert

**Method**

```
POST /alerts
```

**Description**

Creates a new security alert.

**Response**

- 201 Created
- 400 Bad Request

---

## 2. Get All Alerts

**Method**

```
GET /alerts
```

**Description**

Returns all available alerts.

**Response**

- 200 OK

---

## 3. Get Alert by ID

**Method**

```
GET /alerts/{alert_id}
```

**Description**

Returns details of a single alert.

---

## 4. Update Alert

**Method**

```
PATCH /alerts/{alert_id}
```

**Description**

Updates the selected alert.

---

## 5. Delete Alert

**Method**

```
DELETE /alerts/{alert_id}
```

**Description**

Deletes an existing alert.

---

## 6. Resolve All Alerts

**Method**

```
PATCH /alerts/resolve-all
```

**Description**

Marks all open alerts as resolved.

---

## 7. Alert Statistics

**Method**

```
GET /alerts/stats
```

**Description**

Returns overall alert statistics.

---

## 8. Open Alert Count

**Method**

```
GET /alerts/open-count
```

**Description**

Returns the total number of open alerts.

---

## 9. Severity Summary

**Method**

```
GET /alerts/severity-summary
```

**Description**

Displays alert counts grouped by severity.

---

## 10. Filter Alerts

**Method**

```
GET /alerts/filter
```

**Description**

Filters alerts based on selected criteria.

---

## 11. Search by Severity

**Method**

```
GET /alerts/severity/{severity}
```

**Description**

Returns alerts matching the selected severity.

---

## 12. Search by Title

**Method**

```
GET /alerts/search/title
```

**Description**

Searches alerts using their title.

---

# Response Codes

| Code | Meaning |
|------|---------|
| 200 | Request Successful |
| 201 | Resource Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

# Testing APIs

Swagger UI

```
http://localhost:8001/docs
```

Interactive API testing can be performed directly from the Swagger interface after authenticating with a valid JWT token.

---

# Conclusion

The REST API provides secure and structured access to the Zero Trust SOC platform, enabling efficient alert management and security monitoring.
