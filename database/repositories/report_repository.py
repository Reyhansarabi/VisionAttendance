"""Repository for report data."""
from database.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository):
    """Data-access boundary for the report domain."""

    def create_attendance_record(
        self,
        user_id,
        date,
        check_in=None,
        check_out=None,
        status="حاضر",
    ):
        connection = self.db.connect()
        try:
            existing = connection.execute(
                """
                SELECT id
                FROM attendance
                WHERE user_id = ? AND date = ?
                LIMIT 1
                """,
                (user_id, date),
            ).fetchone()

            if existing is not None:
                return {
                    "success": False,
                    "reason": "duplicate",
                    "id": existing["id"],
                }

            cursor = connection.execute(
                """
                INSERT INTO attendance
                    (user_id, date, check_in, check_out, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, date, check_in, check_out, status),
            )

            attendance_id = cursor.lastrowid

            # Keep the existing audit-log design consistent with normal attendance.
            if check_in:
                connection.execute(
                    """
                    INSERT INTO attendance_logs
                        (user_id, date, event_type, event_time, status)
                    VALUES (?, ?, 'entry', ?, ?)
                    """,
                    (user_id, date, check_in, status),
                )

            if check_out:
                connection.execute(
                    """
                    INSERT INTO attendance_logs
                        (user_id, date, event_type, event_time, status)
                    VALUES (?, ?, 'exit', ?, ?)
                    """,
                    (user_id, date, check_out, status),
                )

            connection.commit()
            return {
                "success": True,
                "id": attendance_id,
            }

        finally:
            connection.close()

    def update_attendance_record(
        self,
        attendance_id,
        user_id,
        date,
        check_in=None,
        check_out=None,
        status="حاضر",
    ):
        connection = self.db.connect()
        try:
            existing = connection.execute(
                """
                SELECT id
                FROM attendance
                WHERE id = ?
                LIMIT 1
                """,
                (attendance_id,),
            ).fetchone()

            if existing is None:
                return False

            duplicate = connection.execute(
                """
                SELECT id
                FROM attendance
                WHERE user_id = ?
                  AND date = ?
                  AND id <> ?
                LIMIT 1
                """,
                (user_id, date, attendance_id),
            ).fetchone()

            if duplicate is not None:
                return False

            connection.execute(
                """
                UPDATE attendance
                SET user_id = ?,
                    date = ?,
                    check_in = ?,
                    check_out = ?,
                    status = ?
                WHERE id = ?
                """,
                (
                    user_id,
                    date,
                    check_in,
                    check_out,
                    status,
                    attendance_id,
                ),
            )

            # Rebuild audit entries for this attendance day/user so corrections
            # made by the administrator are reflected in the log.
            connection.execute(
                """
                DELETE FROM attendance_logs
                WHERE user_id = ? AND date = ?
                """,
                (user_id, date),
            )

            if check_in:
                connection.execute(
                    """
                    INSERT INTO attendance_logs
                        (user_id, date, event_type, event_time, status)
                    VALUES (?, ?, 'entry', ?, ?)
                    """,
                    (user_id, date, check_in, status),
                )

            if check_out:
                connection.execute(
                    """
                    INSERT INTO attendance_logs
                        (user_id, date, event_type, event_time, status)
                    VALUES (?, ?, 'exit', ?, ?)
                    """,
                    (user_id, date, check_out, status),
                )

            connection.commit()
            return True

        finally:
            connection.close()

    def delete_attendance_record(self, attendance_id):
        connection = self.db.connect()
        try:
            row = connection.execute(
                """
                SELECT user_id, date
                FROM attendance
                WHERE id = ?
                LIMIT 1
                """,
                (attendance_id,),
            ).fetchone()

            if row is None:
                return False

            connection.execute(
                """
                DELETE FROM attendance
                WHERE id = ?
                """,
                (attendance_id,),
            )

            connection.execute(
                """
                DELETE FROM attendance_logs
                WHERE user_id = ? AND date = ?
                """,
                (row["user_id"], row["date"]),
            )

            connection.commit()
            return True

        finally:
            connection.close()
