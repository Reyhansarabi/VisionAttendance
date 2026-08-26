"""
==================================================
Project : حضور
File    : glass_card.py
Author  : Reyhane Sarabi
Purpose : کارت اصلی برنامه با گوشه گرد و سایه نرم
==================================================
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

from theme.colors import Colors


class GlassCard(QFrame):
    """
    کارت استاندارد پروژه

    همه فرم‌ها و جدول‌ها داخل این کارت قرار می‌گیرند.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    # ==========================================
    # تنظیم ظاهر کارت
    # ==========================================

    def setup_ui(self):

        self.setObjectName("GlassCard")

        self.setStyleSheet(f"""
            QFrame#GlassCard
            {{
                background: {Colors.CARD};

                border-radius:18px;

                border:1px solid {Colors.BORDER};
            }}
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(25)

        shadow.setOffset(0, 6)

        shadow.setColor(QColor(0, 0, 0, 35))

        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(20, 20, 20, 20)

        self.layout.setSpacing(15)

        self.setLayout(self.layout)