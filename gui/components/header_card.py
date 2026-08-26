from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QGridLayout
)

from PySide6.QtCore import Qt

from theme.colors import Colors
from theme.fonts import Fonts

class HeaderCard(QWidget):

    """
    هدر اصلی برنامه

    شامل:
    - عنوان در مرکز
    """

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setup_ui()

    # ======================================
    # UI
    # ======================================

    def setup_ui(self):

        self.setFixedHeight(95)

        # ======================================
        # MAIN GRID
        # ======================================

        main_layout = QGridLayout(self)

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)

        # ======================================
        # TITLE
        # ======================================

        text_layout = QVBoxLayout()

        text_layout.setSpacing(2)

        text_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel(
            "FaceRecognitionSystem"
        )

        title.setFont(
            Fonts.large_title()
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.PRIMARY};
                font-weight: bold;
                background: transparent;
                border: none;
            }}
            """
        )

        subtitle = QLabel(
            "سیستم هوشمند مدیریت حضور و غیاب"
        )

        subtitle.setFont(
            Fonts.heading()
        )

        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.MUTED};
                background: transparent;
                border: none;
            }}
            """
        )

        # ======================================
        # LINE
        # ======================================

        line = QFrame()

        line.setFixedSize(
            120,
            2
        )

        line.setStyleSheet(
            f"""
            QFrame {{
                background: {Colors.PRIMARY};
                border: none;
            }}
            """
        )

        text_layout.addWidget(
            title,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        text_layout.addSpacing(5)

        text_layout.addWidget(
            line,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        text_layout.addSpacing(5)

        text_layout.addWidget(
            subtitle,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # ======================================
        # TITLE IN CENTER
        # ======================================

        main_layout.addLayout(
            text_layout,
            0,
            1,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # ======================================
        # GRID STRETCH
        # ======================================

        main_layout.setColumnStretch(
            0,
            1
        )

        main_layout.setColumnStretch(
            1,
            3
        )

        main_layout.setColumnStretch(
            2,
            1
        )

        main_layout.setRowStretch(
            0,
            1
        )
