"""Employee registration controller."""
from database.repositories.user_repository import UserRepository


class RegisterController:
    def __init__(self, repository=None):
        self.repository = repository or UserRepository()

    def create_user(self, first_name, last_name, national_code, face_encoding):
        return self.repository.create_user(
            first_name, last_name, national_code, face_encoding
        )

    def get_user_by_national_code(self, national_code):
        return self.repository.get_user_by_national_code(national_code)

    def get_users(self):
        return self.repository.get_users()
