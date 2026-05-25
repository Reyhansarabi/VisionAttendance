"""
==================================================
Project : حضور
File    : app.py
Author  : Reyhane Sarabi
Purpose : Main Application Window
==================================================
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from PySide6.QtCore import QTimer, Qt

from config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)

from theme.style import AppStyle

from gui.components.sidebar import Sidebar
from gui.components.header_card import HeaderCard
from gui.components.window_toolbar import WindowToolbar

from gui.pages.dashboard import DashboardPage
from gui.pages.register_page import RegisterPage
from gui.pages.report_page import ReportPage
from gui.pages.attendance_page import AttendancePage
from gui.pages.settings_page import SettingsPage
from gui.pages.backup_page import BackupPage
from gui.pages.profile_page import ProfilePage
from controllers.auth_controller import AuthController
from gui.components.field_keyboard_navigation import FieldKeyboardNavigation

class MainWindow(QMainWindow):

    def __init__(
        self,
        username="Admin",
        role="admin",
        user_id=None,
        login_window=None
    ):

        super().__init__()

        # ===============================
        # User
        # ===============================

        self.username = username
        self.user_id = user_id

        # ==================================================
        # Role
        # ==================================================

        role = str(
            role or "user"
        ).strip().lower()

        if role not in (
            "admin",
            "user"
        ):

            role = "user"

        self.role = role

        # ===============================
        # Login Window
        # ===============================

        self.login_window = login_window

        # ===============================
        # Pages
        # ===============================

        self.dashboard = None
        self.register_page = None
        self.attendance_page = None
        self.report_page = None
        self.profile_page = None
        self.settings_page = None
        self.backup_page = None

        # ===============================
        # Window
        # ===============================

        self.setup_window()

    # ==================================================
    # Permission
    # ==================================================

    def is_admin(self):

        return self.role == "admin"

    # ==================================================
    # Window
    # ==================================================

    def setup_window(self):

        self.setWindowTitle(
            APP_NAME
        )

        # حذف قاب پیش‌فرض ویندوز؛ کنترل‌های پنجره در Toolbar اختصاصی پروژه هستند.
        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint,
            True
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.setMinimumSize(
            1200,
            750
        )

        self.setStyleSheet(
            AppStyle.get()
        )

        # ==================================================
        # Container
        # ==================================================

        container = QWidget()

        root_layout = QVBoxLayout(
            container
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root_layout.setSpacing(
            0
        )

        # ==================================================
        # Custom Window Toolbar
        # ==================================================

        self.window_toolbar = WindowToolbar(
            self,
            container
        )

        root_layout.addWidget(
            self.window_toolbar
        )

        # ==================================================
        # Main Body
        # ==================================================

        body = QWidget()

        main_layout = QHBoxLayout(
            body
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # ==================================================
        # Sidebar
        # ==================================================

        self.sidebar = Sidebar(
            self.username,
            role=self.role,
            user_id=self.user_id
        )
        self.refresh_sidebar_profile()
        main_layout.addWidget(
            self.sidebar
        )

        # ==================================================
        # Content
        # ==================================================

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            20,
            10,
            20,
            20
        )

        content_layout.setSpacing(
            10
        )

        # ==================================================
        # Header
        # ==================================================

        self.header = HeaderCard()
        content_layout.addWidget(
            self.header
        )

        # ==================================================
        # Pages Container
        # ==================================================

        self.pages = QStackedWidget()

        content_layout.addWidget(
            self.pages
        )

        main_layout.addWidget(
            content
        )

        root_layout.addWidget(
            body
        )

        # ==================================================
        # Navigation Signals
        # ==================================================

        self.sidebar.dashboard_clicked.connect(
            self.go_dashboard
        )

        self.sidebar.register_clicked.connect(
            self.go_register
        )

        self.sidebar.attendance_clicked.connect(
            self.go_attendance
        )

        self.sidebar.report_clicked.connect(
            self.go_report
        )

        self.sidebar.profile_clicked.connect(
            self.go_profile
        )

        self.sidebar.settings_clicked.connect(
            self.go_settings
        )

        self.sidebar.backup_clicked.connect(
            self.go_backup
        )

        self.sidebar.logout_clicked.connect(
            self.logout
        )

        # ==================================================
        # Default Page
        # ==================================================

        if self.is_admin():

            self.load_dashboard()

            self.pages.setCurrentWidget(
                self.dashboard
            )

            self.sidebar.set_active(
                self.sidebar.dashboard_btn
            )

        else:

            # ==================================================
            # کاربر عادی
            #
            # داشبورد اصلاً ساخته نمی‌شود.
            # اولین صفحه مجاز:
            # حضور و غیاب
            # ==================================================

            self.load_attendance()

            self.pages.setCurrentWidget(
                self.attendance_page
            )

            self.sidebar.set_active(
                self.sidebar.attendance_btn
            )

        # ==================================================
        # Central Widget
        # ==================================================

        self.setCentralWidget(
            container
        )

    # ==================================================
    # Lazy Load Dashboard
    # ==================================================

    def load_dashboard(self):

        # حتی اگر somehow متد صدا زده شود،
        # کاربر عادی نباید بتواند صفحه را بسازد.

        if not self.is_admin():

            return False

        if self.dashboard is None:

            self.dashboard = DashboardPage(
                username=self.username,
                role=self.role,
                user_id=self.user_id
            )

            self.pages.addWidget(
                self.dashboard
            )

        return True

    # ==================================================
    # Lazy Load Register
    # ==================================================

    def load_register(self):

        # ثبت کاربر فقط مخصوص Admin

        if not self.is_admin():

            return False

        if self.register_page is None:

            self.register_page = RegisterPage()

            self.pages.addWidget(
                self.register_page
            )

        return True

    # ==================================================
    # Lazy Load Attendance
    # ==================================================

    def load_attendance(self):

        if self.attendance_page is None:

            self.attendance_page = AttendancePage(
                role=self.role,
                user_id=self.user_id
            )

            self.pages.addWidget(
                self.attendance_page
            )

        return True

    # ==================================================
    # Lazy Load Report
    # ==================================================

    def load_report(self):

        if self.report_page is None:

            self.report_page = ReportPage(
                role=self.role,
                user_id=self.user_id
            )
            self.report_page._field_navigation = FieldKeyboardNavigation(
                self.report_page,
                getattr(self.report_page, "current_submit", None)
            )

            self.pages.addWidget(
                self.report_page
            )

        return True

    # ==================================================
    # Lazy Load Settings
    # ==================================================

    def load_settings(self):

        if self.settings_page is None:

            self.settings_page = SettingsPage()
            self.settings_page._field_navigation = FieldKeyboardNavigation(
                self.settings_page,
                getattr(self.settings_page, "current_submit", None)
            )

            self.pages.addWidget(
                self.settings_page
            )

        return True

    # ==================================================
    # Lazy Load Backup
    # ==================================================

    def load_backup(self):

        if self.backup_page is None:

            self.backup_page = BackupPage()

            self.pages.addWidget(
                self.backup_page
            )

        return True

    # ==================================================
    # Reset Attendance
    # ==================================================

    def reset_attendance_page(self):

        if self.attendance_page:

            self.attendance_page.clear_page()

    # ==================================================
    # Reset Report Smart Panel
    # ==================================================

    def _reset_report_smart_panel(self):
        """وقتی از گزارش به هر صفحه دیگری می‌رویم، تحلیل کاملاً ریست شود."""
        if self.report_page is not None:
            if hasattr(self.report_page, "reset_smart_analysis"):
                self.report_page.reset_smart_analysis()
            elif hasattr(self.report_page, "show_report_table"):
                self.report_page.show_report_table()

    # ==================================================
    # Navigation - Dashboard
    # ==================================================

    def go_dashboard(self):

        self._reset_report_smart_panel()

        # ==================================================
        # SECURITY CHECK
        # ==================================================

        if not self.is_admin():

            # کاربر عادی حق ورود ندارد.
            self.go_attendance()

            return

        if not self.load_dashboard():

            return

        self.pages.setCurrentWidget(
            self.dashboard
        )

        self.sidebar.set_active(
            self.sidebar.dashboard_btn
        )

        # رفرش داشبورد

        if hasattr(
            self.dashboard,
            "refresh_page"
        ):

            self.dashboard.refresh_page()

    # ==================================================
    # Navigation - Register
    # ==================================================

    def go_register(self):

        self._reset_report_smart_panel()

        # ==================================================
        # SECURITY CHECK
        # ==================================================

        if not self.is_admin():

            self.go_attendance()

            return

        if not self.load_register():

            return

        # هر بار ورود به ثبت کاربر، فرم از وضعیت قبلی پاک شود.
        if hasattr(self.register_page, "clear_form"):
            self.register_page.clear_form()

        self.pages.setCurrentWidget(
            self.register_page
        )

        self.sidebar.set_active(
            self.sidebar.register_btn
        )

    # ==================================================
    # Navigation - Attendance
    # ==================================================

    def go_attendance(self):

        self._reset_report_smart_panel()

        if self.attendance_page is None:
            if not self.load_attendance():
                return

        if self.attendance_page is None:
            return

        # هر بار ورود به صفحه حضور و غیاب، وضعیت قبلی صفحه پاک شود
        # تا تصویر/نتیجه تشخیص دفعه قبل باقی نماند.
        if hasattr(self.attendance_page, "clear_page"):
            self.attendance_page.clear_page()

        self.pages.setCurrentWidget(
            self.attendance_page
        )

        self.sidebar.set_active(
            self.sidebar.attendance_btn
        )

    # ==================================================
    # Navigation - Report
    # ==================================================

    def go_report(self):

        if not (self.is_admin() or self.role == "user"):
            self.go_attendance()
            return

        if not self.load_report():

            return

        # هر بار ورود به گزارش، اطلاعات تازه از دیتابیس خوانده شود.
        if hasattr(self.report_page, "refresh_table"):
            self.report_page.refresh_table()

        self.pages.setCurrentWidget(
            self.report_page
        )

        self.sidebar.set_active(
            self.sidebar.report_btn
        )

    # ==================================================
    # Navigation - Settings
    # ==================================================

    def go_settings(self):

        self._reset_report_smart_panel()

        if not self.is_admin():
            self.go_attendance()
            return

        if not self.load_settings():
            return

        self.pages.setCurrentWidget(
            self.settings_page
        )

        self.sidebar.set_active(
            self.sidebar.settings_btn
        )

        if hasattr(self.settings_page, "load_settings"):
            self.settings_page.load_settings()

    # ==================================================
    # Navigation - Backup
    # ==================================================

    def go_backup(self):

        self._reset_report_smart_panel()

        if not self.is_admin():
            self.go_attendance()
            return

        if not self.load_backup():
            return

        self.pages.setCurrentWidget(
            self.backup_page
        )

        self.sidebar.set_active(
            self.sidebar.backup_btn
        )

        if hasattr(self.backup_page, "refresh_backups"):
            self.backup_page.refresh_backups()

    def refresh_sidebar_profile(self):

        try:
            account = AuthController().get_profile(self.user_id, self.username)
            if account is not None:
                self.sidebar.set_profile_image(account["profile_image"] or "")
                self.sidebar.set_user(
                    account["username"] or self.username,
                    role=account["role"] or self.role,
                    user_id=account["user_id"] or self.user_id
                )
                self.sidebar.set_profile_image(account["profile_image"] or "")
        except Exception as error:
            print("Sidebar profile refresh error:", error)

    # ==================================================
    # Lazy Load Profile
    # ==================================================

    def load_profile(self):

        if self.profile_page is None:

            self.profile_page = ProfilePage(
                user_id=self.user_id,
                username=self.username,
                role=self.role
            )
            self.profile_page._field_navigation = FieldKeyboardNavigation(
                self.profile_page,
                self.profile_page.current_submit
            )

            self.pages.addWidget(
                self.profile_page
            )
            self.profile_page.profile_updated.connect(self.on_profile_updated)

        return True


    def on_profile_updated(self, first_name, last_name, profile_image):
        self.username = self.profile_page.username
        self.sidebar.set_user(self.username, role=self.role, user_id=self.user_id)
        self.sidebar.set_profile_image(profile_image)

    # ==================================================
    # Navigation - Profile
    # ==================================================

    def go_profile(self):

        self._reset_report_smart_panel()

        if not self.load_profile():

            return

        self.pages.setCurrentWidget(
            self.profile_page
        )

        self.sidebar.set_active(
            self.sidebar.profile_btn
        )

    # ==================================================
    # Logout
    # ==================================================

    def logout(self):

        # اگر پنجره Login وجود دارد

        if self.login_window is not None:

            self.hide()

            self.login_window.show()

            if hasattr(self.login_window, "success_message"):
                self.login_window.success_message = ""

            if hasattr(self.login_window, "show_login_mode"):
                self.login_window.show_login_mode("")

            self.login_window.activateWindow()

            self.login_window.raise_()

            return

        # اگر LoginWindow موجود نیست

        self.hide()