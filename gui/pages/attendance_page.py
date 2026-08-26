from pathlib import Path

import cv2

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QMessageBox,
    QGraphicsDropShadowEffect,
)

from PySide6.QtCore import (
    Qt,
    QEvent,
    QTimer,
)

from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QPen,
    QColor,
)

from theme.fonts import Fonts
from theme.colors import Colors

from gui.components.glass_card import GlassCard
from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton

from controllers.attendance_controller import AttendanceController
from core.face_recognizer import FaceRecognizer


class AttendancePage(QWidget):

    def __init__(self, role="admin", user_id=None, parent=None):

        super().__init__(parent)

        # ==================================================
        # SESSION / PERMISSIONS
        # ==================================================

        self.role = str(role or "user").strip().lower()
        self.user_id = user_id

        if self.role not in ("admin", "user"):
            self.role = "user"

        # ==================================================
        # DATA
        # ==================================================

        self.repository = AttendanceController()
        self.face_recognizer = FaceRecognizer()

        self.image_path = None
        self.current_pixmap = None

        self.detected_user = None
        self.current_bbox = None

        # آیا اصلاً چهره‌ای پیدا شده؟
        self.face_found = False

        # آیا چهره متعلق به کاربر ثبت‌شده است؟
        self.user_found = False

        # ==================================================
        # UI
        # ==================================================

        self.setup_ui()

        self._success_timer = QTimer(self)
        self._success_timer.setSingleShot(True)
        self._success_timer.timeout.connect(self._finish_attendance_success)

        # ==================================================
        # CONNECTIONS
        # ==================================================

        self.select_image.clicked.connect(
            self.select_image_file
        )

        self.enter_button.clicked.connect(
            self.register_entry
        )

        self.exit_button.clicked.connect(
            self.register_exit
        )

        # ==================================================
        # GLOBAL EVENT FILTER
        # ==================================================

        app = self.window().windowHandle()

        QApplication = __import__(
            "PySide6.QtWidgets",
            fromlist=["QApplication"]
        ).QApplication

        application = QApplication.instance()

        if application is not None:

            application.installEventFilter(
                self
            )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            22,
            30,
            22
        )

        main_layout.setSpacing(
            15
        )

        # ==================================================
        # MAIN CARD
        # ==================================================

        main_card = GlassCard()

        main_card.setFixedWidth(
            560
        )

        main_card.setMinimumHeight(
            560
        )

        main_card.layout.setContentsMargins(
            30,
            26,
            30,
            26
        )

        main_card.layout.setSpacing(
            12
        )

        # ==================================================
        # CARD SHADOW
        # ==================================================

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            50
        )

        shadow.setOffset(
            0,
            14
        )

        shadow.setColor(
            QColor(
                37,
                99,
                235,
                45
            )
        )

        main_card.setGraphicsEffect(
            shadow
        )

        # ==================================================
        # CARD STYLE
        # ==================================================

        main_card.setStyleSheet(
            """
            QWidget {
                background: rgba(255, 255, 255, 0.96);
                border-radius: 20px;
            }
            """
        )

        # ==================================================
        # TITLE
        # ==================================================

        title = QLabel(
            "عملیات حضور"
        )

        title.setFont(
            Fonts.heading()
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.TEXT};
                background: transparent;
                border: none;
                padding: 0px;
            }}
            """
        )

        main_card.layout.addWidget(
            title
        )

        # ==================================================
        # SPACE
        # ==================================================

        main_card.layout.addSpacing(
            8
        )

        # ==================================================
        # PREVIEW CONTAINER
        # ==================================================

        preview_container = QWidget()

        preview_container.setFixedHeight(
            340
        )

        preview_container.setStyleSheet(
            """
            QWidget {
                background: transparent;
                border: none;
            }
            """
        )

        preview_layout = QVBoxLayout(
            preview_container
        )

        preview_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        preview_layout.setAlignment(
            Qt.AlignCenter
        )

        self.attendance_success_label = QLabel("")
        self.attendance_success_label.setAlignment(Qt.AlignCenter)
        self.attendance_success_label.setStyleSheet(
            "QLabel { color: #16A34A; background: transparent; border: none; "
            "font-size: 11px; font-weight: bold; padding: 0px; }"
        )
        self.attendance_success_label.hide()
        preview_layout.addWidget(
            self.attendance_success_label,
            alignment=Qt.AlignCenter
        )

        # ==================================================
        # PREVIEW
        # ==================================================

        self.preview = QLabel()

        self.preview.setFixedSize(
            300,
            300
        )

        self.preview.setAlignment(
            Qt.AlignCenter
        )

        self.preview.setStyleSheet(
            """
            QLabel {
                background: white;
                border: 1px solid #D9E3EE;
                border-radius: 16px;
                padding: 0px;
            }
            """
        )

        self.preview.setPixmap(QIcon("assets/icons/camera.svg").pixmap(64, 64))

        self.preview.setFont(
            Fonts.title()
        )

        preview_layout.addWidget(
            self.preview,
            alignment=Qt.AlignCenter
        )

        main_card.layout.addWidget(
            preview_container
        )

        # ==================================================
        # STATUS
        # ==================================================

        self.status_label = QLabel(
            "برای شروع یک تصویر انتخاب کنید"
        )

        self.status_label.setFont(
            Fonts.small()
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setWordWrap(
            True
        )

        self.set_status_default()

        main_card.layout.addWidget(
            self.status_label
        )

        # ==================================================
        # SPACE BEFORE SELECT BUTTON
        # ==================================================

        main_card.layout.addSpacing(
            12
        )

        # ==================================================
        # SELECT IMAGE
        # ==================================================

        self.select_image = SecondaryButton(
            "انتخاب تصویر"
        )

        self.select_image.setMinimumHeight(
            42
        )

        self.select_image.setCursor(
            Qt.PointingHandCursor
        )

        self.select_image.setFocusPolicy(
            Qt.StrongFocus
        )

        main_card.layout.addWidget(
            self.select_image
        )

        # ==================================================
        # SPACE
        # ==================================================

        main_card.layout.addSpacing(
            8
        )

        # ==================================================
        # ACTION BUTTONS
        # ==================================================

        buttons_layout = QHBoxLayout()

        buttons_layout.setSpacing(
            10
        )

        # ==================================================
        # ENTRY
        # ==================================================

        self.enter_button = PrimaryButton(
            "ثبت ورود"
        )

        self.enter_button.setMinimumHeight(
            42
        )

        self.enter_button.setCursor(
            Qt.PointingHandCursor
        )

        self.enter_button.setFocusPolicy(
            Qt.StrongFocus
        )

        # ==================================================
        # EXIT
        # ==================================================

        self.exit_button = SecondaryButton(
            "ثبت خروج"
        )

        self.exit_button.setMinimumHeight(
            42
        )

        self.exit_button.setCursor(
            Qt.PointingHandCursor
        )

        self.exit_button.setFocusPolicy(
            Qt.StrongFocus
        )

        buttons_layout.addWidget(
            self.enter_button
        )

        buttons_layout.addWidget(
            self.exit_button
        )

        main_card.layout.addLayout(
            buttons_layout
        )

        # ==================================================
        # CENTER CARD
        # ==================================================

        card_wrapper = QHBoxLayout()

        card_wrapper.setContentsMargins(
            0,
            0,
            0,
            0
        )

        card_wrapper.addStretch()

        card_wrapper.addWidget(
            main_card
        )

        card_wrapper.addStretch()

        main_layout.addLayout(
            card_wrapper
        )

        main_layout.addStretch()

    # ==================================================
    # STATUS DEFAULT
    # ==================================================

    def set_status_default(self):

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #94A3B8;
                background: transparent;
                border: none;
                padding: 3px;
            }
            """
        )

    # ==================================================
    # STATUS SUCCESS
    # ==================================================

    def set_status_success(self):

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #16A34A;
                background: transparent;
                border: none;
                font-weight: bold;
                padding: 3px;
            }
            """
        )

    # ==================================================
    # STATUS ERROR
    # ==================================================

    def set_status_error(self):

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #EF4444;
                background: transparent;
                border: none;
                font-weight: bold;
                padding: 3px;
            }
            """
        )

    # ==================================================
    # SELECT IMAGE
    # ==================================================

    def select_image_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "انتخاب تصویر",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if not file_path:
            return

        self.image_path = Path(
            file_path
        )

        pixmap = QPixmap(
            str(self.image_path)
        )

        if pixmap.isNull():

            self.current_pixmap = None
            self.current_bbox = None
            self.detected_user = None

            self.face_found = False
            self.user_found = False

            self.preview.clear()

            self.preview.setPixmap(QIcon("assets/icons/camera.svg").pixmap(64, 64))

            self.set_status_error()

            self.status_label.setText(
                "تصویر قابل خواندن نیست"
            )

            return

        self.current_pixmap = pixmap

        # ==================================================
        # FACE RECOGNITION
        # ==================================================

        result = self.recognize_user()

        if result is None:

            self.show_preview(
                pixmap,
                bbox=None,
                found=False
            )

            return

        self.show_preview(
            pixmap,
            bbox=result.get("bbox"),
            found=result.get(
                "found",
                False
            )
        )

    # ==================================================
    # SHOW PREVIEW
    # ==================================================

    def show_preview(
        self,
        pixmap,
        bbox=None,
        found=False
    ):

        if pixmap.isNull():
            return

        target_width = self.preview.width()
        target_height = self.preview.height()

        # ==================================================
        # SCALE IMAGE
        # ==================================================

        scaled = pixmap.scaled(
            target_width,
            target_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # ==================================================
        # RESULT PIXMAP
        # ==================================================

        result_pixmap = QPixmap(
            target_width,
            target_height
        )

        result_pixmap.fill(
            Qt.transparent
        )

        painter = QPainter(
            result_pixmap
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # ==================================================
        # IMAGE POSITION
        # ==================================================

        offset_x = (
            target_width
            - scaled.width()
        ) // 2

        offset_y = (
            target_height
            - scaled.height()
        ) // 2

        painter.drawPixmap(
            offset_x,
            offset_y,
            scaled
        )

        # ==================================================
        # BOUNDING BOX
        # ==================================================

        if bbox is not None:

            x1, y1, x2, y2 = bbox

            original_width = pixmap.width()
            original_height = pixmap.height()

            scale_x = (
                scaled.width()
                / original_width
            )

            scale_y = (
                scaled.height()
                / original_height
            )

            scale = min(
                scale_x,
                scale_y
            )

            rect_x = (
                offset_x
                + x1 * scale
            )

            rect_y = (
                offset_y
                + y1 * scale
            )

            rect_width = (
                x2 - x1
            ) * scale

            rect_height = (
                y2 - y1
            ) * scale

            # ==================================================
            # BOX COLOR
            # ==================================================

            if found:

                color = QColor(
                    "#22C55E"
                )

            else:

                color = QColor(
                    "#EF4444"
                )

            pen = QPen(
                color
            )

            pen.setWidth(
                3
            )

            pen.setJoinStyle(
                Qt.MiterJoin
            )

            painter.setPen(
                pen
            )

            painter.setBrush(
                Qt.NoBrush
            )

            painter.drawRect(
                int(rect_x),
                int(rect_y),
                int(rect_width),
                int(rect_height)
            )

        painter.end()

        # ==================================================
        # SET IMAGE
        # ==================================================

        self.preview.setPixmap(
            result_pixmap
        )

        self.preview.setText(
            ""
        )

    # ==================================================
    # RECOGNIZE USER
    # ==================================================

    def recognize_user(self):

        if self.image_path is None:
            return None

        users = self.repository.get_users()

        try:

            result = self.face_recognizer.recognize(
                str(self.image_path),
                users
            )

        except Exception as error:

            print(
                "Recognition error:",
                error
            )

            self.face_found = False
            self.user_found = False
            self.detected_user = None
            self.current_bbox = None

            self.set_status_error()

            self.status_label.setText(
                "خطا در تشخیص تصویر"
            )

            return None

        # ==================================================
        # BBOX
        # ==================================================

        self.current_bbox = result.get(
            "bbox"
        )

        self.face_found = (
            self.current_bbox is not None
        )

        # ==================================================
        # NO FACE
        # ==================================================

        if not self.face_found:

            self.detected_user = None
            self.user_found = False

            self.set_status_error()

            self.status_label.setText(
                "هیچ چهره‌ای در تصویر پیدا نشد"
            )

            return result

        # ==================================================
        # FACE FOUND BUT UNKNOWN
        # ==================================================

        if not result.get(
            "found",
            False
        ):

            self.detected_user = None
            self.user_found = False

            self.set_status_error()

            self.status_label.setText(
                "چهره پیدا شد، اما در سیستم ثبت نشده است"
            )

            return result

        # ==================================================
        # USER
        # ==================================================

        user = result.get(
            "user"
        )

        if user is None:

            self.detected_user = None
            self.user_found = False

            self.set_status_error()

            self.status_label.setText(
                "چهره پیدا شد، اما کاربر شناسایی نشد"
            )

            return result

        self.detected_user = user
        self.user_found = True

        # Normal users may only operate on their own attendance record.
        if self.role == "user":
            if self.user_id is None:
                self.detected_user = None
                self.user_found = False
                self.set_status_error()
                self.status_label.setText(
                    "حساب شما به یک کاربر ثبت‌شده متصل نیست."
                )
                return result

            if int(user["id"]) != int(self.user_id):
                self.detected_user = None
                self.user_found = False
                self.set_status_error()
                self.status_label.setText(
                    "دسترسی غیرمجاز: این چهره متعلق به حساب واردشده نیست."
                )
                return result

        full_name = (
            f"{user['first_name']} "
            f"{user['last_name']}"
        )

        score = result.get(
            "score",
            0.0
        )

        self.set_status_success()
        score_percent = max(0.0, min(100.0, float(score) * 100.0))
        self.status_label.setText(
            f"چهره شناسایی شد: {full_name}  |  درصد تطابق: {score_percent:.1f}%"
        )

        return result

    # ==================================================
    # REGISTER ENTRY
    # ==================================================

    def register_entry(self):

        if not self.face_found:

            self.show_message(
                "چهره پیدا نشد",
                "در تصویر انتخاب‌شده هیچ چهره‌ای پیدا نشد."
            )

            return

        if (
            not self.user_found
            or self.detected_user is None
        ):

            self.show_message(
                "کاربر شناسایی نشد",
                "چهره پیدا شد، اما این شخص در سیستم ثبت نشده است."
            )

            return

        user = self.detected_user

        try:

            result = self.repository.register_entry(
                user["id"]
            )

        except Exception as error:

            print(
                "Entry error:",
                error
            )

            self.show_message(
                "خطا",
                "ثبت ورود انجام نشد."
            )

            return

        if result.get("duplicate"):
            self.set_status_error()
            self.status_label.setText("این ورود قبلاً برای امروز ثبت شده است.")
        else:
            self.set_status_success()
            # Keep the recognition name and match percentage visible until
            # the page is cleared or the user navigates away.
            self.attendance_success_label.setText("✓ ورود با موفقیت ثبت شد")
            self.attendance_success_label.show()
            self._success_timer.start(2000)

    # ==================================================
    # REGISTER EXIT
    # ==================================================

    def register_exit(self):

        if not self.face_found:

            self.show_message(
                "چهره پیدا نشد",
                "در تصویر انتخاب‌شده هیچ چهره‌ای پیدا نشد."
            )

            return

        if (
            not self.user_found
            or self.detected_user is None
        ):

            self.show_message(
                "کاربر شناسایی نشد",
                "چهره پیدا شد، اما این شخص در سیستم ثبت نشده است."
            )

            return

        user = self.detected_user

        try:

            result = self.repository.register_exit(
                user["id"]
            )

        except Exception as error:

            print(
                "Exit error:",
                error
            )

            self.show_message(
                "خطا",
                "ثبت خروج انجام نشد."
            )

            return

        if result.get("no_entry"):
            self.set_status_error()
            self.status_label.setText(
                "برای این کاربر امروز ورود ثبت نشده است؛ خروج ثبت نشد."
            )
        else:
            self.set_status_success()
            # Keep the recognition name and match percentage visible until
            # the page is cleared or the user navigates away.
            self.attendance_success_label.setText("✓ خروج با موفقیت ثبت شد")
            self.attendance_success_label.show()
            self._success_timer.start(2000)

    # ==================================================
    # CLEAR PAGE
    # ==================================================

    def _finish_attendance_success(self):
        self.attendance_success_label.hide()

    def clear_page(self):

        if hasattr(self, "_success_timer") and self._success_timer.isActive():
            self._success_timer.stop()

        self.attendance_success_label.hide()

        self.image_path = None
        self.current_pixmap = None

        self.detected_user = None
        self.current_bbox = None

        self.face_found = False
        self.user_found = False

        self.preview.clear()

        self.preview.setPixmap(
            QPixmap()
        )

        self.preview.setPixmap(QIcon("assets/icons/camera.svg").pixmap(64, 64))

        self.set_status_default()

        self.status_label.setText(
            "برای شروع یک تصویر انتخاب کنید"
        )

    def hideEvent(self, event):

        # Remove the captured face image when leaving the page, while
        # keeping it visible during the two-second success message.
        self.clear_page()
        super().hideEvent(event)

    # ==================================================
    # GLOBAL EVENT FILTER
    # ==================================================

    def eventFilter(
        self,
        watched,
        event
    ):

        if (
            event.type()
            == QEvent.Type.MouseButtonPress
        ):

            self.enter_button.clearFocus()
            self.exit_button.clearFocus()
            self.select_image.clearFocus()

        return super().eventFilter(
            watched,
            event
        )

    # ==================================================
    # MOUSE PRESS
    # ==================================================

    def mousePressEvent(
        self,
        event
    ):

        self.enter_button.clearFocus()
        self.exit_button.clearFocus()
        self.select_image.clearFocus()

        self.setFocus(
            Qt.MouseFocusReason
        )

        super().mousePressEvent(
            event
        )

    # ==================================================
    # MESSAGE
    # ==================================================

    def show_message(
        self,
        title,
        text
    ):

        QMessageBox.information(
            self,
            title,
            text
        )