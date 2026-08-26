from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
)
from PySide6.QtCore import Qt

from theme.fonts import Fonts
from theme.colors import Colors
from gui.components.glass_card import GlassCard
from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton

from controllers.backup_controller import BackupController


class BackupPage(QWidget):
    """Manual database/data backup page."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = BackupController()

        self.setup_ui()
        self.refresh_backups()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        card = GlassCard()

        # عنوان
        title = QLabel("پشتیبان‌گیری")
        title.setFont(Fonts.heading())
        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.TEXT};
                background: transparent;
                border: none;
            }}
            """
        )
        card.layout.addWidget(title)

        # توضیحات
        description = QLabel(
            "از اطلاعات پایگاه داده و داده‌های برنامه یک نسخه پشتیبان فشرده تهیه کنید."
        )
        description.setStyleSheet(
            """
            QLabel {
                color: #64748B;
                background: transparent;
                border: none;
            }
            """
        )
        card.layout.addWidget(description)

        # دکمه‌ها
        actions = QHBoxLayout()
        actions.setSpacing(8)

        # ایجاد پشتیبان
        create = PrimaryButton("ایجاد پشتیبان")
        create.setFixedHeight(40)
        create.clicked.connect(self.create_backup)

        # باز کردن پوشه
        open_folder = SecondaryButton("باز کردن پوشه")
        open_folder.setFixedHeight(40)
        open_folder.clicked.connect(self.open_folder)

        # بروزرسانی لیست
        refresh = SecondaryButton("بروزرسانی")
        refresh.setFixedHeight(40)
        refresh.clicked.connect(self.refresh_backups)

        actions.addWidget(create)
        actions.addWidget(open_folder)
        actions.addWidget(refresh)
        actions.addStretch()

        card.layout.addLayout(actions)

        # لیست پشتیبان‌ها
        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet(
            """
            QListWidget {
                background: white;
                border: 1px solid #D9E3EE;
                border-radius: 10px;
                color: #334155;
                padding: 6px;
            }

            QListWidget::item {
                padding: 8px;
            }

            QListWidget::item:selected {
                background: #EEF4FF;
                color: #2B6EDB;
            }
            """
        )

        card.layout.addWidget(self.backup_list, 1)

        layout.addWidget(card)

    def refresh_backups(self):
        """Refresh the list of available backup files."""

        try:
            self.backup_list.clear()

            backups = self.controller.list_backups()

            if not backups:
                self.backup_list.addItem(
                    "هنوز نسخه پشتیبانی ایجاد نشده است."
                )
                return

            for item in backups:
                self.backup_list.addItem(item.name)

        except Exception as error:
            self.backup_list.clear()

            self.backup_list.addItem(
                f"خطا در خواندن پشتیبان‌ها: {error}"
            )

    def create_backup(self):
        """Create a new backup."""

        try:
            target = self.controller.create_backup()

            # Refresh the list after creating the backup
            self.refresh_backups()

            QMessageBox.information(
                self,
                "پشتیبان‌گیری",
                f"نسخه پشتیبان با موفقیت ایجاد شد.\n\n{target}",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "خطا",
                f"ایجاد نسخه پشتیبان انجام نشد:\n{error}",
            )

    def open_folder(self):
        """Open the backup directory in Windows Explorer."""

        try:
            path = self.controller.get_backup_directory()

            import os

            os.startfile(str(path))

        except Exception as error:
            QMessageBox.warning(
                self,
                "پشتیبان‌گیری",
                f"باز کردن پوشه انجام نشد:\n{error}",
            )