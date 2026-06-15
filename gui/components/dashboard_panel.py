"""
==================================================
Project : حضور
File    : dashboard_panel.py
Author  : Reyhane Sarabi
Purpose : Dashboard Main Analytics Panel
==================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt, QSize

from theme.colors import Colors
from theme.fonts import Fonts
from PySide6.QtGui import QIcon
from gui.components.hover_card import HoverCard


class DashboardPanel(HoverCard):

    def __init__(
        self,
        repository=None,
        parent=None
    ):

        super().__init__(parent)

        self.repository = repository

        self.setup_ui()

    # ==================================
    # UI
    # ==================================

    def setup_ui(self):

        self.setFixedHeight(
            220
        )

        self.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 24px;
            }
            """
        )

        main_layout = QHBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        main_layout.setSpacing(
            25
        )

        # ==================================
        # Left : Recent Attendance
        # ==================================

        self.recent_layout = QVBoxLayout()

        self.recent_layout.setSpacing(
            12
        )

        recent_title = QLabel(
            "آخرین حضورهای ثبت شده"
        )

        recent_title.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        recent_title.setFont(
            Fonts.heading()
        )

        recent_title.setStyleSheet(
            f"""
            color: {Colors.TEXT};
            font-weight: bold;
            background: transparent;
            """
        )

        self.recent_layout.addWidget(
            recent_title
        )

        self.recent_rows_layout = QVBoxLayout()

        self.recent_rows_layout.setSpacing(
            8
        )

        self.recent_layout.addLayout(
            self.recent_rows_layout
        )

        self.recent_layout.addStretch()

        # ==================================
        # Divider
        # ==================================

        divider = QFrame()

        divider.setFixedWidth(
            1
        )

        divider.setStyleSheet(
            """
            background: #E8EDF5;
            """
        )

        # ==================================
        # Right : Chart
        # ==================================

        chart_layout = QVBoxLayout()

        chart_layout.setSpacing(
            10
        )

        chart_title = QLabel(
            "گزارش حضور هفتگی"
        )

        chart_title.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        chart_title.setFont(
            Fonts.heading()
        )

        chart_title.setStyleSheet(
            f"""
            color: {Colors.TEXT};
            font-weight: bold;
            background: transparent;
            """
        )

        chart_layout.addWidget(
            chart_title
        )

        self.chart_layout = QVBoxLayout()

        self.chart_layout.setSpacing(
            5
        )

        chart_layout.addLayout(
            self.chart_layout
        )

        chart_layout.addStretch()

        # ==================================
        # Main
        # ==================================

        main_layout.addLayout(
            self.recent_layout,
            1
        )

        main_layout.addWidget(
            divider
        )

        main_layout.addLayout(
            chart_layout,
            1
        )

        # اولین بار دریافت اطلاعات

        self.refresh_data()

    # ==================================
    # Clear Layout
    # ==================================

    def clear_layout(
        self,
        layout
    ):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            child_layout = item.layout()

            if widget:

                widget.deleteLater()

            elif child_layout:

                self.clear_layout(
                    child_layout
                )

    # ==================================
    # Refresh Data
    # ==================================

    def refresh_data(self):

        if self.repository is None:
            return

        # ==================================
        # Recent Attendance
        # ==================================

        recent = (
            self.repository
            .get_recent_attendance(
                3
            )
        )

        self.clear_layout(
            self.recent_rows_layout
        )

        for row_data in recent:

            first_name = row_data["first_name"]
            last_name = row_data["last_name"]
            check_in = row_data["check_in"]

            name_label = QLabel(
                f"{first_name} {last_name}"
            )

            name_label.setFont(
                Fonts.text()
            )

            name_label.setStyleSheet(
                f"""
                color: {Colors.TEXT};
                background: transparent;
                """
            )

            time_label = QLabel(
                str(check_in)
            )

            time_label.setFont(
                Fonts.text()
            )

            time_label.setStyleSheet(
                f"""
                color: {Colors.MUTED};
                background: transparent;
                """
            )

            row = QHBoxLayout()

            row.setDirection(
                QHBoxLayout.RightToLeft
            )

            user_icon = QLabel()
            user_icon.setPixmap(
                QIcon("assets/icons/user.svg").pixmap(QSize(18, 18))
            )
            user_icon.setFixedSize(18, 18)

            row.addWidget(
                user_icon
            )

            row.addWidget(
                name_label
            )

            row.addStretch()

            row.addWidget(
                time_label
            )

            self.recent_rows_layout.addLayout(
                row
            )

        # ==================================
        # Weekly Chart
        # ==================================

        weekly_data = (
            self.repository
            .get_weekly_attendance()
        )

        self.clear_layout(
            self.chart_layout
        )

        # شنبه تا چهارشنبه
        weekdays = [
            "شنبه",
            "یکشنبه",
            "دوشنبه",
            "سه‌شنبه",
            "چهارشنبه"
        ]

        # weekday پایتون:
        # Monday = 0
        # Tuesday = 1
        # Wednesday = 2
        # Thursday = 3
        # Friday = 4
        # Saturday = 5
        # Sunday = 6

        # ترتیب موردنظر:
        # Saturday, Sunday, Monday, Tuesday, Wednesday
        wanted_days = [5, 6, 0, 1, 2]

        data_by_weekday = {
            item["weekday"]: item
            for item in weekly_data
        }

        for weekday_index in wanted_days:

            item = data_by_weekday.get(
                weekday_index
            )

            if item is None:
                continue

            count = item["count"]

            day_name = weekdays[
                wanted_days.index(
                    weekday_index
                )
            ]

            row = QHBoxLayout()

            label = QLabel(
                day_name
            )

            label.setFont(
                Fonts.text()
            )

            label.setStyleSheet(
                f"""
                color: {Colors.MUTED};
                background: transparent;
                """
            )

            # فقط خود نمودار، بدون نمایش عدد
            bar = QLabel(
                "█" * min(count, 20)
            )

            bar.setFont(
                Fonts.text()
            )

            bar.setStyleSheet(
                f"""
                color: {Colors.PRIMARY};
                background: transparent;
                """
            )

            row.addWidget(
                label
            )

            row.addStretch()

            row.addWidget(
                bar
            )

            self.chart_layout.addLayout(
                row
            )