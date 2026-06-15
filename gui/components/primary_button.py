"""
==================================================
Project : حضور
File    : primary_button.py
Author  : Reyhane Sarabi
Purpose : دکمه اصلی پروژه
==================================================
"""

from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor

from theme.colors import Colors
from theme.fonts import Fonts


class PrimaryButton(QPushButton):
    """
    دکمه اصلی پروژه

    دارای:
        - Radius
        - Hover
        - Shadow
        - Press Animation
    """

    def __init__(self, text="", parent=None):

        super().__init__(text, parent)

        self.setup_ui()

    # ==========================================
    # تنظیم ظاهر
    # ==========================================

    def setup_ui(self):

        self.setCursor(Qt.PointingHandCursor)

        self.setMinimumHeight(42)

        self.setFont(Fonts.button())

        self.setStyleSheet(f"""
            QPushButton
            {{
                background:{Colors.PRIMARY};

                color:white;

                border:none;

                border-radius:14px;

                padding:8px 18px;
            }}

            QPushButton:hover
            {{
                background:{Colors.PRIMARY_HOVER};
            }}

            QPushButton:pressed
            {{
                background:#2D6CDF;
            }}
        """)

        # ---------- Shadow ----------

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(18)

        shadow.setOffset(0, 5)

        shadow.setColor(QColor(0, 0, 0, 35))

        self.setGraphicsEffect(shadow)

    # ==========================================
    # کلیک نرم
    # ==========================================

    def mousePressEvent(self, event):

        self.animate_click(0.97)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        self.animate_click(1)

        super().mouseReleaseEvent(event)

    def animate_click(self, scale):

        geometry = self.geometry()

        w = geometry.width()
        h = geometry.height()

        new_w = int(w * scale)
        new_h = int(h * scale)

        x = geometry.x() + (w - new_w) // 2
        y = geometry.y() + (h - new_h) // 2

        self.anim = QPropertyAnimation(self, b"geometry")

        self.anim.setDuration(120)

        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        self.anim.setStartValue(self.geometry())

        self.anim.setEndValue(
            geometry.__class__(x, y, new_w, new_h)
        )

        self.anim.start()