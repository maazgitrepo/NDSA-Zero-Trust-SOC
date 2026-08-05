from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_connection
from auth import (
    verify_token,
    admin_required,
    analyst_required,
    viewer_required
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


# ==========================
# CREATE ALERT
# ==========================
@router.post("/alerts")
def create_alert(
    title: str,
    severity: str,
    user=Depends(analyst_required)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO alerts (title, severity) VALUES (%s, %s) RETURNING id",
        (title, severity)
    )

    alert_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": alert_id,
        "title": title,
        "severity": severity,
        "status": "open"
    }


# ==========================
# GET ALL ALERTS
# ==========================
@router.get("/alerts")
def get_alerts(user=Depends(viewer_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

# ==========================
# RESOLVE ALL ALERTS
# ==========================
@router.patch("/alerts/resolve-all")
def resolve_all_alerts(
    user=Depends(verify_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE alerts
        SET status = 'resolved'
        WHERE status = 'open'
        RETURNING id
    """)

    rows = cur.fetchall()

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "All open alerts resolved",
        "resolved_count": len(rows)
    }


# ==========================
# UPDATE ALERT STATUS
# ==========================
@router.patch("/alerts/{alert_id}")
def update_alert_status(
    alert_id: int,
    status: str,
    user=Depends(verify_token)
):
    if status not in ["open", "resolved"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be open or resolved"
        )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE alerts
        SET status=%s
        WHERE id=%s
        RETURNING id,title,severity,status
        """,
        (status, alert_id)
    )

    alert = cur.fetchone()

    if not alert:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": alert[0],
        "title": alert[1],
        "severity": alert[2],
        "status": alert[3]
    }


# ==========================
# DELETE ALERT
# ==========================
@router.delete("/alerts/{alert_id}")
def delete_alert(
    alert_id: int,
    user=Depends(admin_required)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM alerts WHERE id=%s RETURNING id",
        (alert_id,)
    )

    deleted = cur.fetchone()

    if not deleted:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Alert deleted successfully",
        "id": deleted[0]
    }


# ==========================
# ALERT STATISTICS
# ==========================
@router.get("/alerts/stats")
def alert_stats(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE status='open') AS open,
            COUNT(*) FILTER (WHERE status='resolved') AS resolved,
            COUNT(*) FILTER (WHERE severity='critical') AS critical,
            COUNT(*) FILTER (WHERE severity='high') AS high
        FROM alerts
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total": row[0],
        "open": row[1],
        "resolved": row[2],
        "critical": row[3],
        "high": row[4]
    }

# ==========================
# SEVERITY SUMMARY
# ==========================
@router.get("/alerts/severity-summary")
def severity_summary(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT severity, COUNT(*)
        FROM alerts
        GROUP BY severity
        ORDER BY severity
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }

# ==========================
# OPEN ALERT COUNT
# ==========================
@router.get("/alerts/open-count")
def open_alert_count(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE status = 'open'
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "open_alerts": count
    }

