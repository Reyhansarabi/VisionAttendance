"""Backup controller."""
from services.backup_service import BackupService


class BackupController:
    def __init__(self, service=None):
        self.service = service or BackupService()

    def create_backup(self):
        return self.service.create_backup()

    def list_backups(self):
        return self.service.list_backups()

    def get_backup_directory(self):
        return self.service.get_backup_directory()
