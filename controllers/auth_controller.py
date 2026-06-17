"""Authentication controller."""

from database.repositories.auth_repository import AuthRepository


class AuthController:

    def __init__(
        self,
        repository=None
    ):

        self.repository = (
            repository
            or AuthRepository()
        )

    # ==================================================
    # Login
    # ==================================================

    def login(
        self,
        username,
        password
    ):

        return self.repository.get_login_account(
            username,
            password
        )

    def get_login_account(
        self,
        username,
        password
    ):

        return self.repository.get_login_account(
            username,
            password
        )

    def login_username_exists(
        self,
        username
    ):

        return self.repository.login_username_exists(
            username
        )

    def get_login_account_by_username(
        self,
        username
    ):

        return self.repository.get_login_account_by_username(
            username
        )

    def create_login_account(
        self,
        username,
        password,
        role="user",
        user_id=None,
        first_name=None,
        last_name=None
    ):

        return self.repository.create_login_account(
            username,
            password,
            role,
            user_id,
            first_name,
            last_name
        )

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(
        self,
        user_id=None,
        username=None
    ):

        return self.repository.get_profile(
            user_id,
            username
        )

    def update_profile(
        self,
        user_id,
        username,
        first_name,
        last_name,
        profile_image=None
    ):

        return self.repository.update_profile(
            user_id,
            username,
            first_name,
            last_name,
            profile_image
        )

