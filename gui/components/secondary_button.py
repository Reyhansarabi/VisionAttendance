"""
==================================================
Project : حضور
File    : secondary_button.py
Author  : Reyhane Sarabi
Purpose : دکمه ثانویه پروژه
==================================================
"""

from PySide6.QtWidgets import (
    QPushButton,
    QGraphicsDropShadowEffect
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QColor

from theme.colors import Colors
from theme.fonts import Fonts


class SecondaryButton(QPushButton):
    """
    دکمه ثانویه پروژه

    ویژگی‌ها:
        - ظاهر مینیمال
        - گوشه گرد
        - سایه نرم
        - Hover
    """

    def __init__(
        self,
        text="",
        parent=None
    ):

        super().__init__(
            text,
            parent
        )

        self.setup_ui()

    # ==========================================
    # تنظیم ظاهر دکمه
    # ==========================================

    def setup_ui(self):

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setMinimumHeight(
            42
        )

        self.setFont(
            Fonts.button()
        )

        self.setStyleSheet(
            """
            QPushButton
            {
                background: #E8EDF5;

                color: #4A5568;

                border: 1px solid #CBD5E1;

                border-radius: 14px;

                padding: 8px 18px;
            }

            QPushButton:hover
            {
                background: #D6DEE8;

                color: #2D3748;

                border: 1px solid #A0AEC0;
            }

            QPushButton:pressed
            {
                background: #C7D2DE;

                color: #2D3748;

                border: 1px solid #90A0B0;
            }
            """
        )

        # ==================================
        # سایه نرم
        # ==================================

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            15
        )

        shadow.setOffset(
            0,
            4
        )

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                25
            )
        )

        self.setGraphicsEffect(
            shadow
        )