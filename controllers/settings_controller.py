"""Settings controller."""
from services.settings_service import SettingsService


class SettingsController:
    def __init__(self, service=None):
        self.service = service or SettingsService()

    def get_settings(self):
        return self.service.get_all()

    def save(
        self,
        app_name,
        app_version,
        backup_path,
        max_backups,
        work_start,
        work_end,
        grace_minutes,
    ):
        values = {
            "app_name": app_name,
            "app_version": app_version,
            "backup_path": backup_path,
            "max_backups": max_backups,
            "work_start": work_start,
            "work_end": work_end,
            "grace_minutes": grace_minutes,
        }
        for key, value in values.items():
            self.service.set(key, value)
        return self.get_settings()
