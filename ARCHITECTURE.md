# معماری سامانه حضور

The project now follows a lightweight layered structure without changing the existing UI/business behavior unnecessarily.

```text
GUI Pages / Components
        |
        v
Controllers
        |
        v
Services (where file/system workflows need them)
        |
        v
Repository
        |
        v
SQLite Database
```

## Main layers

- `gui/`: PySide6 UI only.
- `controllers/`: application-facing operations used by the UI.
- `services/`: reusable workflows such as settings and backup.
- `database/`: SQLite connection, schema and repository/data access.
- `core/`: application shell and face-recognition engine.
- `settings/`: reserved package for future settings-specific components.
- `backup/`: reserved package for future backup-specific components.
- `assets/`, `theme/`: existing visual resources.

## Added features

- `Settings` page and sidebar entry.
- `Backup` page and sidebar entry.
- SQLite-backed application settings.
- Timestamped ZIP backups containing the SQLite database and `data/`.
- Configurable backup location and maximum retained backups.
- Existing pages now access their database operations through controllers.

The existing visual theme, page layouts and attendance/face-recognition logic were intentionally left in place.
