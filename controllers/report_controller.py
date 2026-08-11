"""Report controller."""
from database.repositories.report_repository import ReportRepository


class ReportController:
    def __init__(self, repository=None):
        self.repository = repository or ReportRepository()

    def get_attendance(self):
        return self.repository.get_attendance()

    def get_attendance_by_user(self, user_id):
        return self.repository.get_attendance_by_user(user_id)

    def get_attendance_between_dates(self, start_date, end_date, user_id=None):
        return self.repository.get_attendance_between_dates(
            start_date, end_date, user_id
        )

    def get_users(self):
        return self.repository.get_users()

    def create_attendance_record(
        self, user_id, date, check_in=None, check_out=None, status="حاضر"
    ):
        return self.repository.create_attendance_record(
            user_id, date, check_in, check_out, status
        )

    def update_attendance_record(
        self,
        attendance_id,
        user_id,
        date,
        check_in=None,
        check_out=None,
        status="حاضر",
    ):
        return self.repository.update_attendance_record(
            attendance_id,
            user_id,
            date,
            check_in,
            check_out,
            status,
        )

    def delete_attendance_record(self, attendance_id):
        return self.repository.delete_attendance_record(attendance_id)
