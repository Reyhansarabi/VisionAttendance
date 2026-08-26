"""Dashboard controller."""
from database.repositories.dashboard_repository import DashboardRepository


class DashboardController:
    def __init__(self, repository=None):
       self.repository = repository or DashboardRepository()

    def get_users_count(self):
        return self.repository.get_users_count()

    def get_today_present_count(self):
        return self.repository.get_today_present_count()

    def get_today_absent_count(self):
        return self.repository.get_today_absent_count()

    def get_today_late_count(self):
        return self.repository.get_today_late_count()

    def get_today_record(self, user_id):
        return self.repository.get_today_record(user_id)

    def get_recent_attendance(self, limit=5):
        return self.repository.get_recent_attendance(limit)

    def get_weekly_attendance(self):
        return self.repository.get_weekly_attendance()

    def get_users(self):
        return self.repository.get_users()
