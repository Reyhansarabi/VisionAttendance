"""Safe local backup service for حضور."""
from datetime import datetime
from pathlib import Path
import json
import shutil
import tempfile
import zipfile

from services.settings_service import SettingsService


class BackupService:
    def __init__(self, project_root=None, settings_service=None):
        self.root = Path(project_root or Path(__file__).resolve().parents[1])
        self.settings = settings_service or SettingsService()

    def get_backup_directory(self):
        configured = str(
            self.settings.get("backup_path", "backup/archives")
        ).strip()
        path = Path(configured)
        if not path.is_absolute():
            path = self.root / path
        path.mkdir(parents=True, exist_ok=True)
        return path

    def create_backup(self):
        """Create a timestamped ZIP containing application data."""
        backup_dir = self.get_backup_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = backup_dir / f"VisionAttendance_backup_{timestamp}.zip"

        database_file = self.root / "database" / "attendance.db"
        data_dir = self.root / "data"

        if not database_file.exists():
            raise FileNotFoundError("فایل پایگاه داده پیدا نشد.")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copy2(database_file, temp_root / "attendance.db")

            if data_dir.exists():
                shutil.copytree(data_dir, temp_root / "data", dirs_exist_ok=True)

            manifest = {
                "application": "حضور",
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "contents": ["database/attendance.db", "data/"],
            }
            (temp_root / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            with zipfile.ZipFile(
                target, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                for item in temp_root.rglob("*"):
                    if item.is_file():
                        archive.write(item, item.relative_to(temp_root))

        self.cleanup_old_backups()
        return target

    def cleanup_old_backups(self):
        try:
            max_backups = max(1, int(self.settings.get("max_backups", "10")))
        except (TypeError, ValueError):
            max_backups = 10

        backups = sorted(
            self.get_backup_directory().glob("VisionAttendance_backup_*.zip"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for old_file in backups[max_backups:]:
            try:
                old_file.unlink()
            except OSError:
                pass

    def list_backups(self):
        return sorted(
            self.get_backup_directory().glob("VisionAttendance_backup_*.zip"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def open_backup_directory(self):
        path = self.get_backup_directory()
        return path
