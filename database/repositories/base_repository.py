"""Shared repository implementation.

The previous monolithic repository has been split into domain repositories.
Stable database methods are retained here so behavior does not change.
"""

from datetime import datetime, time, timedelta
import sqlite3

import jdatetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database.database import DatabaseManager


class BaseRepository:
    def __init__(self, db=None):
        self.db = db or DatabaseManager()

    def connect(self):
        return self.db.connect()


class _LegacyRepositoryMethods:
    """
    Single database access layer for:
    - Users
    - Attendance
    - Attendance event logs
    - Login accounts
    - Roles
    - Password hashing
    """

    WORK_START_TIME = time(7, 30, 0)

    def __init__(self):
        self.db = DatabaseManager()

    # ==================================================
    # Dates
    # ==================================================

    @staticmethod
    def today_jalali():
        return jdatetime.datetime.now().strftime("%Y/%m/%d")

    @staticmethod
    def to_jalali(date_value):

        if not date_value:
            return ""

        if isinstance(date_value, jdatetime.date):
            return date_value.strftime("%Y/%m/%d")

        if all(
            hasattr(date_value, value)
            for value in ("year", "month", "day")
        ):
            try:
                return jdatetime.date(
                    date_value.year,
                    date_value.month,
                    date_value.day,
                ).strftime("%Y/%m/%d")

            except Exception:
                pass

        return str(date_value)

    # ==================================================
    # Users
    # ==================================================

    def get_users(self):

        connection = self.db.connect()

        try:
            return connection.execute(
                """
                SELECT *
                FROM users
                ORDER BY first_name, last_name
                """
            ).fetchall()

        finally:
            connection.close()

    def get_user_by_national_code(
        self,
        national_code
    ):

        connection = self.db.connect()

        try:
            return connection.execute(
                """
                SELECT *
                FROM users
                WHERE national_code = ?
                """,
                (national_code,),
            ).fetchone()

        finally:
            connection.close()

    def get_user_by_id(
        self,
        user_id
    ):

        connection = self.db.connect()

        try:
            return connection.execute(
                """
                SELECT *
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

        finally:
            connection.close()

    def get_user_by_name(
        self,
        first_name,
        last_name
    ):

        connection = self.db.connect()

        try:
            return connection.execute(
                """
                SELECT *
                FROM users
                WHERE first_name = ?
                AND last_name = ?
                LIMIT 1
                """,
                (
                    first_name,
                    last_name,
                ),
            ).fetchone()

        finally:
            connection.close()

    def create_user(
        self,
        first_name,
        last_name,
        national_code,
        face_encoding
    ):

        connection = self.db.connect()

        try:
            connection.execute(
                """
                INSERT INTO users
                (
                    first_name,
                    last_name,
                    national_code,
                    face_encoding
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    first_name,
                    last_name,
                    national_code,
                    face_encoding,
                ),
            )

            connection.commit()

        finally:
            connection.close()

    def get_users_count(self):

        connection = self.db.connect()

        try:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM users
                """
            ).fetchone()

            return row["total"]

        finally:
            connection.close()

    def get_work_start_time(self):
        """Return the configured work-start time, falling back to 07:00."""
        raw = self.get_setting("work_start", "07:00")
        try:
            hour, minute = str(raw).strip().split(":")[:2]
            return time(int(hour), int(minute), 0)
        except (ValueError, TypeError):
            return time(7, 0, 0)

    # ==================================================
    # Attendance Select Helper
    # ==================================================

    def _attendance_select(
        self,
        where="",
        params=(),
        order_by="attendance.date DESC, attendance.check_in ASC"
    ):

        connection = self.db.connect()

        try:

            sql = f"""
                SELECT
                    attendance.id,
                    attendance.user_id,
                    users.first_name,
                    users.last_name,
                    users.national_code,
                    attendance.date,
                    attendance.check_in,
                    attendance.check_out,
                    attendance.status

                FROM attendance

                INNER JOIN users
                    ON users.id = attendance.user_id

                {where}

                ORDER BY {order_by}
            """

            return connection.execute(
                sql,
                params
            ).fetchall()

        finally:
            connection.close()

    # ==================================================
    # Attendance - Today
    # ==================================================

    def get_today_attendance(self):

        return self._attendance_select(
            "WHERE attendance.date = ?",
            (self.today_jalali(),),
            "attendance.check_in ASC",
        )

    # ==================================================
    # Attendance - All
    # ==================================================

    def get_attendance(self):

        return self._attendance_select()

    # ==================================================
    # Attendance - User
    # ==================================================

    def get_attendance_by_user(
        self,
        user_id
    ):

        return self._attendance_select(
            "WHERE attendance.user_id = ?",
            (user_id,),
            """
            attendance.date DESC,
            attendance.check_in ASC
            """,
        )

    # ==================================================
    # Attendance - User Today
    # ==================================================

    def get_today_attendance_by_user(
        self,
        user_id
    ):

        return self._attendance_select(
            """
            WHERE attendance.user_id = ?
            AND attendance.date = ?
            """,
            (
                user_id,
                self.today_jalali(),
            ),
            "attendance.check_in ASC",
        )

    # ==================================================
    # Attendance - Date Range
    # ==================================================

    def get_attendance_between_dates(
        self,
        start_date,
        end_date,
        user_id=None
    ):

        where = """
            WHERE attendance.date >= ?
            AND attendance.date <= ?
        """

        params = [
            start_date,
            end_date,
        ]

        if user_id is not None:

            where += """
                AND attendance.user_id = ?
            """

            params.append(
                user_id
            )

        return self._attendance_select(
            where,
            tuple(params),
            """
            attendance.date DESC,
            attendance.check_in ASC
            """,
        )

    # ==================================================
    # Attendance Statistics
    # ==================================================

    def get_today_present_count(self):

        connection = self.db.connect()

        try:

            row = connection.execute(
                """
                SELECT COUNT(DISTINCT user_id) AS total

                FROM attendance

                WHERE date = ?
                AND check_in IS NOT NULL
                """,
                (
                    self.today_jalali(),
                ),
            ).fetchone()

            return row["total"]

        finally:
            connection.close()

    def get_today_absent_count(self):

        total_users = self.get_users_count()

        present_users = (
            self.get_today_present_count()
        )

        return max(
            0,
            total_users - present_users
        )

    def get_today_late_count(self):

        connection = self.db.connect()

        try:

            row = connection.execute(
                """
                SELECT COUNT(DISTINCT user_id) AS total

                FROM attendance

                WHERE date = ?
                AND status = ?
                """,
                (
                    self.today_jalali(),
                    "تاخیر",
                ),
            ).fetchone()

            return row["total"]

        finally:
            connection.close()

    # ==================================================
    # Recent Attendance
    # ==================================================

    def get_recent_attendance(
        self,
        limit=5
    ):

        connection = self.db.connect()

        try:

            return connection.execute(
                """
                SELECT
                    attendance.id,
                    attendance.user_id,
                    users.first_name,
                    users.last_name,
                    attendance.date,
                    attendance.check_in,
                    attendance.check_out,
                    attendance.status

                FROM attendance

                INNER JOIN users
                    ON users.id = attendance.user_id

                WHERE attendance.check_in IS NOT NULL

                ORDER BY attendance.id DESC

                LIMIT ?
                """,
                (
                    max(
                        1,
                        int(limit)
                    ),
                ),
            ).fetchall()

        finally:
            connection.close()

    # ==================================================
    # Weekly Attendance
    # ==================================================

    def get_weekly_attendance(self):

        connection = self.db.connect()

        try:

            today = jdatetime.date.today()

            result = []

            for offset in range(
                6,
                -1,
                -1
            ):

                current_date = (
                    today -
                    timedelta(
                        days=offset
                    )
                )

                date_string = (
                    current_date.strftime(
                        "%Y/%m/%d"
                    )
                )

                row = connection.execute(
                    """
                    SELECT COUNT(DISTINCT user_id) AS total

                    FROM attendance

                    WHERE date = ?
                    AND check_in IS NOT NULL
                    """,
                    (
                        date_string,
                    ),
                ).fetchone()

                result.append(
                    {
                        "date": date_string,
                        "weekday": current_date.weekday(),
                        "count": row["total"],
                    }
                )

            return result

        finally:
            connection.close()

    # ==================================================
    # Today's User Record
    # ==================================================

    def get_today_record(
        self,
        user_id
    ):

        connection = self.db.connect()

        try:

            return connection.execute(
                """
                SELECT *
                FROM attendance

                WHERE user_id = ?
                AND date = ?

                LIMIT 1
                """,
                (
                    user_id,
                    self.today_jalali(),
                ),
            ).fetchone()

        finally:
            connection.close()

    # ==================================================
    # Attendance Event Log
    # ==================================================

    def record_attendance_event(
        self,
        user_id,
        event_type,
        event_time=None,
        date_value=None,
        status=None
    ):

        event_time = (
            event_time
            or datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        date_value = (
            date_value
            or self.today_jalali()
        )

        connection = self.db.connect()

        try:

            connection.execute(
                """
                INSERT INTO attendance_logs
                (
                    user_id,
                    date,
                    event_type,
                    event_time,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    date_value,
                    event_type,
                    event_time,
                    status,
                ),
            )

            connection.commit()

        finally:
            connection.close()

    # ==================================================
    # Get Attendance Logs
    # ==================================================

    def get_attendance_logs(
        self,
        user_id=None,
        start_date=None,
        end_date=None
    ):

        connection = self.db.connect()

        try:

            conditions = []
            params = []

            if user_id is not None:

                conditions.append(
                    "attendance_logs.user_id = ?"
                )

                params.append(
                    user_id
                )

            if start_date:

                conditions.append(
                    "attendance_logs.date >= ?"
                )

                params.append(
                    start_date
                )

            if end_date:

                conditions.append(
                    "attendance_logs.date <= ?"
                )

                params.append(
                    end_date
                )

            if conditions:

                where = (
                    "WHERE "
                    +
                    " AND ".join(
                        conditions
                    )
                )

            else:

                where = ""

            return connection.execute(
                f"""
                SELECT
                    attendance_logs.*,
                    users.first_name,
                    users.last_name,
                    users.national_code

                FROM attendance_logs

                INNER JOIN users
                    ON users.id =
                       attendance_logs.user_id

                {where}

                ORDER BY
                    attendance_logs.date DESC,
                    attendance_logs.id DESC
                """,
                tuple(params),
            ).fetchall()

        finally:
            connection.close()

    # ==================================================
    # Register Entry
    # ==================================================

    def register_entry(
        self,
        user_id
    ):

        connection = self.db.connect()

        try:

            now = datetime.now()

            today = self.today_jalali()

            current_time = (
                now.strftime(
                    "%H:%M:%S"
                )
            )

            existing = connection.execute(
                """
                SELECT *
                FROM attendance

                WHERE user_id = ?
                AND date = ?

                LIMIT 1
                """,
                (
                    user_id,
                    today,
                ),
            ).fetchone()

            work_start = self.get_work_start_time()

            status = (
                "حاضر"
                if now.time() <= work_start
                else
                "تاخیر"
            )

            # ------------------------------------------
            # Always save the scan in raw log
            # ------------------------------------------

            connection.execute(
                """
                INSERT INTO attendance_logs
                (
                    user_id,
                    date,
                    event_type,
                    event_time,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    'entry',
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    today,
                    current_time,
                    status,
                ),
            )

            # ------------------------------------------
            # Duplicate entry
            # ------------------------------------------

            if existing:

                connection.commit()

                return {
                    "success": False,
                    "duplicate": True,
                    "record": existing,
                    "date": today,
                    "check_in": existing["check_in"],
                    "check_out": existing["check_out"],
                    "status": existing["status"],
                }

            # ------------------------------------------
            # Create final daily record
            # ------------------------------------------

            cursor = connection.execute(
                """
                INSERT INTO attendance
                (
                    user_id,
                    date,
                    check_in,
                    check_out,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    NULL,
                    ?
                )
                """,
                (
                    user_id,
                    today,
                    current_time,
                    status,
                ),
            )

            connection.commit()

            return {
                "success": True,
                "duplicate": False,
                "id": cursor.lastrowid,
                "date": today,
                "check_in": current_time,
                "check_out": None,
                "status": status,
            }

        finally:
            connection.close()

    # ==================================================
    # Register Exit
    # ==================================================

    def register_exit(
        self,
        user_id
    ):

        connection = self.db.connect()

        try:

            today = self.today_jalali()

            current_time = (
                datetime.now().strftime(
                    "%H:%M:%S"
                )
            )

            existing = connection.execute(
                """
                SELECT *
                FROM attendance

                WHERE user_id = ?
                AND date = ?

                LIMIT 1
                """,
                (
                    user_id,
                    today,
                ),
            ).fetchone()

            # ------------------------------------------
            # Exit without entry
            # ------------------------------------------

            if existing is None:

                connection.execute(
                    """
                    INSERT INTO attendance_logs
                    (
                        user_id,
                        date,
                        event_type,
                        event_time,
                        status
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        'exit_without_entry',
                        ?,
                        NULL
                    )
                    """,
                    (
                        user_id,
                        today,
                        current_time,
                    ),
                )

                connection.commit()

                return {
                    "success": False,
                    "no_entry": True,
                }

            # ------------------------------------------
            # Update final daily record
            # ------------------------------------------

            connection.execute(
                """
                UPDATE attendance

                SET check_out = ?

                WHERE id = ?
                """,
                (
                    current_time,
                    existing["id"],
                ),
            )

            # ------------------------------------------
            # Always save exit event
            # ------------------------------------------

            connection.execute(
                """
                INSERT INTO attendance_logs
                (
                    user_id,
                    date,
                    event_type,
                    event_time,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    'exit',
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    today,
                    current_time,
                    existing["status"],
                ),
            )

            connection.commit()

            return {
                "success": True,
                "no_entry": False,
                "date": today,
                "check_in": existing["check_in"],
                "check_out": current_time,
                "status": existing["status"],
            }

        finally:
            connection.close()

    # ==================================================
    # Delete User
    # ==================================================

    def delete_user(
        self,
        user_id
    ):

        connection = self.db.connect()

        try:

            connection.execute(
                """
                DELETE FROM users
                WHERE id = ?
                """,
                (
                    user_id,
                ),
            )

            connection.commit()

        finally:
            connection.close()

    # ==================================================
    # Login Columns
    # ==================================================

    def _ensure_login_columns(self):

        connection = self.db.connect()

        try:

            columns = {
                row["name"]
                for row in connection.execute(
                    """
                    PRAGMA table_info(
                        login_accounts
                    )
                    """
                ).fetchall()
            }

            additions = {
                "role":
                    "TEXT NOT NULL DEFAULT 'user'",

                "user_id":
                    "INTEGER",

                "first_name":
                    "TEXT",

                "last_name":
                    "TEXT",
            }

            changed = False

            for name, definition in additions.items():

                if name not in columns:

                    connection.execute(
                        f"""
                        ALTER TABLE login_accounts
                        ADD COLUMN {name} {definition}
                        """
                    )

                    changed = True

            if changed:
                connection.commit()

        finally:
            connection.close()

    # ==================================================
    # Login Account
    # ==================================================

    def get_login_account(
        self,
        username,
        password
    ):
        """
        Authenticate user.

        Important:
        Password is NOT compared directly in SQL.
        The stored password is a hash and is checked
        using check_password_hash().
        """

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            account = connection.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    user_id,
                    first_name,
                    last_name

                FROM login_accounts

                WHERE username = ?

                LIMIT 1
                """,
                (
                    username,
                ),
            ).fetchone()

            if account is None:
                return None

            stored_password = account["password"]

            # ------------------------------------------
            # Normal hashed password
            # ------------------------------------------

            password_is_valid = False

            try:

                password_is_valid = (
                    check_password_hash(
                        stored_password,
                        password
                    )
                )

            except Exception:

                password_is_valid = False

            # ------------------------------------------
            # Legacy plain-text password
            #
            # If an old account still contains a
            # plain password, authenticate it once
            # and immediately replace it with a hash.
            # ------------------------------------------

            if not password_is_valid:

                if stored_password == password:

                    new_hash = (
                        generate_password_hash(
                            password
                        )
                    )

                    connection.execute(
                        """
                        UPDATE login_accounts

                        SET password = ?

                        WHERE id = ?
                        """,
                        (
                            new_hash,
                            account["id"],
                        ),
                    )

                    connection.commit()

                    password_is_valid = True

            if not password_is_valid:
                return None

            # ------------------------------------------
            # Resolve user_id for old accounts
            # ------------------------------------------

            user_id = account["user_id"]

            if (
                user_id is None
                and account["first_name"]
                and account["last_name"]
            ):

                user = connection.execute(
                    """
                    SELECT id
                    FROM users

                    WHERE first_name = ?
                    AND last_name = ?

                    LIMIT 1
                    """,
                    (
                        account["first_name"],
                        account["last_name"],
                    ),
                ).fetchone()

                if user is not None:

                    user_id = user["id"]

                    connection.execute(
                        """
                        UPDATE login_accounts

                        SET user_id = ?

                        WHERE id = ?
                        """,
                        (
                            user_id,
                            account["id"],
                        ),
                    )

                    connection.commit()

            # ------------------------------------------
            # Return fresh account
            # ------------------------------------------

            return connection.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    user_id,
                    first_name,
                    last_name

                FROM login_accounts

                WHERE id = ?

                LIMIT 1
                """,
                (
                    account["id"],
                ),
            ).fetchone()

        finally:
            connection.close()

    # ==================================================
    # Create Login Account
    # ==================================================

    def create_login_account(
        self,
        username,
        password,
        role="user",
        user_id=None,
        first_name=None,
        last_name=None
    ):

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            password_hash = (
                generate_password_hash(
                    password
                )
            )

            connection.execute(
                """
                INSERT INTO login_accounts
                (
                    username,
                    password,
                    role,
                    user_id,
                    first_name,
                    last_name
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    username,
                    password_hash,
                    role,
                    user_id,
                    first_name,
                    last_name,
                ),
            )

            connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        finally:
            connection.close()

    # ==================================================
    # Username Exists
    # ==================================================

    def login_username_exists(
        self,
        username
    ):

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            row = connection.execute(
                """
                SELECT id

                FROM login_accounts

                WHERE username = ?

                LIMIT 1
                """,
                (
                    username,
                ),
            ).fetchone()

            return row is not None

        finally:
            connection.close()

    # ==================================================
    # Get Login Account By Username
    # ==================================================

    def get_login_account_by_username(
        self,
        username
    ):

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            return connection.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    user_id,
                    first_name,
                    last_name

                FROM login_accounts

                WHERE username = ?

                LIMIT 1
                """,
                (
                    username,
                ),
            ).fetchone()

        finally:
            connection.close()

    # ==================================================
    # Change Password
    # ==================================================

    def update_login_password(
        self,
        username,
        new_password
    ):
        """
        Change password for an existing account.

        The new password is always stored as a hash.
        """

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            new_password_hash = (
                generate_password_hash(
                    new_password
                )
            )

            cursor = connection.execute(
                """
                UPDATE login_accounts

                SET password = ?

                WHERE username = ?
                """,
                (
                    new_password_hash,
                    username,
                ),
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception as error:

            print(
                "Update password error:",
                error
            )

            return False

        finally:
            connection.close()

    # ==================================================
    # Verify Current Password
    # ==================================================

    def verify_login_password(
        self,
        username,
        password
    ):
        """
        Verify the current password without
        returning the password itself.
        """

        self._ensure_login_columns()

        connection = self.db.connect()

        try:

            account = connection.execute(
                """
                SELECT password

                FROM login_accounts

                WHERE username = ?

                LIMIT 1
                """,
                (
                    username,
                ),
            ).fetchone()

            if account is None:
                return False

            stored_password = account["password"]

            try:

                if check_password_hash(
                    stored_password,
                    password
                ):
                    return True

            except Exception:
                pass

            # Legacy account support.
            if stored_password == password:

                new_hash = (
                    generate_password_hash(
                        password
                    )
                )

                connection.execute(
                    """
                    UPDATE login_accounts

                    SET password = ?

                    WHERE username = ?
                    """,
                    (
                        new_hash,
                        username,
                    ),
                )

                connection.commit()

                return True

            return False

        finally:
            connection.close()

    # ==================================================
    # Update Role
    # ==================================================

    def update_login_role(
        self,
        username,
        role
    ):

        self._ensure_login_columns()

        if role not in (
            "admin",
            "user"
        ):
            return False

        connection = self.db.connect()

        try:

            cursor = connection.execute(
                """
                UPDATE login_accounts

                SET role = ?

                WHERE username = ?
                """,
                (
                    role,
                    username,
                ),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    # ==========================================================
    # Application Settings
    # ==========================================================

    def get_settings(self):
        connection = self.db.connect()
        try:
            rows = connection.execute(
                "SELECT key, value FROM app_settings ORDER BY key"
            ).fetchall()
            return {row["key"]: row["value"] for row in rows}
        finally:
            connection.close()

    def get_setting(self, key, default=None):
        connection = self.db.connect()
        try:
            row = connection.execute(
                "SELECT value FROM app_settings WHERE key = ?",
                (key,),
            ).fetchone()
            return row["value"] if row else default
        finally:
            connection.close()

    def set_setting(self, key, value):
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



# Preserve the tested legacy behavior on the new base repository.
for _name, _value in _LegacyRepositoryMethods.__dict__.items():
    if not _name.startswith("__"):
        setattr(BaseRepository, _name, _value)
