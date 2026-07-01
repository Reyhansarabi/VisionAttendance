from database.database import DatabaseManager


class SettingsRepository:
    """Repository dedicated to application settings.

    Uses the real database schema: app_settings(key, value).
    """

    def __init__(self, db=None):
        self.db = db or DatabaseManager()

    def get_all(self):
        connection = self.db.connect()
        try:
            rows = connection.execute(
                "SELECT key, value FROM app_settings ORDER BY key"
            ).fetchall()
            return {row["key"]: row["value"] for row in rows}
        finally:
            connection.close()

    def get(self, key, default=None):
        connection = self.db.connect()
        try:
            row = connection.execute(
                "SELECT value FROM app_settings WHERE key = ?",
                (key,),
            ).fetchone()
            return row["value"] if row is not None else default
        finally:
            connection.close()

    def set(self, key, value):
        connection = self.db.connect()
        try:
            connection.execute(
                """
                INSERT INTO app_settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (str(key), str(value)),
            )
            connection.commit()
            return True
        finally:
            connection.close()

    def set_many(self, values):
        connection = self.db.connect()
        try:
            connection.executemany(
                """
                INSERT INTO app_settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                [(str(k), str(v)) for k, v in values.items()],
            )
            connection.commit()
            return True
        finally:
            connection.close()
