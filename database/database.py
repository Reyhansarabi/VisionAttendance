"""SQLite database manager and safe schema migrations."""

import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):
        self.database_path = Path(__file__).resolve().parent / "attendance.db"
        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(str(self.database_path), timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        connection = self.connect()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    national_code TEXT UNIQUE NOT NULL,
                    face_encoding BLOB,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS login_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    user_id INTEGER,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            login_columns = {
                row["name"] for row in cursor.execute(
                    "PRAGMA table_info(login_accounts)"
                ).fetchall()
            }
            for name, definition in {
                "role": "TEXT NOT NULL DEFAULT 'user'",
                "user_id": "INTEGER",
                "first_name": "TEXT",
                "last_name": "TEXT",
            }.items():
                if name not in login_columns:
                    cursor.execute(
                        f"ALTER TABLE login_accounts ADD COLUMN {name} {definition}"
                    )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    check_in TEXT,
                    check_out TEXT,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS app_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_time TEXT NOT NULL,
                    status TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            # Backfill the audit log once from the existing final attendance table.
            cursor.execute("SELECT COUNT(*) AS total FROM attendance_logs")
            log_count = cursor.fetchone()["total"]
            if log_count == 0:
                rows = cursor.execute(
                    "SELECT user_id, date, check_in, check_out, status FROM attendance"
                ).fetchall()
                for row in rows:
                    if row["check_in"]:
                        cursor.execute(
                            """
                            INSERT INTO attendance_logs
                                (user_id, date, event_type, event_time, status)
                            VALUES (?, ?, 'entry', ?, ?)
                            """,
                            (row["user_id"], row["date"], row["check_in"], row["status"]),
                        )
                    if row["check_out"]:
                        cursor.execute(
                            """
                            INSERT INTO attendance_logs
                                (user_id, date, event_type, event_time, status)
                            VALUES (?, ?, 'exit', ?, ?)
                            """,
                            (row["user_id"], row["date"], row["check_out"], row["status"]),
                        )

            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_attendance_user_date ON attendance(user_id, date)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_user_date ON attendance_logs(user_id, date)"
            )

            connection.commit()
        finally:
            connection.close()
