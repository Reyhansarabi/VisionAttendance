"""Repository for auth data."""

import os
import sqlite3

from database.repositories.base_repository import BaseRepository


class AuthRepository(BaseRepository):

    """Data-access boundary for the auth domain."""

    # ==================================================
    # Profile Columns
    # ==================================================

    def _ensure_profile_columns(self):

        self._ensure_login_columns()

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

            if "profile_image" not in columns:

                connection.execute(
                    """
                    ALTER TABLE login_accounts
                    ADD COLUMN profile_image TEXT
                    """
                )

                connection.commit()

        finally:

            connection.close()

    # ==================================================
    # Get Profile
    # ==================================================

    def get_profile(
        self,
        user_id=None,
        username=None
    ):

        self._ensure_profile_columns()

        connection = self.db.connect()

        try:

            if user_id is not None:

                account = connection.execute(
                    """
                    SELECT
                        la.id,
                        la.username,
                        la.role,
                        la.user_id,
                        u.national_code AS national_code,
                        COALESCE(NULLIF(la.first_name, ''), u.first_name, '') AS first_name,
                        COALESCE(NULLIF(la.last_name, ''), u.last_name, '') AS last_name,
                        la.profile_image

                    FROM login_accounts la
                    LEFT JOIN users u ON u.id = la.user_id

                    WHERE la.user_id = ?

                    LIMIT 1
                    """,
                    (
                        user_id,
                    ),
                ).fetchone()

            else:

                account = connection.execute(
                    """
                    SELECT
                        la.id,
                        la.username,
                        la.role,
                        la.user_id,
                        u.national_code AS national_code,
                        COALESCE(NULLIF(la.first_name, ''), u.first_name, '') AS first_name,
                        COALESCE(NULLIF(la.last_name, ''), u.last_name, '') AS last_name,
                        la.profile_image

                    FROM login_accounts la
                    LEFT JOIN users u ON u.id = la.user_id

                    WHERE la.username = ?

                    LIMIT 1
                    """,
                    (
                        username,
                    ),
                ).fetchone()

            return account

        finally:

            connection.close()

    # ==================================================
    # Update Profile
    # ==================================================

    def update_profile(
        self,
        user_id,
        username,
        first_name,
        last_name,
        profile_image=None
    ):

        self._ensure_profile_columns()

        connection = self.db.connect()

        try:

            connection.execute(
                """
                UPDATE login_accounts

                SET
                    first_name = ?,
                    last_name = ?,
                    profile_image = ?

                WHERE username = ?
                """,
                (
                    first_name,
                    last_name,
                    profile_image,
                    username,
                ),
            )

            if user_id is not None:

                connection.execute(
                    """
                    UPDATE users

                    SET
                        first_name = ?,
                        last_name = ?

                    WHERE id = ?
                    """,
                    (
                        first_name,
                        last_name,
                        user_id,
                    ),
                )

            connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        except Exception as error:

            print(
                "Update profile error:",
                error
            )

            return False

        finally:

            connection.close()