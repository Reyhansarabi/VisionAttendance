# ==================================================
# Project : حضور
# File    : register_page.py
# Author  : Reyhane Sarabi
# Purpose : Register Page
# ==================================================

from pathlib import Path
import pickle

from PySide6.QtCore import Qt, QEvent, QTimer, QRegularExpression

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QGraphicsDropShadowEffect
)

from PySide6.QtGui import QColor, QRegularExpressionValidator

from gui.components.glass_card import GlassCard
from gui.components.image_preview import ImagePreview
from gui.components.rounded_input import RoundedLineEdit
from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton

from controllers.register_controller import RegisterController

from theme.fonts import Fonts
from theme.colors import Colors

from core.face_recognizer import FaceRecognizer


class RegisterPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        # ==================================================
        # Data
        # ==================================================

        self.image_path = None
        self.current_face_info = None

        self.repository = RegisterController()

        self.face_recognizer = FaceRecognizer()

        # ==================================================
        # UI
        # ==================================================

        self.setup_ui()

        self.select_image.clicked.connect(
            self.select_image_file
        )

        self.register_button.clicked.connect(
            self.register_user
        )

        # ==================================================
        # Keyboard Navigation
        # ==================================================

        self.current_fields = [
            self.first_name,
            self.last_name,
            self.national_code
        ]

        self.current_submit = (
            self.register_button
        )

        self._success_timer = QTimer(self)
        self._success_timer.setSingleShot(True)
        self._success_timer.timeout.connect(self._finish_registration_success)

        self.installEventFilter(self)

    # ==================================================
    # Event Filter — Keyboard Navigation
    # ==================================================

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyPress:

            key = event.key()

            # --------------------------------------------
            # Enter → Click Submit Button
            # --------------------------------------------

            if key in (
                Qt.Key_Return,
                Qt.Key_Enter
            ):

                if self.current_submit is not None:

                    self.current_submit.click()

                    return True

            # --------------------------------------------
            # Page Down / Page Up → Navigate Fields
            # --------------------------------------------

            if key in (
                Qt.Key_Down,
                Qt.Key_Up,
                Qt.Key_PageDown,
                Qt.Key_PageUp
            ):

                if (
                    self.current_fields
                    and len(self.current_fields) > 1
                ):

                    focused = self.focusWidget()

                    current_index = -1

                    for i, field in enumerate(
                        self.current_fields
                    ):

                        if field.line_edit is focused:

                            current_index = i

                            break

                    if current_index == -1:

                        return False

                    if key in (Qt.Key_Down, Qt.Key_PageDown):

                        next_index = (
                            current_index + 1
                        ) % len(
                            self.current_fields
                        )

                    else:

                        next_index = (
                            current_index - 1
                        ) % len(
                            self.current_fields
                        )

                    self.current_fields[
                        next_index
                    ].setFocus()

                    return True

        return super().eventFilter(
            obj, event
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
            20,
            30,
            20
        )

        main_layout.setSpacing(
            15
        )

        # ==================================================
        # MAIN CARD
        # ==================================================

        main_card = GlassCard()

        main_card.setFixedWidth(
            920
        )

        main_card.setFixedHeight(
            520
        )

        main_card.layout.setContentsMargins(
            35,
            30,
            35,
            30
        )

        main_card.layout.setSpacing(
            0
        )

        # ==================================================
        # MAIN CARD SHADOW
        # ==================================================

        shadow = QGraphicsDropShadowEffect(
            main_card
        )

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
                55
            )
        )

        main_card.setGraphicsEffect(
            shadow
        )

        # ==================================================
        # CONTENT LAYOUT
        # ==================================================

        content_layout = QHBoxLayout()

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        content_layout.setSpacing(
            45
        )

        # ==================================================
        # PREVIEW SIDE
        # ==================================================

        preview_container = QWidget()

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
            10,
            0,
            10,
            0
        )

        preview_layout.setSpacing(
            4
        )

        self.register_success_label = QLabel("")
        self.register_success_label.setAlignment(Qt.AlignCenter)
        self.register_success_label.setStyleSheet(
            "QLabel { color: #16A34A; background: transparent; border: none; "
            "font-size: 11px; font-weight: bold; padding: 0px; }"
        )
        self.register_success_label.hide()
        preview_layout.addWidget(
            self.register_success_label,
            alignment=Qt.AlignCenter
        )

        # ==================================================
        # PREVIEW
        # ==================================================

        self.preview = ImagePreview()

        preview_layout.addStretch()

        preview_layout.addWidget(
            self.preview,
            alignment=Qt.AlignCenter
        )

        preview_layout.addStretch()

        content_layout.addWidget(
            preview_container,
            1
        )

        # ==================================================
        # VERTICAL SEPARATOR
        # ==================================================

        separator = QWidget()

        separator.setFixedWidth(
            1
        )

        separator.setStyleSheet(
            """
            QWidget {
                background: #D9E3EE;
                border: none;
            }
            """
        )

        content_layout.addWidget(
            separator
        )

        # ==================================================
        # FORM SIDE
        # ==================================================

        form_container = QWidget()

        form_container.setStyleSheet(
            """
            QWidget {
                background: transparent;
                border: none;
            }
            """
        )

        form_layout = QVBoxLayout(
            form_container
        )

        form_layout.setContentsMargins(
            15,
            0,
            10,
            0
        )

        form_layout.setSpacing(
            12
        )

        # ==================================================
        # TITLE
        # ==================================================

        form_title = QLabel(
            "اطلاعات کاربر"
        )

        form_title.setFont(
            Fonts.heading()
        )

        form_title.setAlignment(
            Qt.AlignCenter
        )

        form_title.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.TEXT};
                background: transparent;
                border: none;
                font-weight: bold;
            }}
            """
        )

        form_layout.addWidget(
            form_title
        )

        form_layout.addSpacing(
            30
        )

        # ==================================================
        # GENERAL ERROR LABEL
        # ==================================================

        self.general_error = QLabel()

        self.general_error.setAlignment(
            Qt.AlignCenter
        )

        self.general_error.setFont(
            Fonts.text()
        )

        self.general_error.setStyleSheet(
            """
            QLabel
            {
                color: #DC2626;
                background: transparent;
                border: none;
                font-size: 10px;
                padding: 2px 4px 0px 4px;
                margin: 0px;
            }
            """
        )

        self.general_error.hide()

        form_layout.addWidget(
            self.general_error
        )

        # ==================================================
        # FIRST NAME
        # ==================================================

        self.first_name = RoundedLineEdit(
            placeholder="نام"
        )

        self.first_name.setFixedWidth(
            280
        )

        form_layout.addWidget(
            self.first_name,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # FIRST NAME ERROR
        # ==================================================

        self.first_name_error = QLabel()

        self.first_name_error.setAlignment(
            Qt.AlignRight
        )

        self.first_name_error.setFont(
            Fonts.text()
        )

        self.first_name_error.setStyleSheet(
            """
            QLabel
            {
                color: #DC2626;
                background: transparent;
                border: none;
                font-size: 10px;
                padding: 2px 4px 0px 4px;
                margin: 0px;
            }
            """
        )

        self.first_name_error.hide()

        form_layout.addWidget(
            self.first_name_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # LAST NAME
        # ==================================================

        self.last_name = RoundedLineEdit(
            placeholder="نام خانوادگی"
        )

        self.last_name.setFixedWidth(
            280
        )

        form_layout.addWidget(
            self.last_name,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # LAST NAME ERROR
        # ==================================================

        self.last_name_error = QLabel()

        self.last_name_error.setAlignment(
            Qt.AlignRight
        )

        self.last_name_error.setFont(
            Fonts.text()
        )

        self.last_name_error.setStyleSheet(
            """
            QLabel
            {
                color: #DC2626;
                background: transparent;
                border: none;
                font-size: 10px;
                padding: 2px 4px 0px 4px;
                margin: 0px;
            }
            """
        )

        self.last_name_error.hide()

        form_layout.addWidget(
            self.last_name_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # NATIONAL CODE
        # ==================================================

        self.national_code = RoundedLineEdit(
            placeholder="کد ملی"
        )

        self.national_code.setFixedWidth(
            280
        )
        self.national_code.line_edit.setMaxLength(10)
        self.national_code.line_edit.setValidator(
            QRegularExpressionValidator(
                QRegularExpression(r"[0-9]{0,10}"),
                self.national_code.line_edit
            )
        )

        form_layout.addWidget(
            self.national_code,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # NATIONAL CODE ERROR
        # ==================================================

        self.national_code_error = QLabel()

        self.national_code_error.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        self.national_code_error.setFixedWidth(
            280
        )

        self.national_code_error.setFont(
            Fonts.text()
        )

        self.national_code_error.setStyleSheet(
            """
            QLabel
            {
                color: #DC2626;
                background: transparent;
                border: none;
                font-size: 10px;
                padding: 2px 4px 0px 4px;
                margin: 0px;
            }
            """
        )

        self.national_code_error.hide()

        form_layout.addWidget(
            self.national_code_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # SPACE BEFORE BUTTONS
        # ==================================================

        form_layout.addSpacing(
            30
        )

        # ==================================================
        # SELECT IMAGE BUTTON
        # ==================================================

        self.select_image = SecondaryButton(
            "انتخاب تصویر"
        )

        self.select_image.setFixedWidth(
            230
        )

        self.select_image.setFixedHeight(
            38
        )

        self.select_image.setCursor(
            Qt.PointingHandCursor
        )

        form_layout.addWidget(
            self.select_image,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # SPACE BETWEEN BUTTONS
        # ==================================================

        form_layout.addSpacing(
            8
        )

        # ==================================================
        # REGISTER BUTTON
        # ==================================================

        self.register_button = PrimaryButton(
            "ثبت کاربر جدید"
        )

        self.register_button.setFixedWidth(
            230
        )

        self.register_button.setFixedHeight(
            38
        )

        self.register_button.setCursor(
            Qt.PointingHandCursor
        )

        form_layout.addWidget(
            self.register_button,
            alignment=Qt.AlignHCenter
        )

        form_layout.addStretch()

        # ==================================================
        # ADD FORM TO CONTENT
        # ==================================================

        content_layout.addWidget(
            form_container,
            1
        )

        # ==================================================
        # ADD CONTENT TO MAIN CARD
        # ==================================================

        main_card.layout.addLayout(
            content_layout
        )

        # ==================================================
        # CENTER MAIN CARD
        # ==================================================

        main_layout.addStretch()

        main_layout.addWidget(
            main_card,
            alignment=Qt.AlignCenter
        )

        main_layout.addStretch()

    # ==================================================
    # Select Image
    # ==================================================

    def select_image_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "انتخاب تصویر",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_path:
            return

        self.image_path = Path(
            file_path
        )

        # ==================================================
        # Show Image
        # ==================================================

        self.preview.set_image(
            str(self.image_path)
        )

        # ==================================================
        # Face Detection
        # ==================================================

        try:

            face_info = (
                self.face_recognizer
                .get_face_info(
                    str(self.image_path)
                )
            )

        except Exception as error:

            print(
                "Face detection error:",
                error
            )

            self.current_face_info = None

            self.show_field_error(
                self.general_error,
                "در پردازش تصویر مشکلی به وجود آمد.",
                self.national_code
            )

            return

        # ==================================================
        # No Face
        # ==================================================

        if face_info is None:

            self.current_face_info = None

            self.show_field_error(
                self.general_error,
                "چهره‌ای در تصویر پیدا نشد.",
                self.national_code
            )

            return

        # ==================================================
        # Face Found
        # ==================================================

        self.current_face_info = face_info

        print(
            "Face detected"
        )

        print(
            "Bounding Box:",
            face_info["bbox"]
        )

    # ==================================================
    # Show Field Error
    # ==================================================

    def show_field_error(
        self,
        label,
        text,
        widget
    ):

        label.setText(
            text
        )

        label.show()

        widget.setFocus()

    # ==================================================
    # Hide Field Error
    # ==================================================

    def hide_field_error(
        self,
        label
    ):

        label.clear()

        label.hide()

    # ==================================================
    # Register User
    # ==================================================

    def register_user(self):

        # ------------------------------------------------
        # Clear Previous Errors
        # ------------------------------------------------

        self.hide_field_error(
            self.first_name_error
        )

        self.hide_field_error(
            self.last_name_error
        )

        self.hide_field_error(
            self.national_code_error
        )

        first_name = (
            self.first_name
            .text()
            .strip()
        )

        last_name = (
            self.last_name
            .text()
            .strip()
        )

        national_code = (
            self.national_code
            .text()
            .strip()
        )

        # ==================================================
        # Validation
        # ==================================================

        if not first_name:

            self.show_field_error(
                self.first_name_error,
                "نام را وارد کنید.",
                self.first_name
            )

            return

        if not last_name:

            self.show_field_error(
                self.last_name_error,
                "نام خانوادگی را وارد کنید.",
                self.last_name
            )

            return

        if not national_code:

            self.show_field_error(
                self.national_code_error,
                "کد ملی را وارد کنید.",
                self.national_code
            )

            return

        if not national_code.isdigit():

            self.show_field_error(
                self.national_code_error,
                "کد ملی باید فقط شامل عدد باشد.",
                self.national_code
            )

            return

        if len(national_code) != 10:

            self.show_field_error(
                self.national_code_error,
                "کد ملی باید ۱۰ رقم باشد.",
                self.national_code
            )

            return

        if self.image_path is None:

            self.show_field_error(
                self.general_error,
                "ابتدا یک تصویر انتخاب کنید.",
                self.national_code
            )

            return

        # ==================================================
        # Face Detection
        # ==================================================

        face_info = self.current_face_info

        if face_info is None:

            try:

                face_info = (
                    self.face_recognizer
                    .get_face_info(
                        str(self.image_path)
                    )
                )

            except Exception as error:

                print(
                    "Face recognition error:",
                    error
                )

                self.show_field_error(
                    self.general_error,
                    "در پردازش تصویر مشکلی به وجود آمد.",
                    self.national_code
                )

                return

        # ==================================================
        # No Face
        # ==================================================

        if face_info is None:

            self.show_field_error(
                self.general_error,
                "چهره‌ای در تصویر پیدا نشد.",
                self.national_code
            )

            return

        # ==================================================
        # Encoding
        # ==================================================

        encoding = face_info.get(
            "encoding"
        )

        if encoding is None:

            self.show_field_error(
                self.general_error,
                "ویژگی‌های چهره استخراج نشد.",
                self.national_code
            )

            return

        # ==================================================
        # Duplicate National Code
        # ==================================================

        existing_user = (
            self.repository
            .get_user_by_national_code(
                national_code
            )
        )

        if existing_user:

            self.show_field_error(
                self.national_code_error,
                "این کد ملی قبلاً ثبت شده است.",
                self.national_code
            )

            return

        # ==================================================
        # Serialize Encoding
        # ==================================================

        try:

            face_data = pickle.dumps(
                encoding
            )

        except Exception as error:

            print(
                "Encoding serialization error:",
                error
            )

            self.show_field_error(
                self.general_error,
                "ذخیره اطلاعات چهره با مشکل مواجه شد.",
                self.national_code
            )

            return

        # ==================================================
        # Save User
        # ==================================================

        try:

            self.repository.create_user(
                first_name,
                last_name,
                national_code,
                face_data
            )

        except Exception as error:

            print(
                "Database error:",
                error
            )

            self.show_field_error(
                self.general_error,
                "ذخیره کاربر در دیتابیس انجام نشد.",
                self.national_code
            )

            return

        # ==================================================
        # Success
        # ==================================================

        self.general_error.setStyleSheet(
            """
            QLabel
            {
                color: #16A34A;
                background: transparent;
                border: none;
                font-size: 11px;
                padding: 2px 4px 0px 4px;
                margin: 0px;
            }
            """
        )

        # ==================================================
        # Success Feedback
        # ==================================================

        self.general_error.hide()
        self.register_success_label.setText("✓ ثبت کاربر با موفقیت انجام شد")
        self.register_success_label.show()
        self._success_timer.start(2000)

    def _finish_registration_success(self):

        self.register_success_label.hide()
        self.clear_form(hide_message=True)

        # Keep the form visually fresh for the next registration.
        self.first_name.setFocus()

    # ==================================================
    # Clear Form
    # ==================================================

    def clear_form(self, hide_message=True):

        if hide_message:
            self.general_error.hide()

        self.register_success_label.hide()

        self.first_name.clear()

        self.last_name.clear()

        self.national_code.clear()

        self.image_path = None

        self.current_face_info = None

        self.preview.clear()

    # ==================================================
    # Back
    # ==================================================

    def go_back(self):

        if self.parent():

            self.parent().setCurrentIndex(
                0
            )