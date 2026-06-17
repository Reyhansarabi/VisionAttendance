from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QBrush
)

import jdatetime

from theme.fonts import Fonts
from theme.colors import Colors

from gui.components.stat_card import StatCard
from gui.components.dashboard_panel import DashboardPanel

from controllers.dashboard_controller import DashboardController


class DashboardPage(QWidget):

    # ==================================================
    # Init
    # ==================================================

    def __init__(
        self,
        username="Admin",
        role="admin",
        user_id=None,
        parent=None
    ):

        super().__init__(parent)

        self.username = username
        self.role = role
        self.user_id = user_id

        self.setObjectName(
            "DashboardPage"
        )

        # ==================================================
        # Repository
        # ==================================================

        self.repository = DashboardController()

        # ==================================================
        # UI
        # ==================================================

        self.setup_ui()

        # ==================================================
        # Auto Refresh Timer
        # ==================================================

        self.refresh_timer = QTimer(
            self
        )

        self.refresh_timer.setInterval(
            3000
        )

        self.refresh_timer.timeout.connect(
            self.refresh_data
        )

        self.refresh_timer.start()

        # ==================================================
        # First Refresh
        # ==================================================

        QTimer.singleShot(
            100,
            self.refresh_data
        )

    # ==================================================
    # Role
    # ==================================================

    def is_admin(self):

        return self.role == "admin"

    # ==================================================
    # Background
    # ==================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor(
                    43,
                    110,
                    219,
                    25
                )
            )
        )

        for x in range(
            70,
            self.width(),
            120
        ):

            for y in range(
                90,
                self.height(),
                120
            ):

                painter.drawEllipse(
                    x,
                    y,
                    4,
                    4
                )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setStyleSheet(
            """
            QWidget#DashboardPage
            {
                background: #F4F7FB;
            }
            """
        )

        # ==================================================
        # Main Layout
        # ==================================================

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        main_layout.setSpacing(
            15
        )

        # ==================================================
        # Header
        # ==================================================

        header_layout = QHBoxLayout()

        # --------------------------------------------------
        # Date
        # --------------------------------------------------

        self.date_label = QLabel()

        self.date_label.setFont(
            Fonts.text()
        )

        self.date_label.setStyleSheet(
            f"""
            QLabel
            {{
                color: {Colors.MUTED};
                background: transparent;
                border: none;
            }}
            """
        )

        # --------------------------------------------------
        # Welcome
        # --------------------------------------------------

        self.welcome = QLabel(
            f"سلام {self.username}، خوش آمدی 👋"
        )

        self.welcome.setFont(
            Fonts.title()
        )

        self.welcome.setAlignment(
            Qt.AlignRight
        )

        self.welcome.setStyleSheet(
            f"""
            QLabel
            {{
                color: {Colors.TEXT};
                font-weight: bold;
                background: transparent;
                border: none;
            }}
            """
        )

        header_layout.addWidget(
            self.date_label
        )

        header_layout.addStretch()

        header_layout.addWidget(
            self.welcome
        )

        main_layout.addLayout(
            header_layout
        )

        main_layout.addSpacing(
            50
        )

        # ==================================================
        # Dashboard By Role
        # ==================================================

        if self.is_admin():

            self.setup_admin_dashboard(
                main_layout
            )

        else:

            self.setup_user_dashboard(
                main_layout
            )

        main_layout.addStretch()

    # ==================================================
    # Admin Dashboard
    # ==================================================

    def setup_admin_dashboard(
        self,
        main_layout
    ):

        # ==================================================
        # Statistics Cards
        # ==================================================

        cards_container = QHBoxLayout()

        cards_container.addStretch()

        stats_layout = QHBoxLayout()

        stats_layout.setSpacing(
            20
        )

        # ==================================================
        # Users Card
        # ==================================================

        self.users_card = StatCard(
            "کاربران ثبت شده",
            "0",
            value_color="#4A90E2"
        )

        # ==================================================
        # Present Card
        # ==================================================

        self.present_card = StatCard(
            "حضور امروز",
            "0",
            value_color="#16A34A"
        )

        # ==================================================
        # Absent Card
        # ==================================================

        self.absent_card = StatCard(
            "غیبت امروز",
            "0",
            value_color="#DC2626"
        )

        # ==================================================
        # Add Cards
        # ==================================================

        stats_layout.addWidget(
            self.users_card,
            1
        )

        stats_layout.addWidget(
            self.present_card,
            1
        )

        stats_layout.addWidget(
            self.absent_card,
            1
        )

        cards_container.addLayout(
            stats_layout
        )

        cards_container.addStretch()

        main_layout.addLayout(
            cards_container
        )

        main_layout.addSpacing(
            20
        )

        # ==================================================
        # Dashboard Panel
        # ==================================================

        self.dashboard_panel = DashboardPanel(
            self.repository
        )

        main_layout.addWidget(
            self.dashboard_panel
        )

    # ==================================================
    # Normal User Dashboard
    # ==================================================

    def setup_user_dashboard(
        self,
        main_layout
    ):

        # ==================================================
        # User Title
        # ==================================================

        user_title = QLabel(
            "داشبورد شخصی"
        )

        user_title.setAlignment(
            Qt.AlignCenter
        )

        user_title.setFont(
            Fonts.title()
        )

        user_title.setStyleSheet(
            f"""
            QLabel
            {{
                color: {Colors.TEXT};
                font-weight: bold;
                background: transparent;
                border: none;
            }}
            """
        )

        main_layout.addWidget(
            user_title
        )

        main_layout.addSpacing(
            20
        )

        # ==================================================
        # User Attendance Card
        # ==================================================

        self.user_attendance_card = StatCard(
            "وضعیت حضور امروز",
            "در حال بررسی...",
            value_color="#4A90E2"
        )

        user_card_layout = QHBoxLayout()

        user_card_layout.addStretch()

        user_card_layout.addWidget(
            self.user_attendance_card
        )

        user_card_layout.addStretch()

        main_layout.addLayout(
            user_card_layout
        )

        main_layout.addSpacing(
            20
        )

        # ==================================================
        # Description
        # ==================================================

        self.user_description = QLabel(
            "از منوی برنامه می‌توانید حضور و غیاب و گزارش شخصی خود را مشاهده کنید."
        )

        self.user_description.setAlignment(
            Qt.AlignCenter
        )

        self.user_description.setWordWrap(
            True
        )

        self.user_description.setFont(
            Fonts.text()
        )

        self.user_description.setStyleSheet(
            f"""
            QLabel
            {{
                color: {Colors.MUTED};
                background: transparent;
                border: none;
                padding: 15px;
            }}
            """
        )

        main_layout.addWidget(
            self.user_description
        )

        # ==================================================
        # No Admin Panel For Normal User
        # ==================================================

        self.dashboard_panel = None

    # ==================================================
    # Refresh Data
    # ==================================================

    def refresh_data(self):

        try:

            # ==================================================
            # Jalali Date
            # ==================================================

            now = jdatetime.datetime.now()

            self.date_label.setText(
                now.strftime(
                    "%Y-%m-%d"
                )
            )

            # ==================================================
            # Admin
            # ==================================================

            if self.is_admin():

                # ==============================================
                # Users
                # ==============================================

                users_count = (
                    self.repository
                    .get_users_count()
                )

                # ==============================================
                # Present
                # ==============================================

                present_count = (
                    self.repository
                    .get_today_present_count()
                )

                # ==============================================
                # Absent
                # ==============================================

                absent_count = (
                    self.repository
                    .get_today_absent_count()
                )

                # ==============================================
                # Update Cards
                # ==============================================

                self.users_card.set_value(
                    str(users_count)
                )

                self.present_card.set_value(
                    str(present_count)
                )

                self.absent_card.set_value(
                    str(absent_count)
                )

                # ==============================================
                # Dashboard Panel
                # ==============================================

                if self.dashboard_panel is not None:

                    self.dashboard_panel.refresh_data()

            # ==================================================
            # Normal User
            # ==================================================

            else:

                self.refresh_user_data()

        except Exception as error:

            print(
                "Dashboard refresh error:",
                error
            )

    # ==================================================
    # Refresh User Data
    # ==================================================

    def refresh_user_data(self):

        # --------------------------------------------------
        # اگر شناسه کاربر مشخص نیست
        # --------------------------------------------------

        if self.user_id is None:

            self.user_attendance_card.set_value(
                "نامشخص"
            )

            return

        # --------------------------------------------------
        # دریافت رکورد امروز کاربر
        # --------------------------------------------------

        record = (
            self.repository
            .get_today_record(
                self.user_id
            )
        )

        # --------------------------------------------------
        # هنوز حضور ثبت نشده
        # --------------------------------------------------

        if record is None:

            self.user_attendance_card.set_value(
                "ثبت نشده"
            )

            return

        # --------------------------------------------------
        # وضعیت حضور
        # --------------------------------------------------

        status = (
            record["status"]
            or "نامشخص"
        )

        check_in = (
            record["check_in"]
            or "-"
        )

        check_out = (
            record["check_out"]
            or "-"
        )

        self.user_attendance_card.set_value(
            f"{status} | ورود: {check_in} | خروج: {check_out}"
        )

    # ==================================================
    # Page Refresh
    # ==================================================

    def refresh_page(self):

        self.refresh_data()

    # ==================================================
    # Show Event
    # ==================================================

    def showEvent(
        self,
        event
    ):

        super().showEvent(
            event
        )

        self.refresh_data()

        if not self.refresh_timer.isActive():

            self.refresh_timer.start()

    # ==================================================
    # Hide Event
    # ==================================================

    def hideEvent(
        self,
        event
    ):

        super().hideEvent(
            event
        )

        if self.refresh_timer.isActive():

            self.refresh_timer.stop()