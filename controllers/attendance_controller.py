"""Attendance application controller.

Keeps the UI independent from the database implementation.
"""
from database.repositories.attendance_repository import AttendanceRepository


class AttendanceController:
    def __init__(self, repository=None):
        self.repository = repository or AttendanceRepository()

    def get_users(self):
        return self.repository.get_users()

    def register_entry(self, user_id):
        return self.repository.register_entry(user_id)

    def register_exit(self, user_id):
        return self.repository.register_exit(user_id)

    def get_today_record(self, user_id):
        return self.repository.get_today_record(user_id)

    def get_today_attendance(self):
        return self.repository.get_today_attendance()

    def get_attendance_logs(self, user_id=None, start_date=None, end_date=None):
        return self.repository.get_attendance_logs(user_id, start_date, end_date)
