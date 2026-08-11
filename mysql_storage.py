import datetime

import pymysql
import pymysql.cursors

from .base import SubmissionStorage

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(30),
    service VARCHAR(60),
    message TEXT NOT NULL,
    page VARCHAR(500),
    ip_address VARCHAR(64)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

INSERT_SQL = """
INSERT INTO submissions (created_at, name, email, phone, service, message, page, ip_address)
VALUES (%(created_at)s, %(name)s, %(email)s, %(phone)s, %(service)s, %(message)s, %(page)s, %(ip_address)s);
"""

SELECT_SQL = """
SELECT id, created_at, name, email, phone, service, message, page, ip_address
FROM submissions
ORDER BY id DESC
LIMIT %(limit)s;
"""


class MySQLStorage(SubmissionStorage):
    """Stores each submission as a row in a `submissions` table.

    Uses a fresh short-lived connection per call rather than a pooled
    connection, which keeps this simple and safe for typical contact-form
    traffic volumes. Swap in a connection pool (e.g. DBUtils / SQLAlchemy)
    if you expect high throughput.
    """

    def __init__(self, host, port, user, password, database):
        self._conn_kwargs = dict(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        self._ensure_table()

    def _connect(self):
        return pymysql.connect(**self._conn_kwargs)

    def _ensure_table(self):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)

    def save_submission(self, data: dict) -> str:
        row = {
            "created_at": datetime.datetime.utcnow(),
            "name": data["name"],
            "email": data["email"],
            "phone": data.get("phone", ""),
            "service": data.get("service", ""),
            "message": data["message"],
            "page": data.get("page", ""),
            "ip_address": data.get("ip_address", ""),
        }
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_SQL, row)
                return str(cur.lastrowid)

    def list_submissions(self, limit: int = 50) -> list:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_SQL, {"limit": limit})
                rows = cur.fetchall()
        for row in rows:
            if isinstance(row.get("created_at"), datetime.datetime):
                row["created_at"] = row["created_at"].isoformat()
        return rows
