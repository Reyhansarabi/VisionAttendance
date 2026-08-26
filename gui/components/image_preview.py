# ==================================================
# Project : حضور
# File    : image_preview.py
# Author  : Reyhane Sarabi
# Purpose : Image Preview Component
# ==================================================


from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
)

from theme.fonts import Fonts
from theme.colors import Colors


class ImagePreview(QWidget):
    """
    پیش نمایش تصویر

    استفاده در:
        - ثبت کاربر
        - ورود
        - خروج
    """

    def __init__(self, parent=None):

        super().__init__(parent)

        self.current_pixmap = None

        self.setup_ui()

    # ==========================================
    # UI
    # ==========================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(0)

        # ======================================
        # Preview Card
        # ======================================

        self.image_label = QLabel()

        self.image_label.setFixedSize(
            420,
            420
        )

        self.image_label.setAlignment(
            Qt.AlignCenter
        )

        # --------------------------------------
        # کادر واقعی Preview
        # --------------------------------------

        self.image_label.setStyleSheet(
            """
            QLabel {
                background: #FFFFFF;
                border: 2px solid #D9E2EC;
                border-radius: 18px;
                color: #94A3B8;
                padding: 0px;
            }
            """
        )

        # ======================================
        # Content inside preview
        # ======================================

        preview_content = QWidget()

        preview_content.setAttribute(
            Qt.WA_TranslucentBackground
        )

        preview_content.setStyleSheet(
            """
            QWidget {
                background: transparent;
                border: none;
            }
            """
        )

        preview_layout = QVBoxLayout(
            preview_content
        )

        preview_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        preview_layout.setSpacing(8)

        preview_layout.setAlignment(
            Qt.AlignCenter
        )

        # ======================================
        # Camera Icon
        # ======================================

        self.camera_icon = QLabel()
        self.camera_icon.setPixmap(
            QIcon("assets/icons/camera.svg").pixmap(42, 42)
        )

        self.camera_icon.setAlignment(
            Qt.AlignCenter
        )

        self.camera_icon.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
                color: #94A3B8;
                font-size: 42px;
            }
            """
        )

        self.camera_icon.setFont(
            Fonts.title()
        )

        preview_layout.addWidget(
            self.camera_icon,
            alignment=Qt.AlignCenter
        )

        # ======================================
        # Caption
        # ======================================

        self.caption = QLabel(
            "برای شروع، یک تصویر انتخاب کنید"
        )

        self.caption.setAlignment(
            Qt.AlignCenter
        )

        self.caption.setWordWrap(
            False
        )

        self.caption.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.TEXT};

                background: transparent;

                border: none;

                padding: 0px;
            }}
            """
        )

        self.caption.setFont(
            Fonts.small()
        )

        preview_layout.addWidget(
            self.caption,
            alignment=Qt.AlignCenter
        )

        # ======================================
        # قرار دادن محتوا داخل کادر
        # ======================================

        outer_layout = QVBoxLayout(
            self.image_label
        )

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        outer_layout.setAlignment(
            Qt.AlignCenter
        )

        outer_layout.addWidget(
            preview_content,
            alignment=Qt.AlignCenter
        )

        # ======================================
        # Main Layout
        # ======================================

        layout.addWidget(
            self.image_label,
            alignment=Qt.AlignCenter
        )

    # ==========================================
    # Load Image
    # ==========================================

    def set_image(
        self,
        image_path
    ):

        pixmap = QPixmap(
            image_path
        )

        if pixmap.isNull():
            return

        self.current_pixmap = pixmap

        scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.camera_icon.hide()
        self.caption.hide()

        self.image_label.setPixmap(
            scaled
        )

        self.image_label.setAlignment(
            Qt.AlignCenter
        )

    # ==========================================
    # Clear Image
    # ==========================================

    def clear(self):

        self.current_pixmap = None

        self.image_label.clear()

        self.image_label.setPixmap(
            QPixmap()
        )

        self.camera_icon.show()
        self.caption.show()

        self.caption.setText(
            "برای شروع، یک تصویر انتخاب کنید"
        )

        self.image_label.setAlignment(
            Qt.AlignCenter
        )

