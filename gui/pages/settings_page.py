from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFileDialog,
    QSpinBox,
    QTimeEdit,
    QMessageBox,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QPixmap

from theme.fonts import Fonts
from theme.colors import Colors
from gui.components.glass_card import GlassCard
from gui.components.rounded_input import RoundedLineEdit
from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton

from controllers.settings_controller import SettingsController


class SettingsPage(QWidget):
    """Application settings page."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = SettingsController()

        self.setup_ui()
        self.load_settings()

    def _label(self, text, muted=False, size=12):
        label = QLabel(text)

        label.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.MUTED if muted else Colors.TEXT};
                background: transparent;
                border: none;
                font-size: {size}px;
            }}
            """
        )

        return label

    def _section_title(self, text):
        label = self._label(text, size=13)
        label.setFont(Fonts.button())
        return label

    def _time_edit(self):
        edit = QTimeEdit()

        edit.setDisplayFormat("HH:mm")
        edit.setFixedHeight(36)
        edit.setTime(QTime(7, 0))

        edit.setStyleSheet(
            """
            QTimeEdit {
                background: white;
                border: 1px solid #D9E3EE;
                border-radius: 10px;
                padding: 5px 9px;
                color: #334155;
                font-size: 12px;
            }

            QTimeEdit:focus {
                border: 1px solid #5699D7;
            }
            """
        )

        return edit

    def _spinbox_style(self):
        return """
        QSpinBox {
            background: white;
            border: 1px solid #D9E3EE;
            border-radius: 10px;
            padding: 5px 9px;
            color: #334155;
            font-size: 12px;
        }

        QSpinBox:focus {
            border: 1px solid #5699D7;
        }
        """

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # صفحه تنظیمات از محتوای نسبتاً بلندی تشکیل شده است.
        # اسکرول عمودی باعث می‌شود در اندازه‌های مختلف پنجره،
        # هیچ عنوان یا فیلدی بریده نشود.
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                width: 7px;
                background: transparent;
                margin: 4px 1px 4px 1px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        card = GlassCard()
        card.setMinimumWidth(0)
        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------

        header = QHBoxLayout()
        header.setSpacing(12)

        logo = QLabel()
        logo.setFixedSize(54, 54)
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
            }
            """
        )

        pixmap = QPixmap("assets/logo1.png")

        if not pixmap.isNull():
            logo.setPixmap(
                pixmap.scaled(
                    54,
                    54,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        header_text = QVBoxLayout()
        header_text.setSpacing(1)

        title = QLabel("حضور")
        title.setFont(Fonts.heading())

        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.TEXT};
                background: transparent;
                border: none;
                font-size: 18px;
            }}
            """
        )

        subtitle = QLabel("سیستم هوشمند حضور و غیاب")

        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.MUTED};
                background: transparent;
                border: none;
                font-size: 11px;
            }}
            """
        )

        header_text.addWidget(title)
        header_text.addWidget(subtitle)

        header.addWidget(logo)
        header.addLayout(header_text)
        header.addStretch()

        card.layout.addLayout(header)

        card.layout.addSpacing(7)

        # ---------------------------------------------------------
        # Description
        # ---------------------------------------------------------

        description = self._label(
            "اطلاعات عمومی برنامه، ساعت کاری و تنظیمات پشتیبان‌گیری را مدیریت کنید.",
            muted=True,
            size=11,
        )
        description.setWordWrap(True)

        card.layout.addWidget(description)

        card.layout.addSpacing(9)

        # ---------------------------------------------------------
        # Application Information
        # ---------------------------------------------------------

        info_title = self._section_title("اطلاعات برنامه")
        card.layout.addWidget(info_title)

        info_grid = QGridLayout()

        info_grid.setHorizontalSpacing(10)
        info_grid.setVerticalSpacing(5)

        self.app_name = RoundedLineEdit(
            placeholder="نام برنامه"
        )
        self.app_name.setMinimumHeight(36)

        self.app_version = RoundedLineEdit(
            placeholder="نسخه"
        )
        self.app_version.setMinimumHeight(36)

        info_grid.addWidget(
            self._label("نام برنامه", size=11),
            0,
            0,
        )

        info_grid.addWidget(
            self.app_name,
            1,
            0,
        )

        info_grid.addWidget(
            self._label("نسخه", size=11),
            0,
            1,
        )

        info_grid.addWidget(
            self.app_version,
            1,
            1,
        )

        card.layout.addLayout(info_grid)

        card.layout.addSpacing(8)

        # ---------------------------------------------------------
        # Work Hours
        # ---------------------------------------------------------

        work_title = self._section_title("ساعت کاری")
        card.layout.addWidget(work_title)

        work_grid = QGridLayout()

        work_grid.setHorizontalSpacing(10)
        work_grid.setVerticalSpacing(5)

        self.work_start = self._time_edit()
        self.work_end = self._time_edit()

        self.work_start.setTime(QTime(7, 0))
        self.work_end.setTime(QTime(16, 0))

        work_grid.addWidget(
            self._label("شروع کار", size=11),
            0,
            0,
        )

        work_grid.addWidget(
            self.work_start,
            1,
            0,
        )

        work_grid.addWidget(
            self._label("پایان کار", size=11),
            0,
            1,
        )

        work_grid.addWidget(
            self.work_end,
            1,
            1,
        )

        card.layout.addLayout(work_grid)

        card.layout.addSpacing(8)

        # ---------------------------------------------------------
        # Attendance Rules
        # ---------------------------------------------------------

        attendance_title = self._section_title(
            "قوانین حضور و غیاب"
        )

        card.layout.addWidget(attendance_title)

        card.layout.addWidget(
            self._label(
                "تأخیر مجاز",
                size=11,
            )
        )

        self.grace_minutes = QSpinBox()

        self.grace_minutes.setRange(0, 120)
        self.grace_minutes.setFixedHeight(36)
        self.grace_minutes.setSuffix(" دقیقه")
        self.grace_minutes.setLayoutDirection(
            Qt.RightToLeft
        )

        self.grace_minutes.setStyleSheet(
            self._spinbox_style()
        )

        card.layout.addWidget(
            self.grace_minutes
        )

        card.layout.addSpacing(8)

        # ---------------------------------------------------------
        # Backup Settings
        # ---------------------------------------------------------

        backup_title = self._section_title(
            "پشتیبان‌گیری"
        )

        card.layout.addWidget(
            backup_title
        )

        path_row = QHBoxLayout()
        path_row.setSpacing(7)

        self.backup_path = RoundedLineEdit(
            placeholder="مسیر پشتیبان"
        )

        self.backup_path.setMinimumHeight(36)

        browse = SecondaryButton(
            "انتخاب مسیر"
        )

        browse.setFixedHeight(36)

        browse.clicked.connect(
            self.choose_backup_path
        )

        path_row.addWidget(
            self.backup_path,
            1,
        )

        path_row.addWidget(
            browse
        )

        card.layout.addLayout(
            path_row
        )

        card.layout.addSpacing(5)

        card.layout.addWidget(
            self._label(
                "حداکثر تعداد نسخه‌های پشتیبان",
                size=11,
            )
        )

        self.max_backups = QSpinBox()

        self.max_backups.setRange(1, 100)
        self.max_backups.setFixedHeight(36)
        self.max_backups.setSuffix(" نسخه")
        self.max_backups.setLayoutDirection(
            Qt.RightToLeft
        )

        self.max_backups.setStyleSheet(
            self._spinbox_style()
        )

        card.layout.addWidget(
            self.max_backups
        )

        card.layout.addSpacing(8)

        # ---------------------------------------------------------
        # Save Button
        # ---------------------------------------------------------

        save = PrimaryButton(
            "ذخیره تنظیمات"
        )

        save.setFixedHeight(38)

        save.clicked.connect(
            self.save_settings
        )
        self.save_button = save
        self.current_submit = self.save_button

        card.layout.addWidget(
            save,
            alignment=Qt.AlignLeft,
        )

        # ---------------------------------------------------------
        # Information
        # ---------------------------------------------------------

        info = QLabel(
            "تنظیمات در پایگاه داده برنامه ذخیره می‌شوند. "
            "ساعت کاری پیش‌فرض حضور از ۰۷:۰۰ تا ۱۶:۰۰ است."
        )

        info.setWordWrap(True)

        info.setStyleSheet(
            """
            QLabel {
                color: #64748B;
                background: transparent;
                border: none;
                font-size: 10px;
            }
            """
        )

        card.layout.addSpacing(4)

        card.layout.addWidget(
            info
        )

        scroll.setWidget(card)
        layout.addWidget(scroll)

    def load_settings(self):
        values = self.controller.get_settings()


        self.app_name.setText(
            values.get(
                "app_name",
                "حضور",
            )
        )

        self.app_version.setText(
            values.get(
                "app_version",
                "1.0.0",
            )
        )

        self.backup_path.setText(
            values.get(
                "backup_path",
                "backup/archives",
            )
        )

        try:
            self.max_backups.setValue(
                int(
                    values.get(
                        "max_backups",
                        10,
                    )
                )
            )

        except (TypeError, ValueError):
            self.max_backups.setValue(10)

        try:
            start = values.get(
                "work_start",
                "07:00",
            ).split(":")

            self.work_start.setTime(
                QTime(
                    int(start[0]),
                    int(start[1]),
                )
            )

        except (
            ValueError,
            IndexError,
            AttributeError,
        ):
            self.work_start.setTime(
                QTime(7, 0)
            )

        try:
            end = values.get(
                "work_end",
                "16:00",
            ).split(":")

            self.work_end.setTime(
                QTime(
                    int(end[0]),
                    int(end[1]),
                )
            )

        except (
            ValueError,
            IndexError,
            AttributeError,
        ):
            self.work_end.setTime(
                QTime(16, 0)
            )

        try:
            self.grace_minutes.setValue(
                int(
                    values.get(
                        "grace_minutes",
                        15,
                    )
                )
            )

        except (TypeError, ValueError):
            self.grace_minutes.setValue(15)

    def choose_backup_path(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "انتخاب محل ذخیره پشتیبان",
        )

        if directory:
            self.backup_path.setText(
                directory
            )

    def save_settings(self):
        path = self.backup_path.text().strip()

        if not path:
            QMessageBox.warning(
                self,
                "تنظیمات",
                "مسیر پشتیبان را وارد کنید.",
            )
            return

        if (
            self.work_end.time()
            <= self.work_start.time()
        ):
            QMessageBox.warning(
                self,
                "تنظیمات",
                "ساعت پایان کار باید بعد از ساعت شروع کار باشد.",
            )
            return

        try:
            self.controller.save(
                app_name=(
                    self.app_name.text().strip()
                    or "حضور"
                ),
                app_version=(
                    self.app_version.text().strip()
                    or "1.0.0"
                ),
                backup_path=path,
                max_backups=(
                    self.max_backups.value()
                ),
                work_start=(
                    self.work_start.time()
                    .toString("HH:mm")
                ),
                work_end=(
                    self.work_end.time()
                    .toString("HH:mm")
                ),
                grace_minutes=(
                    self.grace_minutes.value()
                ),
            )

            QMessageBox.information(
                self,
                "تنظیمات",
                "تنظیمات با موفقیت ذخیره شد.",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "خطا",
                f"ذخیره تنظیمات انجام نشد:\n{error}",
            )