# ==========================
# RECENT ALERTS
# ==========================
@router.get("/alerts/recent")
def recent_alerts(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        ORDER BY created_at DESC
        LIMIT 5
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

# ==========================
# LATEST ALERT
# ==========================
@router.get("/alerts/latest")
def latest_alert(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        ORDER BY created_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="No alerts found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3],
        "created_at": row[4]
    }


# ==========================
# COUNT BY STATUS
# ==========================
@router.get("/alerts/count-by-status")
def count_by_status(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM alerts
        GROUP BY status
        ORDER BY status
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }

# ==========================
# COUNT BY TITLE
# ==========================
@router.get("/alerts/count-by-title")
def count_by_title(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT title, COUNT(*)
        FROM alerts
        GROUP BY title
        ORDER BY COUNT(*) DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }

# ==========================
# FILTER ALERTS BY STATUS
# ==========================
@router.get("/alerts/filter")
def filter_alerts(
    status: str,
    user=Depends(verify_token)
):
    if status not in ["open", "resolved"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be open or resolved"
        )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE status=%s
        ORDER BY id DESC
    """, (status,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]


# ==========================
# SEARCH BY SEVERITY
# ==========================
@router.get("/alerts/search")
def search_by_severity(
    severity: str,
    user=Depends(verify_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE severity=%s
        ORDER BY id DESC
    """, (severity,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

# ==========================
# GET ALERTS BY SEVERITY
# ==========================
@router.get("/alerts/severity/{severity}")
def get_alerts_by_severity(
    severity: str,
    user=Depends(verify_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE severity=%s
        ORDER BY id DESC
    """, (severity,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

# ==========================
# SEARCH BY TITLE
# ==========================
@router.get("/alerts/search/title")
def search_by_title(
    keyword: str,
    user=Depends(verify_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE title ILIKE %s
        ORDER BY id DESC
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in rows

    ]

# ==========================
# TOTAL ALERTS
# ==========================
@router.get("/alerts/total")
def total_alerts(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM alerts")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"total_alerts": total}

# ==========================
# CRITICAL ALERT COUNT
# ==========================
@router.get("/alerts/critical-count")
def critical_count(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE severity='critical'
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"critical_alerts": count}

# ==========================
# HIGH ALERT COUNT
# ==========================
@router.get("/alerts/high-count")
def high_count(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE severity='high'
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"high_alerts": count}

# ==========================
# RESOLVED ALERT COUNT
# ==========================
@router.get("/alerts/resolved-count")
def resolved_count(user=Depends(verify_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE status='resolved'
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"resolved_alerts": count}


# ==========================
# GET SINGLE ALERT
# ==========================
@router.get("/alerts/{alert_id}")
def get_alert(
    alert_id: int,
    user=Depends(verify_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE id = %s
    """, (alert_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3],
        "created_at": row[4]
    }


# ==========================
# SOC DASHBOARD
# ==========================
@router.get("/dashboard")
def dashboard(user=Depends(viewer_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_alerts,
            COUNT(*) FILTER (WHERE status='open') AS open_alerts,
            COUNT(*) FILTER (WHERE status='resolved') AS resolved_alerts,
            COUNT(*) FILTER (WHERE severity='critical') AS critical_alerts,
            COUNT(*) FILTER (WHERE severity='high') AS high_alerts
        FROM alerts
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_alerts": row[0],
        "open_alerts": row[1],
        "resolved_alerts": row[2],
        "critical_alerts": row[3],
        "high_alerts": row[4],
        "system_status": "Healthy"
    }


# ==========================
# THREAT DETECTION
# ==========================
@router.get("/threats")
def threat_detection(user=Depends(viewer_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, severity, status, created_at
        FROM alerts
        WHERE severity='critical'
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "threat_id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "detected_at": row[4]
        }
        for row in rows
    ]


# ==========================
# VULNERABILITY MANAGEMENT
# ==========================
@router.get("/vulnerabilities")
def vulnerabilities(user=Depends(viewer_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE severity='critical') AS critical,
            COUNT(*) FILTER (WHERE severity='high') AS high,
            COUNT(*) FILTER (WHERE severity='critical' AND status='open') AS unresolved_critical,
            COUNT(*) FILTER (WHERE status='resolved') AS resolved
        FROM alerts
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "critical_vulnerabilities": row[0],
        "high_vulnerabilities": row[1],
        "unresolved_critical": row[2],
        "resolved_vulnerabilities": row[3],
        "scan_status": "Completed"
    }

# ==========================
# INCIDENT RESPONSE
# ==========================
@router.get("/incident-response")
def incident_response(user=Depends(viewer_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE status='open'),
            COUNT(*) FILTER (WHERE status='resolved'),
            COUNT(*)
        FROM alerts
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "active_incidents": row[0],
        "resolved_incidents": row[1],
        "total_incidents": row[2],
        "response_status": "Operational"
    }

# ==========================
# ENDPOINT HEALTH
# ==========================
@router.get("/endpoint-health")
def endpoint_health(user=Depends(viewer_required)):
    return {
        "linux_server": "Healthy",
        "database": "Healthy",
        "backend_api": "Running",
        "frontend": "Running"
    }

# ==========================
# CONTAINER SECURITY
# ==========================
@router.get("/container-security")
def container_security(user=Depends(viewer_required)):
    return {
        "docker_status": "Secure",
        "running_containers": 3,
        "critical_findings": 0
    }

# ==========================
# NETWORK SECURITY
# ==========================
@router.get("/network-security")
def network_security(user=Depends(viewer_required)):
    return {
        "firewall": "Active",
        "ids": "Monitoring",
        "blocked_ips": 2,
        "network_status": "Secure"
    }

# ==========================
# SYSTEM STATUS
# ==========================
@router.get("/system-status")
def system_status(user=Depends(viewer_required)):
    return {
        "api": "Online",
        "database": "Online",
        "keycloak": "Online",
        "uptime": "99.9%"
    }
