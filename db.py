import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

DB_PATH = os.getenv("DB_PATH", "urls.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS request_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                method TEXT NOT NULL,
                path TEXT NOT NULL,
                status_code INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def create_link(code: str, url: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO links(code, url, clicks, created_at) VALUES(?, ?, 0, ?)",
            (code, url, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()


def get_link(code: str):
    with get_connection() as conn:
        row = conn.execute("SELECT code, url, clicks, created_at FROM links WHERE code = ?", (code,)).fetchone()
        return dict(row) if row else None


def increment_click(code: str) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
        conn.commit()


def total_links() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM links").fetchone()
        return int(row["c"])


def total_clicks() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COALESCE(SUM(clicks), 0) AS c FROM links").fetchone()
        return int(row["c"])


def top_links(limit: int = 5):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT code, url, clicks FROM links ORDER BY clicks DESC, created_at ASC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def log_request_metric(method: str, path: str, status_code: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO request_metrics(ts, method, path, status_code) VALUES(?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), method, path, int(status_code)),
        )
        conn.commit()


def requests_per_minute_last_hour():
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT substr(ts, 1, 16) AS minute, COUNT(*) AS requests
            FROM request_metrics
            WHERE ts >= ?
            GROUP BY substr(ts, 1, 16)
            ORDER BY minute ASC
            """,
            (cutoff,),
        ).fetchall()
        return [dict(r) for r in rows]
