from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "healthy"}

from database.connection import get_connection

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
