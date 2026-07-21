"""Application settings service."""
from database.repositories.settings_repository import SettingsRepository


class SettingsService:
    DEFAULTS = {
        "app_name": "حضور",
        "app_version": "1.0.0",
        "backup_path": "backup/archives",
        "max_backups": "10",
        "work_start": "07:00",
        "work_end": "16:00",
        "grace_minutes": "15",
    }

    def __init__(self, repository=None):
        self.repository = repository or SettingsRepository()

    def get(self, key, default=None):
        value = self.repository.get(key)
        if value is None:
            return self.DEFAULTS.get(key, default)
        return value

    def set(self, key, value):
        return self.repository.set(key, value)

    def get_all(self):
        values = dict(self.DEFAULTS)
        values.update(self.repository.get_all())
        return values
