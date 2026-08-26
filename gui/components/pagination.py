"""
==================================================
Project : حضور
File    : pagination.py
Author  : Reyhane Sarabi
Purpose : Pagination Component
==================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt, Signal

from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton

from theme.fonts import Fonts


class Pagination(QFrame):
    """
    صفحه‌بندی جدول

    فعلاً فقط ظاهر

    بعداً:
        تعداد صفحات
        قبلی
        بعدی
        شماره صفحات
    """

    page_changed = Signal(int)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.current_page = 1
        self.total_pages = 1

        self.setup_ui()

        self.previous_btn.clicked.connect(self.previous_page)
        self.next_btn.clicked.connect(self.next_page)

    # ==================================

    def setup_ui(self):

        self.setFixedHeight(55)

        self.setStyleSheet("""
        QFrame{
            background:transparent;
        }
        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(10)

        layout.addStretch()

        # ----------------------
        # Previous
        # ----------------------

        self.previous_btn = SecondaryButton(
            "← قبلی"
        )

        layout.addWidget(
            self.previous_btn
        )

        # ----------------------
        # Label
        # ----------------------

        self.page_label = QLabel()

        self.page_label.setAlignment(
            Qt.AlignCenter
        )

        self.page_label.setFont(
            Fonts.small()
        )

        layout.addWidget(
            self.page_label
        )

        # ----------------------
        # Next
        # ----------------------

        self.next_btn = SecondaryButton(
            "بعدی →"
        )

        layout.addWidget(
            self.next_btn
        )

        layout.addStretch()

        self.update_label()

    # ==================================

    def previous_page(self):

        if self.current_page > 1:
            self.set_pages(self.current_page - 1, self.total_pages)
            self.page_changed.emit(self.current_page)

    def next_page(self):

        if self.current_page < self.total_pages:
            self.set_pages(self.current_page + 1, self.total_pages)
            self.page_changed.emit(self.current_page)

    def update_label(self):

        self.page_label.setText(

            f"صفحه {self.current_page} از {self.total_pages}"

        )

    # ==================================

    def set_pages(self, current, total):

        self.current_page = current

        self.total_pages = total

        self.update_label()