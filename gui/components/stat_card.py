"""
==================================================
Project : حضور
File    : stat_card.py
Author  : Reyhane Sarabi
Purpose : Dashboard Statistic Card
==================================================
"""

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt

from gui.components.hover_card import HoverCard
from theme.colors import Colors
from theme.fonts import Fonts


class StatCard(HoverCard):

    def __init__(
        self,
        title,
        value,
        value_color=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        # ==================================================
        # Card Size
        # ==================================================

        self.setFixedHeight(
            150
        )

        # ==================================================
        # Card Style
        # ==================================================

        self.setStyleSheet(
            """
            QFrame
            {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
            }
            """
        )

        # ==================================================
        # Layout
        # ==================================================

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(
            8
        )

        layout.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # Title
        # ==================================================

        self.title_label = QLabel(
            title
        )

        self.title_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        self.title_label.setFont(
            Fonts.heading()
        )

        self.title_label.setStyleSheet(
            f"""
            QLabel
            {{
                color: {Colors.MUTED};
                background: transparent;
                border: none;
            }}
            """
        )

        # ==================================================
        # Value
        # ==================================================

        self.value_label = QLabel(
            str(value)
        )

        self.value_label.setAlignment(
            Qt.AlignCenter
        )

        self.value_label.setFont(
            Fonts.large_title()
        )

        # اگر رنگ داده نشده بود،
        # رنگ اصلی برنامه استفاده شود.

        if value_color is None:

            value_color = Colors.PRIMARY

        self.value_color = value_color

        self.value_label.setStyleSheet(
            f"""
            QLabel
            {{
                color: {self.value_color};
                background: transparent;
                border: none;
                font-weight: bold;
            }}
            """
        )

        # ==================================================
        # Add Widgets
        # ==================================================

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.value_label
        )

    # ==================================================
    # Set Value
    # ==================================================

    def set_value(
        self,
        value
    ):

        self.value_label.setText(
            str(value)
        )

    # ==================================================
    # Set Value Color
    # ==================================================

    def set_value_color(
        self,
        color
    ):

        self.value_color = color

        self.value_label.setStyleSheet(
            f"""
            QLabel
            {{
                color: {self.value_color};
                background: transparent;
                border: none;
                font-weight: bold;
            }}
            """
        )