from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QProxyStyle
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QSize
)

from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QPainter,
    QPainterPath
)

from pathlib import Path

from theme.colors import Colors
from theme.fonts import Fonts


class Sidebar(QFrame):

    # ==================================================
    # Signals
    # ==================================================

    dashboard_clicked = Signal()
    register_clicked = Signal()
    attendance_clicked = Signal()
    report_clicked = Signal()
    profile_clicked = Signal()
    settings_clicked = Signal()
    backup_clicked = Signal()

    # خروج از حساب
    logout_clicked = Signal()

    # ==================================================
    # Init
    # ==================================================

    def __init__(
        self,
        username="reyhanesarabi",
        role="admin",
        user_id=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.username = username
        self.user_id = user_id

        self.role = str(
            role or "user"
        ).strip().lower()

        if self.role not in (
            "admin",
            "user"
        ):

            self.role = "user"

        self.setup_ui()

    # ==================================================
    # Set User
    # ==================================================

    def set_user(
        self,
        username,
        role=None,
        user_id=None
    ):

        self.username = username

        if user_id is not None:

            self.user_id = user_id

        if role is not None:

            self.role = (
                role.strip().lower()
                if isinstance(role, str)
                else "user"
            )

        if hasattr(
            self,
            "user_label"
        ):

            self.user_label.setText(
                username
            )

        if hasattr(
            self,
            "avatar_button"
        ):

            self.set_profile_image(None)

        self.apply_permissions()

    # ==================================================
    # Set Profile Image
    # ==================================================

    def set_profile_image(self, image_path):

        if not hasattr(self, "avatar_button"):
            return

        if image_path and Path(image_path).exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                size = 36
                scaled = pixmap.scaled(
                    size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                output = QPixmap(size, size)
                output.fill(Qt.transparent)
                painter = QPainter(output)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, scaled)
                painter.end()
                self.avatar_button.setText("")
                self.avatar_button.setIcon(QIcon(output))
                self.avatar_button.setIconSize(output.size())
                self.avatar_button.setStyleSheet(
                    "QPushButton { background: #253344; border: 2px solid rgba(255,255,255,0.18); border-radius: 18px; min-width:36px; max-width:36px; min-height:36px; max-height:36px; padding:0; }"
                    "QPushButton:hover { border: 2px solid rgba(255,255,255,0.45); }"
                )
                return

        self.avatar_button.setIcon(QIcon())
        self.avatar_button.setIconSize(QPixmap(1, 1).size())
        self.avatar_button.setText(self.get_initial(self.username))
        self.avatar_button.setStyleSheet(self.avatar_style(self.avatar_color(self.username)))

    # ==================================================
    # Set Role
    # ==================================================

    def set_role(
        self,
        role
    ):

        if isinstance(
            role,
            str
        ):

            self.role = (
                role.strip().lower()
            )

        else:

            self.role = "user"

        self.apply_permissions()

    # ==================================================
    # Permission Helpers
    # ==================================================

    def is_admin(self):

        return self.role == "admin"

    def can_access_dashboard(self):

        return self.is_admin()

    def can_access_register(self):

        return self.is_admin()

    def can_access_attendance(self):

        return True

    def can_access_report(self):

        return True

    def can_access_profile(self):

        return True

    def can_access_settings(self):

        return self.is_admin()

    def can_access_backup(self):

        return self.is_admin()

    # ==================================================
    # Apply Permissions
    # ==================================================

    def apply_permissions(self):

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        if hasattr(
            self,
            "dashboard_btn"
        ):

            self.dashboard_btn.setVisible(
                self.can_access_dashboard()
            )

            self.dashboard_btn.setEnabled(
                self.can_access_dashboard()
            )

        # --------------------------------------------------
        # Register Users
        # --------------------------------------------------

        if hasattr(
            self,
            "register_btn"
        ):

            self.register_btn.setVisible(
                self.can_access_register()
            )

            self.register_btn.setEnabled(
                self.can_access_register()
            )

        # --------------------------------------------------
        # Attendance
        # --------------------------------------------------

        if hasattr(
            self,
            "attendance_btn"
        ):

            self.attendance_btn.setVisible(
                self.can_access_attendance()
            )

            self.attendance_btn.setEnabled(
                self.can_access_attendance()
            )

        # --------------------------------------------------
        # Report
        # --------------------------------------------------

        if hasattr(
            self,
            "report_btn"
        ):

            self.report_btn.setVisible(
                self.can_access_report()
            )

            self.report_btn.setEnabled(
                self.can_access_report()
            )

        # --------------------------------------------------
        # Profile
        # --------------------------------------------------

        if hasattr(
            self,
            "profile_btn"
        ):

            self.profile_btn.setVisible(
                self.can_access_profile()
            )

            self.profile_btn.setEnabled(
                self.can_access_profile()
            )

        # --------------------------------------------------
        # Settings
        # --------------------------------------------------

        if hasattr(
            self,
            "settings_btn"
        ):

            self.settings_btn.setVisible(
                self.can_access_settings()
            )

            self.settings_btn.setEnabled(
                self.can_access_settings()
            )

        # --------------------------------------------------
        # Backup
        # --------------------------------------------------

        if hasattr(
            self,
            "backup_btn"
        ):

            self.backup_btn.setVisible(
                self.can_access_backup()
            )

            self.backup_btn.setEnabled(
                self.can_access_backup()
            )

        # --------------------------------------------------
        # If current active button is unavailable
        # --------------------------------------------------

        if not self.is_admin():

            self.set_active(
                self.attendance_btn
            )

    # ==================================================
    # Initial Letter
    # ==================================================

    def get_initial(
        self,
        username
    ):

        if not username:

            return "?"

        return username.strip()[0].upper()

    # ==================================================
    # Avatar Color
    # ==================================================

    def avatar_color(
        self,
        username
    ):

        colors = [

            "#3B82F6",
            "#14B8A6",
            "#8B5CF6",
            "#06B6D4",
            "#10B981",
            "#6366F1",
            "#0EA5E9",
            "#22C55E"

        ]

        if not username:

            return colors[0]

        index = (
            sum(
                ord(char)
                for char in username
            )
            % len(colors)
        )

        return colors[index]

    # ==================================================
    # Avatar Style
    # ==================================================

    def avatar_style(
        self,
        color
    ):

        return f"""
            QPushButton
            {{
                background: {color};
                color: white;
                border: none;
                border-radius: 18px;

                min-width: 36px;
                max-width: 36px;

                min-height: 36px;
                max-height: 36px;

                font-size: 15px;
                font-weight: bold;
            }}

            QPushButton:hover
            {{
                background: {color};
                border: 2px solid rgba(255,255,255,0.35);
            }}

            QPushButton:pressed
            {{
                background: {color};
            }}
        """

    # ==================================================
    # Active Button
    # ==================================================

    def set_active(
        self,
        button
    ):

        buttons = [

            self.dashboard_btn,
            self.register_btn,
            self.attendance_btn,
            self.report_btn,
            self.profile_btn,
            self.settings_btn,
            self.backup_btn

        ]

        for btn in buttons:

            if not btn.isVisible():

                continue

            if btn == button:

                btn.setStyleSheet(
                    f"""
                    QPushButton
                    {{
                        background: #EEF4FF;
                        color: {Colors.PRIMARY};

                        border: none;
                        border-right: 4px solid {Colors.PRIMARY};

                        border-radius: 14px;

                        text-align: left;
                        padding-left: 18px;

                        font-size: 13px;
                        font-weight: bold;
                    }}

                    QPushButton:hover
                    {{
                        background: #EEF4FF;
                        color: {Colors.PRIMARY};
                    }}
                    """
                )

            else:

                btn.setStyleSheet(
                    f"""
                    QPushButton
                    {{
                        background: transparent;
                        color: #D9E2EC;

                        border: none;
                        border-radius: 14px;

                        text-align: left;
                        padding-left: 18px;

                        font-size: 13px;
                    }}

                    QPushButton:hover
                    {{
                        background: {Colors.PRIMARY};
                        color: white;
                    }}

                    QPushButton:pressed
                    {{
                        background: #2B6EDB;
                    }}
                    """
                )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(
        self
    ):

        self.setFixedWidth(
            270
        )

        self.setStyleSheet(
            """
            QFrame
            {
                background: #17212B;
                border: none;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            25,
            20,
            18
        )

        layout.setSpacing(
            8
        )

        # ==================================================
        # Logo
        # ==================================================

        logo_container = QHBoxLayout()

        logo_container.setContentsMargins(
            0,
            0,
            0,
            0
        )

        logo_container.setSpacing(
            8
        )

        # --------------------------------------------------
        # Logo Image
        # --------------------------------------------------

        logo_image = QLabel()

        logo_image.setFixedSize(
            52,
            52
        )

        logo_image.setAlignment(
            Qt.AlignCenter
        )

        logo_image.setStyleSheet(
            """
            QLabel
            {
                background: transparent;
                border: none;
            }
            """
        )

        logo_pixmap = QPixmap(
            "assets/logo.png"
        )

        if not logo_pixmap.isNull():

            logo_image.setPixmap(
                logo_pixmap.scaled(
                    52,
                    52,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        # --------------------------------------------------
        # App Name
        # --------------------------------------------------

        logo_text = QLabel(
            "حضور"
        )

        logo_text.setFont(
            Fonts.large_title()
        )

        logo_text.setStyleSheet(
            """
            QLabel
            {
                color: white;
                background: transparent;
                border: none;
                font-weight: bold;
            }
            """
        )

        logo_container.addWidget(
            logo_image
        )

        logo_container.addWidget(
            logo_text
        )

        logo_container.addStretch()

        layout.addLayout(
            logo_container
        )

        layout.addSpacing(
            20
        )

        # ==================================================
        # Buttons
        # ==================================================

        self.dashboard_btn = QPushButton("داشبورد")
        self.register_btn = QPushButton("ثبت کاربران")
        self.attendance_btn = QPushButton("ثبت حضور و غیاب")
        self.report_btn = QPushButton("گزارش")
        self.profile_btn = QPushButton("پروفایل من")
        self.settings_btn = QPushButton("تنظیمات")
        self.backup_btn = QPushButton("پشتیبان‌گیری")

        sidebar_icons = {
            self.dashboard_btn: "house.svg",
            self.register_btn: "user-plus.svg",
            self.attendance_btn: "calendar-check.svg",
            self.report_btn: "chart-no-axes-combined.svg",
            self.profile_btn: "user-pen.svg",
            self.settings_btn: "settings.svg",
            self.backup_btn: "database-backup.svg",
        }
        for button, icon_name in sidebar_icons.items():
            button.setIcon(QIcon(f"assets/icons/{icon_name}"))
            button.setIconSize(QSize(21, 21))

        # ==================================================
        # Buttons List
        # ==================================================

        buttons = [

            self.dashboard_btn,
            self.register_btn,
            self.attendance_btn,
            self.report_btn,
            self.profile_btn,
            self.settings_btn,
            self.backup_btn

        ]

        # ==================================================
        # Permissions
        # ==================================================

        if self.role != "admin":

            self.dashboard_btn.hide()

            self.register_btn.hide()

        # ==================================================
        # Button Style
        # ==================================================

        for btn in buttons:

            btn.setCursor(
                Qt.PointingHandCursor
            )

            btn.setFixedHeight(
                46
            )

            btn.setFont(
                Fonts.button()
            )

            btn.setStyleSheet(
                f"""
                QPushButton
                {{
                    background: transparent;
                    color: #D9E2EC;

                    border: none;
                    border-radius: 14px;

                    text-align: left;
                    padding-left: 18px;

                    font-size: 13px;
                }}

                QPushButton:hover
                {{
                    background: {Colors.PRIMARY};
                    color: white;
                }}

                QPushButton:pressed
                {{
                    background: #2B6EDB;
                }}
                """
            )

            layout.addWidget(
                btn
            )

        # ==================================================
        # Space
        # ==================================================

        layout.addStretch()

        # ==================================================
        # User Profile
        # ==================================================

        profile_container = QFrame()

        profile_container.setObjectName(
            "UserProfile"
        )

        profile_container.setCursor(
            Qt.PointingHandCursor
        )

        profile_container.setStyleSheet(
            """
            QFrame#UserProfile
            {
                background: #202B36;

                border: none;
                border-radius: 14px;
            }

            QFrame#UserProfile:hover
            {
                background: #263542;
            }
            """
        )

        profile_layout = QHBoxLayout(
            profile_container
        )

        profile_layout.setContentsMargins(
            8,
            6,
            8,
            6
        )

        profile_layout.setSpacing(
            9
        )

        # ==================================================
        # Avatar
        # ==================================================

        self.avatar_button = QPushButton(
            self.get_initial(
                self.username
            )
        )

        self.avatar_button.setCursor(
            Qt.PointingHandCursor
        )

        self.avatar_button.setStyleSheet(
            self.avatar_style(
                self.avatar_color(
                    self.username
                )
            )
        )

        profile_layout.addWidget(
            self.avatar_button
        )

        # ==================================================
        # Username
        # ==================================================

        self.user_label = QLabel(
            self.username
        )

        self.user_label.setFont(
            Fonts.button()
        )

        self.user_label.setAlignment(
            Qt.AlignLeft |
            Qt.AlignVCenter
        )

        self.user_label.setStyleSheet(
            """
            QLabel
            {
                color: #F1F5F9;

                background: transparent;
                border: none;

                font-size: 12px;
                font-weight: bold;

                padding: 0;
            }
            """
        )

        profile_layout.addWidget(
            self.user_label
        )

        profile_layout.addStretch()

        layout.addWidget(
            profile_container
        )

        # ==================================================
        # Profile Container
        # ==================================================

        self.avatar_button.clicked.connect(
            self.show_profile_menu
        )

        self.user_label.mousePressEvent = (
            lambda event:
            self.show_profile_menu()
        )

        profile_container.mousePressEvent = (
            lambda event:
            self.show_profile_menu()
        )

        # ==================================================
        # Navigation Signals
        # ==================================================

        self.dashboard_btn.clicked.connect(
            self._handle_dashboard_click
        )

        self.register_btn.clicked.connect(
            self._handle_register_click
        )

        self.attendance_btn.clicked.connect(
            self._handle_attendance_click
        )

        self.report_btn.clicked.connect(
            self._handle_report_click
        )

        self.profile_btn.clicked.connect(
            self._handle_profile_click
        )

        self.settings_btn.clicked.connect(
            self._handle_settings_click
        )

        self.backup_btn.clicked.connect(
            self._handle_backup_click
        )

        # ==================================================
        # Initial Permission State
        # ==================================================

        self.apply_permissions()

        # ==================================================
        # Active State
        # ==================================================

        if self.is_admin():

            self.set_active(
                self.dashboard_btn
            )

        else:

            self.set_active(
                self.attendance_btn
            )

    # ==================================================
    # Protected Navigation Handlers
    # ==================================================

    def _handle_dashboard_click(
        self
    ):

        if not self.can_access_dashboard():

            return

        self.set_active(
            self.dashboard_btn
        )

        self.dashboard_clicked.emit()

    # --------------------------------------------------

    def _handle_register_click(
        self
    ):

        if not self.can_access_register():

            return

        self.set_active(
            self.register_btn
        )

        self.register_clicked.emit()

    # --------------------------------------------------

    def _handle_attendance_click(
        self
    ):

        if not self.can_access_attendance():

            return

        self.set_active(
            self.attendance_btn
        )

        self.attendance_clicked.emit()

    # --------------------------------------------------

    def _handle_report_click(
        self
    ):

        if not self.can_access_report():

            return

        self.set_active(
            self.report_btn
        )

        self.report_clicked.emit()

    # --------------------------------------------------

    def _handle_profile_click(
        self
    ):

        if not self.can_access_profile():

            return

        self.set_active(
            self.profile_btn
        )

        self.profile_clicked.emit()

    # --------------------------------------------------

    def _handle_settings_click(
        self
    ):

        if not self.can_access_settings():

            return

        self.set_active(
            self.settings_btn
        )

        self.settings_clicked.emit()

    # --------------------------------------------------

    def _handle_backup_click(
        self
    ):

        if not self.can_access_backup():

            return

        self.set_active(
            self.backup_btn
        )

        self.backup_clicked.emit()

    # ==================================================
    # Profile Menu
    # ==================================================

    def show_profile_menu(
        self
    ):

        menu = QMenu(
            self
        )

        menu.setLayoutDirection(
            Qt.RightToLeft
        )

        menu.setStyleSheet(
            """
            QMenu
            {
                background: white;

                border: none;
                border-radius: 14px;

                padding: 5px;
            }

            QMenu::item
            {
                background: transparent;

                color: #111827;

                padding: 8px 12px;

                border: none;
                border-radius: 9px;

                font-size: 11px;

                min-width: 145px;
            }

            QMenu::item:selected
            {
                background: #F1F5F9;

                color: #111827;
            }
            """
        )

        # ==================================================
        # Logout Icon
        # ==================================================

        logout_icon = QIcon(
            "assets/icons/log-out.svg"
        )

        # ==================================================
        # Menu Icon Style
        # ==================================================

        class MenuIconStyle(
            QProxyStyle
        ):

            def pixelMetric(
                self,
                metric,
                option=None,
                widget=None
            ):

                if (
                    metric ==
                    QProxyStyle.PM_SmallIconSize
                ):

                    return 20

                return super().pixelMetric(
                    metric,
                    option,
                    widget
                )

        menu.setStyle(
            MenuIconStyle()
        )

        # ==================================================
        # Logout
        # ==================================================

        logout_action = menu.addAction(
            logout_icon,
            "خروج از حساب"
        )

        logout_action.triggered.connect(
            self.logout_clicked.emit
        )

        # ==================================================
        # Show Menu
        # ==================================================

        position = (
            self.avatar_button.mapToGlobal(
                self.avatar_button.rect().bottomLeft()
            )
        )

        menu.exec(
            position
        )