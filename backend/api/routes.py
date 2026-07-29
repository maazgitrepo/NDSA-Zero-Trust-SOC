from fastapi import APIRouter
from database.connection import get_connection

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/alerts")
def create_alert(title: str, severity: str):
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


@router.get("/alerts")
def get_alerts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, severity, status, created_at "
        "FROM alerts ORDER BY id DESC"
    )

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
