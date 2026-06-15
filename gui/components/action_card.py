"""
==================================================
Project : حضور
File    : action_card.py
Author  : Reyhane Sarabi
Purpose : Dashboard Action Card Component
==================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGraphicsDropShadowEffect
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QPropertyAnimation,
    QEasingCurve
)

from PySide6.QtGui import QColor

from theme.colors import Colors
from theme.fonts import Fonts


class ActionCard(QFrame):

    clicked = Signal()

    def __init__(
        self,
        icon,
        title,
        description,
        parent=None
    ):

        super().__init__(parent)

        self.icon = icon
        self.title = title
        self.description = description

        self.setup_ui()

    # ======================================
    # UI
    # ======================================

    def setup_ui(self):

        self.setFixedSize(
            300,
            220
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setObjectName(
            "ActionCard"
        )

        # ---------- Shadow ----------

        self.shadow = QGraphicsDropShadowEffect()

        self.shadow.setBlurRadius(35)

        self.shadow.setOffset(0, 8)

        self.shadow.setColor(
            QColor(
                0,
                0,
                0,
                35
            )
        )

        self.setGraphicsEffect(
            self.shadow
        )

        # ---------- Animation ----------

        self.shadow_anim = QPropertyAnimation(
            self.shadow,
            b"blurRadius"
        )

        self.shadow_anim.setDuration(180)

        self.shadow_anim.setEasingCurve(
            QEasingCurve.OutCubic
        )

        # ---------- Layout ----------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        layout.setSpacing(14)

        layout.setAlignment(
            Qt.AlignCenter
        )

        # ---------- Icon ----------

        self.icon_label = QLabel(
            self.icon
        )

        self.icon_label.setAlignment(
            Qt.AlignCenter
        )

        self.icon_label.setStyleSheet(
            """
            font-size:48px;
            color:#444;
            """
        )

        layout.addWidget(
            self.icon_label
        )

        # ---------- Title ----------

        self.title_label = QLabel(
            self.title
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.title_label.setFont(
            Fonts.title()
        )

        layout.addWidget(
            self.title_label
        )

        # ---------- Description ----------

        self.desc_label = QLabel(
            self.description
        )

        self.desc_label.setAlignment(
            Qt.AlignCenter
        )

        self.desc_label.setFont(
            Fonts.small()
        )

        layout.addWidget(
            self.desc_label
        )

        self.normal_style()

            # ======================================
    # حالت عادی
    # ======================================

    def normal_style(self):

        self.setStyleSheet(
            f"""
            QFrame#ActionCard
            {{
                background:{Colors.CARD};
                border-radius:22px;
                border:1px solid {Colors.BORDER};
            }}
            """
        )

        self.title_label.setStyleSheet(
            f"""
            color:{Colors.TEXT};
            font-weight:600;
            """
        )

        self.desc_label.setStyleSheet(
            f"""
            color:{Colors.MUTED};
            """
        )

        self.icon_label.setStyleSheet(
            """
            font-size:48px;
            color:#444;
            """
        )

        self.shadow.setBlurRadius(35)

        self.shadow.setOffset(0, 8)

        self.shadow.setColor(
            QColor(
                0,
                0,
                0,
                35
            )
        )


    # ======================================
    # Hover
    # ======================================

    def enterEvent(self, event):

        self.setStyleSheet(
            f"""
            QFrame#ActionCard
            {{
                background:#F6FAFF;
                border-radius:22px;
                border:2px solid {Colors.PRIMARY};
            }}
            """
        )

        self.title_label.setStyleSheet(
            f"""
            color:{Colors.PRIMARY};
            font-weight:bold;
            """
        )

        self.desc_label.setStyleSheet(
            """
            color:#5B7AA6;
            """
        )

        self.icon_label.setStyleSheet(
            f"""
            font-size:56px;
            color:{Colors.PRIMARY};
            """
        )

        self.shadow_anim.stop()

        self.shadow_anim.setStartValue(
            self.shadow.blurRadius()
        )

        self.shadow_anim.setEndValue(
            55
        )

        self.shadow_anim.start()

        self.shadow.setOffset(0, 14)

        self.shadow.setColor(
            QColor(
                76,
                141,
                255,
                90
            )
        )

        super().enterEvent(event)


    # ======================================
    # Leave
    # ======================================

    def leaveEvent(self, event):

        self.normal_style()

        super().leaveEvent(event)

            # ======================================
    # Mouse Press
    # ======================================

    def mousePressEvent(self, event):

        self.setStyleSheet(
            f"""
            QFrame#ActionCard
            {{
                background:#EAF4FF;
                border-radius:22px;
                border:2px solid {Colors.PRIMARY};
            }}
            """
        )

        self.shadow.setBlurRadius(20)

        self.shadow.setOffset(0, 4)

        self.clicked.emit()

        super().mousePressEvent(event)


    # ======================================
    # Mouse Release
    # ======================================

    def mouseReleaseEvent(self, event):

        if self.underMouse():

            self.enterEvent(event)

        else:

            self.leaveEvent(event)

        super().mouseReleaseEvent(event)

        