# ==================================================
# Project : حضور
# File    : table_toolbar.py
# Purpose : Table Control Toolbar
# ==================================================

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMenu,
    QWidgetAction,
    QLineEdit,
    QWidget,
    QGridLayout
)

from PySide6.QtCore import (
    Qt,
    Signal
)

from PySide6.QtGui import (
    QAction,
    QIcon
)

import jdatetime

from gui.components.rounded_input import RoundedLineEdit
from gui.components.primary_button import PrimaryButton


# ==================================================
# Jalali Calendar Popup
# ==================================================

class JalaliCalendarPopup(QFrame):

    date_selected = Signal(object)

    def __init__(
        self,
        parent=None,
        initial_date=None
    ):

        super().__init__(
            parent,
            Qt.Popup
        )

        self.setObjectName(
            "JalaliCalendarPopup"
        )

        # --------------------------------------------------
        # Date
        # --------------------------------------------------

        if initial_date is None:

            today = jdatetime.date.today()

            self.year = today.year
            self.month = today.month
            self.day = today.day

        else:

            self.year = initial_date[0]
            self.month = initial_date[1]
            self.day = initial_date[2]

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        self.setup_ui()

        self.refresh_calendar()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setFixedWidth(
            300
        )

        self.setStyleSheet(
            """
            QFrame#JalaliCalendarPopup {
                background: #FFFFFF;
                border: 1px solid #D9E2EC;
                border-radius: 14px;
            }

            QLabel {
                background: transparent;
                color: #334155;
            }

            QPushButton {
                background: transparent;
                border: none;
                border-radius: 7px;
                color: #334155;
                padding: 6px;
            }

            QPushButton:hover {
                background: #EEF4FA;
            }

            QPushButton:pressed {
                background: #DCEBFF;
            }

            QPushButton[dayButton="true"] {
                min-width: 32px;
                min-height: 32px;
                padding: 5px;
                color: #334155;
            }

            QPushButton[dayButton="true"]:hover {
                background: #EAF3FF;
                color: #2563EB;
            }

            QPushButton[selected="true"] {
                background: #2563EB;
                color: white;
                font-weight: bold;
            }
            """
        )

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        main_layout.setSpacing(
            8
        )

        # ==================================================
        # Header
        # ==================================================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # Previous month

        self.previous_button = QPushButton(
            "‹"
        )

        self.previous_button.setFixedSize(
            34,
            34
        )

        self.previous_button.clicked.connect(
            self.previous_month
        )

        # Month / Year

        self.month_label = QLabel()

        self.month_label.setAlignment(
            Qt.AlignCenter
        )

        self.month_label.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
                color: #1E293B;
                font-size: 13px;
            }
            """
        )

        # Next month

        self.next_button = QPushButton(
            "›"
        )

        self.next_button.setFixedSize(
            34,
            34
        )

        self.next_button.clicked.connect(
            self.next_month
        )

        header_layout.addWidget(
            self.previous_button
        )

        header_layout.addWidget(
            self.month_label,
            1
        )

        header_layout.addWidget(
            self.next_button
        )

        main_layout.addLayout(
            header_layout
        )

        # ==================================================
        # Week Days
        # ==================================================

        week_layout = QGridLayout()

        week_layout.setHorizontalSpacing(
            2
        )

        week_layout.setVerticalSpacing(
            2
        )

        # شروع هفته در تقویم شمسی: شنبه

        week_days = [
            "ش",
            "ی",
            "د",
            "س",
            "چ",
            "پ",
            "ج"
        ]

        for column, day_name in enumerate(
            week_days
        ):

            label = QLabel(
                day_name
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            label.setStyleSheet(
                """
                QLabel {
                    color: #64748B;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 5px;
                }
                """
            )

            week_layout.addWidget(
                label,
                0,
                column
            )

        main_layout.addLayout(
            week_layout
        )

        # ==================================================
        # Days Grid
        # ==================================================

        self.days_grid = QGridLayout()

        self.days_grid.setHorizontalSpacing(
            2
        )

        self.days_grid.setVerticalSpacing(
            2
        )

        main_layout.addLayout(
            self.days_grid
        )

        # ==================================================
        # Today Button
        # ==================================================

        today_button = QPushButton(
            "امروز"
        )

        today_button.clicked.connect(
            self.select_today
        )

        main_layout.addWidget(
            today_button
        )

    # ==================================================
    # Days In Month
    # ==================================================

    def days_in_month(
        self,
        year,
        month
    ):

        if month <= 6:

            return 31

        if month <= 11:

            return 30

        # اسفند

        if jdatetime.date(
            year,
            1,
            1
        ).isleap():

            return 30

        return 29

    # ==================================================
    # Month Name
    # ==================================================

    def month_name(
        self,
        month
    ):

        names = [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
            "مهر",
            "آبان",
            "آذر",
            "دی",
            "بهمن",
            "اسفند"
        ]

        return names[
            month - 1
        ]

    # ==================================================
    # Refresh Calendar
    # ==================================================

    def refresh_calendar(self):

        # پاک کردن روزهای قبلی

        while self.days_grid.count():

            item = self.days_grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

        # عنوان

        self.month_label.setText(
            f"{self.month_name(self.month)} {self.year}"
        )

        # اولین روز ماه

        first_day = jdatetime.date(
            self.year,
            self.month,
            1
        )

        # weekday جدمیتی:
        # شنبه = 0
        # یکشنبه = 1
        # ...
        # جمعه = 6

        start_column = first_day.weekday()

        total_days = self.days_in_month(
            self.year,
            self.month
        )

        # ==================================================
        # Create Days
        # ==================================================

        for day in range(
            1,
            total_days + 1
        ):

            position = (
                start_column + day - 1
            )

            row = (
                position // 7
            )

            column = (
                position % 7
            )

            button = QPushButton(
                str(day)
            )

            button.setProperty(
                "dayButton",
                True
            )

            button.setFixedSize(
                34,
                32
            )

            # روز انتخاب شده

            if day == self.day:

                button.setProperty(
                    "selected",
                    True
                )

            button.style().unpolish(
                button
            )

            button.style().polish(
                button
            )

            button.clicked.connect(
                lambda checked=False,
                day=day:
                self.select_day(day)
            )

            self.days_grid.addWidget(
                button,
                row,
                column
            )

    # ==================================================
    # Previous Month
    # ==================================================

    def previous_month(self):

        self.month -= 1

        if self.month < 1:

            self.month = 12
            self.year -= 1

        self.day = min(
            self.day,
            self.days_in_month(
                self.year,
                self.month
            )
        )

        self.refresh_calendar()

    # ==================================================
    # Next Month
    # ==================================================

    def next_month(self):

        self.month += 1

        if self.month > 12:

            self.month = 1
            self.year += 1

        self.day = min(
            self.day,
            self.days_in_month(
                self.year,
                self.month
            )
        )

        self.refresh_calendar()

    # ==================================================
    # Select Day
    # ==================================================

    def select_day(
        self,
        day
    ):

        self.day = day

        selected_date = jdatetime.date(
            self.year,
            self.month,
            self.day
        )

        self.date_selected.emit(
            selected_date
        )

        self.close()

    # ==================================================
    # Select Today
    # ==================================================

    def select_today(self):

        today = jdatetime.date.today()

        self.year = today.year
        self.month = today.month
        self.day = today.day

        self.date_selected.emit(
            today
        )

        self.close()


# ==================================================
# Jalali Date Input
# ==================================================

class JalaliDateEdit(QFrame):

    dateChanged = Signal(object)

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.current_date = (
            jdatetime.date.today()
        )

        self.calendar_popup = None

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setFixedHeight(
            38
        )

        # مهم:
        # باعث می‌شود کلیک روی خود فیلد
        # به QMenu منتقل نشود.
        self.setAttribute(
            Qt.WA_NoMousePropagation,
            True
        )

        self.setStyleSheet(
            """
            QFrame {
                background: #F8FAFC;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
            }

            QFrame:hover {
                border: 1px solid #94A3B8;
            }

            QFrame QPushButton {
                background: transparent;
                border: none;
            }

            QFrame QPushButton:hover {
                background: #EAF3FF;
                border-radius: 6px;
            }
            """
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            7,
            2,
            5,
            2
        )

        layout.setSpacing(
            3
        )

        # --------------------------------------------------
        # Calendar Button
        # --------------------------------------------------

        self.calendar_button = QPushButton(
            "📅"
        )

        self.calendar_button.setFixedSize(
            30,
            30
        )

        self.calendar_button.setCursor(
            Qt.PointingHandCursor
        )

        self.calendar_button.setFocusPolicy(
            Qt.NoFocus
        )

        self.calendar_button.clicked.connect(
            self.open_calendar
        )

        layout.addWidget(
            self.calendar_button
        )

        # --------------------------------------------------
        # Date Text
        # --------------------------------------------------

        self.date_label = QLabel()

        self.date_label.setAlignment(
            Qt.AlignCenter
        )

        self.date_label.setAttribute(
            Qt.WA_TransparentForMouseEvents,
            True
        )

        self.date_label.setStyleSheet(
            """
            QLabel {
                color: #1E293B;
                background: transparent;
                border: none;
                font-size: 12px;
            }
            """
        )

        layout.addWidget(
            self.date_label,
            1
        )

        self.update_text()

    # ==================================================
    # Mouse Press
    # ==================================================

    def mousePressEvent(
        self,
        event
    ):

        # جلوگیری از بسته شدن QMenu
        # هنگام کلیک روی خود فیلد تاریخ
        event.accept()

    # ==================================================
    # Mouse Release
    # ==================================================

    def mouseReleaseEvent(
        self,
        event
    ):

        # رویداد را داخل فیلد نگه می‌داریم
        event.accept()

    # ==================================================
    # Update Text
    # ==================================================

    def update_text(self):

        self.date_label.setText(
            self.current_date.strftime(
                "%Y/%m/%d"
            )
        )

    # ==================================================
    # Open Calendar
    # ==================================================

    def open_calendar(self):

        self.calendar_popup = JalaliCalendarPopup(
            self,
            (
                self.current_date.year,
                self.current_date.month,
                self.current_date.day
            )
        )

        self.calendar_popup.date_selected.connect(
            self.set_jalali_date
        )

        # --------------------------------------------------
        # قرار دادن تقویم زیر فیلد
        # --------------------------------------------------

        position = self.mapToGlobal(
            self.rect().bottomLeft()
        )

        self.calendar_popup.move(
            position
        )

        self.calendar_popup.show()

    # ==================================================
    # Set Date
    # ==================================================

    def set_jalali_date(
        self,
        date
    ):

        self.current_date = date

        self.update_text()

        self.dateChanged.emit(
            date
        )

    # ==================================================
    # Get Date
    # ==================================================

    def date(self):

        return self.current_date

    # ==================================================
    # Set Date
    # ==================================================

    def setDate(
        self,
        date
    ):

        if isinstance(
            date,
            jdatetime.date
        ):

            self.current_date = date

            self.update_text()

        elif isinstance(
            date,
            tuple
        ):

            self.current_date = jdatetime.date(
                date[0],
                date[1],
                date[2]
            )

            self.update_text()


# ==================================================
# Table Toolbar
# ==================================================

class TableToolbar(QFrame):

    # ==================================================
    # Signals
    # ==================================================

    search_changed = Signal(str)

    status_changed = Signal(str)

    date_range_changed = Signal(
        object,
        object
    )

    refresh_clicked = Signal()

    print_clicked = Signal()

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setMinimumHeight(
            82
        )

        self.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
            """
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            10
        )

        # ==================================================
        # SEARCH
        # ==================================================

        self.search_input = RoundedLineEdit(
            "جستجو..."
        )

        self.search_input.setLayoutDirection(
            Qt.RightToLeft
        )

        self.search_input.setMinimumWidth(
            250
        )

        self.search_input.setMaximumWidth(
            320
        )

        # --------------------------------------------------
        # Search Icon
        # --------------------------------------------------

        search_icon = QIcon.fromTheme(
            "edit-find"
        )

        if not search_icon.isNull():

            search_action = QAction(
                search_icon,
                "",
                self
            )

            self.search_input.line_edit.addAction(
                search_action,
                QLineEdit.LeadingPosition
            )

        self.search_input.line_edit.textChanged.connect(
            self.search_changed.emit
        )

        layout.addWidget(
            self.search_input
        )

        layout.addStretch()

        # ==================================================
        # FILTER BUTTON
        # ==================================================

        self.filter_button = QPushButton(
            "فیلتر  ▾"
        )

        self.filter_button.setCursor(
            Qt.PointingHandCursor
        )

        self.filter_button.setLayoutDirection(
            Qt.RightToLeft
        )

        self.filter_button.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 9px 14px;
                color: #334155;
                font-weight: 600;
                border-radius: 10px;
            }

            QPushButton:hover {
                background: #F1F5F9;
            }

            QPushButton:pressed {
                background: #E2E8F0;
            }
            """
        )

        layout.addWidget(
            self.filter_button
        )

        # ==================================================
        # PRINT
        # ==================================================

        self.print_button = QPushButton(
            ""
        )

        self.print_button.setCursor(
            Qt.PointingHandCursor
        )

        self.print_button.setToolTip(
            "چاپ گزارش"
        )

        self.print_button.setFixedSize(
            38,
            38
        )

        print_icon = QIcon.fromTheme(
            "document-print"
        )

        if not print_icon.isNull():

            self.print_button.setIcon(
                print_icon
            )

        self.print_button.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 7px;
                border-radius: 10px;
            }

            QPushButton:hover {
                background: #EAF3FF;
            }

            QPushButton:pressed {
                background: #DCEBFF;
            }
            """
        )

        self.print_button.clicked.connect(
            self.print_clicked.emit
        )

        layout.addWidget(
            self.print_button
        )

        # ==================================================
        # REFRESH
        # ==================================================

        self.refresh_button = PrimaryButton(
            ""
        )

        self.refresh_button.setText(
            ""
        )

        refresh_icon = QIcon.fromTheme(
            "view-refresh"
        )

        if not refresh_icon.isNull():

            self.refresh_button.setIcon(
                refresh_icon
            )

        self.refresh_button.setToolTip(
            "بازنشانی جدول"
        )

        self.refresh_button.setFixedSize(
            38,
            38
        )

        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 7px;
                border-radius: 10px;
            }

            QPushButton:hover {
                background: #F1F5F9;
            }

            QPushButton:pressed {
                background: #E2E8F0;
            }
            """
        )

        self.refresh_button.clicked.connect(
            self.refresh_clicked.emit
        )

        layout.addWidget(
            self.refresh_button
        )

        # ==================================================
        # FILTER MENU
        # ==================================================

        self.create_filter_menu()

    # ==================================================
    # FILTER MENU
    # ==================================================

    def create_filter_menu(self):

        self.filter_menu = QMenu(
            self
        )

        self.filter_menu.setLayoutDirection(
            Qt.RightToLeft
        )

        self.filter_menu.setStyleSheet(
            """
            QMenu {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 7px;
                color: #334155;
            }

            QMenu::item {
                padding: 8px 14px;
                min-width: 190px;
                border-radius: 8px;
            }

            QMenu::item:selected {
                background: #F1F5F9;
                color: #0F172A;
            }

            QMenu::separator {
                height: 1px;
                background: #E2E8F0;
                margin: 6px;
            }
            """
        )

        self.filter_button.setMenu(
            self.filter_menu
        )

        self.build_filter_menu()

    # ==================================================
    # BUILD FILTER MENU
    # ==================================================

    def build_filter_menu(self):

        self.filter_menu.clear()

        # ==================================================
        # STATUS
        # ==================================================

        status_title = QAction(
            "وضعیت",
            self
        )

        status_title.setEnabled(
            False
        )

        self.filter_menu.addAction(
            status_title
        )

        statuses = [
            ("همه وضعیت‌ها", "all"),
            ("حاضر", "present"),
            ("تاخیر", "late"),
            ("غایب", "absent")
        ]

        for title, value in statuses:

            action = QAction(
                title,
                self
            )

            action.triggered.connect(
                lambda checked=False,
                value=value:
                self.status_changed.emit(
                    value
                )
            )

            self.filter_menu.addAction(
                action
            )

        self.filter_menu.addSeparator()

        # ==================================================
        # DATE RANGE
        # ==================================================

        date_title = QAction(
            "بازه تاریخ",
            self
        )

        date_title.setEnabled(
            False
        )

        self.filter_menu.addAction(
            date_title
        )

        date_widget = QFrame()

        date_widget.setLayoutDirection(
            Qt.RightToLeft
        )

        # مهم:
        # جلوگیری از انتقال کلیک‌های بخش تاریخ
        # به خود QMenu
        date_widget.setAttribute(
            Qt.WA_NoMousePropagation,
            True
        )

        date_layout = QVBoxLayout(
            date_widget
        )

        date_layout.setContentsMargins(
            12,
            8,
            12,
            10
        )

        date_layout.setSpacing(
            6
        )

        # ==================================================
        # FROM
        # ==================================================

        from_label = QLabel(
            "از تاریخ"
        )

        from_label.setStyleSheet(
            """
            QLabel {
                color: #475569;
                background: transparent;
                border: none;
                font-weight: 600;
            }
            """
        )

        from_label.setAttribute(
            Qt.WA_TransparentForMouseEvents,
            True
        )

        date_layout.addWidget(
            from_label
        )

        self.from_date = JalaliDateEdit()

        date_layout.addWidget(
            self.from_date
        )

        # ==================================================
        # TO
        # ==================================================

        to_label = QLabel(
            "تا تاریخ"
        )

        to_label.setStyleSheet(
            """
            QLabel {
                color: #475569;
                background: transparent;
                border: none;
                font-weight: 600;
            }
            """
        )

        to_label.setAttribute(
            Qt.WA_TransparentForMouseEvents,
            True
        )

        date_layout.addWidget(
            to_label
        )

        self.to_date = JalaliDateEdit()

        date_layout.addWidget(
            self.to_date
        )

        # ==================================================
        # APPLY
        # ==================================================

        apply_button = QPushButton(
            "اعمال فیلتر"
        )

        apply_button.setCursor(
            Qt.PointingHandCursor
        )

        apply_button.setStyleSheet(
            """
            QPushButton {
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background: #1D4ED8;
            }
            """
        )

        apply_button.clicked.connect(
            self.emit_date_range
        )

        date_layout.addWidget(
            apply_button
        )

        widget_action = QWidgetAction(
            self
        )

        widget_action.setDefaultWidget(
            date_widget
        )

        self.filter_menu.addAction(
            widget_action
        )

    # ==================================================
    # EMIT DATE RANGE
    # ==================================================

    def emit_date_range(self):

        start_date = (
            self.from_date.date()
        )

        end_date = (
            self.to_date.date()
        )

        # --------------------------------------------------
        # مقایسه شمسی
        # --------------------------------------------------

        if start_date > end_date:

            start_date, end_date = (
                end_date,
                start_date
            )

            self.from_date.setDate(
                start_date
            )

            self.to_date.setDate(
                end_date
            )

        self.date_range_changed.emit(
            start_date,
            end_date
        )

        # فقط بعد از اعمال فیلتر بسته شود
        self.filter_menu.close()

    # ==================================================
    # RESET
    # ==================================================

    def reset_filters(self):

        today = jdatetime.date.today()

        self.search_input.blockSignals(
            True
        )

        self.search_input.clear()

        self.search_input.blockSignals(
            False
        )

        self.from_date.setDate(
            today
        )

        self.to_date.setDate(
            today
        )

        self.status_changed.emit(
            "all"
        )

        self.date_range_changed.emit(
            today,
            today
        )