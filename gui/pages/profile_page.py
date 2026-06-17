from pathlib import Path
import shutil

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFileDialog,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QFrame,
    QToolButton,
)

from PySide6.QtCore import Qt, Signal, QTimer, QSize
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QPainterPath,
    QIcon,
)

from gui.components.rounded_input import RoundedLineEdit
from gui.components.primary_button import PrimaryButton
from controllers.auth_controller import AuthController
from theme.fonts import Fonts
from theme.colors import Colors


class ProfilePage(QWidget):

    profile_updated = Signal(str, str, str)

    def __init__(
        self,
        user_id=None,
        username="",
        role="user",
        parent=None
    ):
        super().__init__(parent)

        # =====================================================
        # Compatibility with core/app.py
        # =====================================================

        self.current_submit = None

        # =====================================================
        # User Data
        # =====================================================

        self.user_id = user_id
        self.username = username
        self.role = role
        self.profile_image = ""

        # =====================================================
        # Repository
        # =====================================================

        self.repository = AuthController()

        # =====================================================
        # UI
        # =====================================================

        self.setup_ui()

        # =====================================================
        # Load Data
        # =====================================================

        self.load_profile()

    # =========================================================
    # UI
    # =========================================================

    def setup_ui(self):

        self.setStyleSheet(
            f"""
            ProfilePage {{
                background: {Colors.BACKGROUND};
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}
            """
        )

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(15)

        # =====================================================
        # Main Card
        # =====================================================

        self.card = QFrame()

        self.card.setObjectName(
            "ProfileCard"
        )

        self.card.setMaximumWidth(
            650
        )

        self.card.setStyleSheet(
            """
            QFrame#ProfileCard {
                background: #FFFFFF;
                border: 1px solid #D9E2EC;
                border-radius: 24px;
            }
            """
        )

        self.setFocusPolicy(
            Qt.ClickFocus
        )

        self.card.setFocusPolicy(
            Qt.ClickFocus
        )

        self.card.mousePressEvent = (
            self._clear_field_focus
        )

        # =====================================================
        # Shadow
        # =====================================================

        shadow = QGraphicsDropShadowEffect(
            self.card
        )

        shadow.setBlurRadius(
            32
        )

        shadow.setOffset(
            0,
            8
        )

        self.card.setGraphicsEffect(
            shadow
        )

        # =====================================================
        # Card Layout
        # =====================================================

        card_layout = QVBoxLayout(
            self.card
        )

        card_layout.setContentsMargins(
            40,
            32,
            40,
            34
        )

        card_layout.setSpacing(
            10
        )

        # =====================================================
        # Title
        # =====================================================

        title = QLabel(
            "پروفایل من"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            Fonts.title()
        )

        title.setStyleSheet(
            f"""
            color: {Colors.TEXT};
            font-size: 20px;
            font-weight: bold;
            """
        )

        card_layout.addWidget(
            title
        )

        # =====================================================
        # Subtitle
        # =====================================================

        subtitle = QLabel(
            "مدیریت اطلاعات حساب کاربری"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setFont(
            Fonts.small()
        )

        subtitle.setStyleSheet(
            f"""
            color: {Colors.MUTED};
            font-size: 10px;
            """
        )

        card_layout.addWidget(
            subtitle
        )

        card_layout.addSpacing(
            12
        )

        # =====================================================
        # Avatar Container
        # =====================================================

        self.avatar_wrap = QFrame()

        self.avatar_wrap.setFixedSize(
            190,
            166
        )

        self.avatar_wrap.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
            """
        )

        # =====================================================
        # Avatar
        # =====================================================

        self.avatar_label = QLabel(
            self.avatar_wrap
        )

        self.avatar_label.setGeometry(
            30,
            0,
            130,
            130
        )

        self.avatar_label.setAlignment(
            Qt.AlignCenter
        )

        self.avatar_label.setCursor(
            Qt.PointingHandCursor
        )

        self.avatar_label.mousePressEvent = (
            lambda event:
            self.select_profile_image()
        )

        # =====================================================
        # Edit Avatar Button
        # =====================================================

        self.edit_avatar_button = QToolButton(
            self.avatar_wrap
        )

        self.edit_avatar_button.setGeometry(
            118,
            100,
            46,
            46
        )

        self.edit_avatar_button.setCursor(
            Qt.PointingHandCursor
        )

        self.edit_avatar_button.setIcon(
            self.profile_pencil_icon()
        )

        self.edit_avatar_button.setIconSize(
            QSize(
                20,
                20
            )
        )

        self.edit_avatar_button.setStyleSheet(
            """
            QToolButton {
                background: #2F80ED;
                border: 3px solid white;
                border-radius: 23px;
                padding: 0px;
            }

            QToolButton:hover {
                background: #2563EB;
            }

            QToolButton:pressed {
                background: #1D4ED8;
            }
            """
        )

        self.edit_avatar_button.clicked.connect(
            self.select_profile_image
        )

        # =====================================================
        # Remove Avatar Button
        # =====================================================

        self.remove_avatar_button = QToolButton(
            self.avatar_wrap
        )

        self.remove_avatar_button.setGeometry(
            151,
            100,
            46,
            46
        )

        self.remove_avatar_button.setCursor(
            Qt.PointingHandCursor
        )

        self.remove_avatar_button.setText(
            "−"
        )

        self.remove_avatar_button.setStyleSheet(
            """
            QToolButton {
                background: #EF4444;
                color: white;
                border: 3px solid white;
                border-radius: 23px;
                padding: 0px 0px 3px 0px;
                font-size: 22px;
                font-weight: bold;
            }

            QToolButton:hover {
                background: #DC2626;
            }

            QToolButton:pressed {
                background: #B91C1C;
            }
            """
        )

        self.remove_avatar_button.clicked.connect(
            self.remove_profile_image
        )

        self.remove_avatar_button.hide()

        # =====================================================
        # Add Avatar
        # =====================================================

        card_layout.addWidget(
            self.avatar_wrap,
            alignment=Qt.AlignHCenter
        )

        # =====================================================
        # Edit Image Label
        # =====================================================

        self.edit_image_label = QLabel(
            "ویرایش تصویر"
        )

        self.edit_image_label.setAlignment(
            Qt.AlignCenter
        )

        self.edit_image_label.setCursor(
            Qt.PointingHandCursor
        )

        self.edit_image_label.setStyleSheet(
            """
            QLabel {
                color: #2F80ED;
                font-size: 11px;
                font-weight: bold;
                padding: 0px;
            }

            QLabel:hover {
                color: #2563EB;
            }
            """
        )

        self.edit_image_label.mousePressEvent = (
            lambda event:
            self.select_profile_image()
        )

        card_layout.addWidget(
            self.edit_image_label
        )

        card_layout.addSpacing(
            10
        )

        # =====================================================
        # Display Name
        # =====================================================

        self.display_name = QLabel(
            ""
        )

        self.display_name.setAlignment(
            Qt.AlignCenter
        )

        self.display_name.setFont(
            Fonts.heading()
        )

        self.display_name.setStyleSheet(
            f"""
            color: {Colors.TEXT};
            font-size: 15px;
            font-weight: bold;
            """
        )

        card_layout.addWidget(
            self.display_name
        )

        # =====================================================
        # Role
        # =====================================================

        self.role_label = QLabel(
            self.role_text()
        )

        self.role_label.setAlignment(
            Qt.AlignCenter
        )

        self.role_label.setStyleSheet(
            f"""
            QLabel {{
                color: {Colors.PRIMARY};
                background: #EEF6FF;
                border: 1px solid #D8EAFE;
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 9px;
                font-weight: bold;
            }}
            """
        )

        card_layout.addWidget(
            self.role_label,
            alignment=Qt.AlignHCenter
        )

        card_layout.addSpacing(
            16
        )

        # =====================================================
        # Section Header
        # =====================================================

        section_header = QHBoxLayout()

        section_title = QLabel(
            "اطلاعات حساب"
        )

        section_title.setFont(
            Fonts.button()
        )

        section_title.setStyleSheet(
            f"""
            color: {Colors.TEXT};
            font-size: 12px;
            font-weight: bold;
            """
        )

        section_header.addWidget(
            section_title
        )

        section_header.addStretch()

        info_line = QFrame()

        info_line.setFixedHeight(
            1
        )

        info_line.setStyleSheet(
            """
            background: #E5EDF5;
            border: none;
            """
        )

        section_header.addWidget(
            info_line,
            1
        )

        card_layout.addLayout(
            section_header
        )

        card_layout.addSpacing(
            6
        )

        # =====================================================
        # Information Grid
        # =====================================================

        info_grid = QGridLayout()

        info_grid.setContentsMargins(
            0,
            0,
            0,
            0
        )

        info_grid.setHorizontalSpacing(
            22
        )

        info_grid.setVerticalSpacing(
            18
        )

        # =====================================================
        # First Name
        # =====================================================

        (
            self.first_name_label,
            self.first_name
        ) = self._profile_field(
            "نام",
            editable=True
        )

        # =====================================================
        # Last Name
        # =====================================================

        (
            self.last_name_label,
            self.last_name
        ) = self._profile_field(
            "نام خانوادگی",
            editable=True
        )

        # =====================================================
        # Username
        # =====================================================

        (
            self.username_label,
            self.username_input
        ) = self._profile_field(
            "نام کاربری",
            editable=False
        )

        # =====================================================
        # National Code
        # =====================================================

        (
            self.national_code_label,
            self.national_code_input
        ) = self._profile_field(
            "کد ملی",
            editable=False
        )

        self.username_input.line_edit.setToolTip(
            "نام کاربری قابل تغییر نیست"
        )

        self.national_code_input.line_edit.setToolTip(
            "کد ملی ثبت‌شده قابل تغییر نیست"
        )

        # =====================================================
        # Field List
        # =====================================================

        fields = [
            (
                self.first_name_label,
                self.first_name
            ),
            (
                self.last_name_label,
                self.last_name
            ),
            (
                self.username_label,
                self.username_input
            ),
            (
                self.national_code_label,
                self.national_code_input
            ),
        ]

        # =====================================================
        # Add Fields
        # =====================================================

        for index, (label, field) in enumerate(
            fields
        ):

            cell = QWidget()

            cell.setStyleSheet(
                """
                QWidget {
                    background: transparent;
                    border: none;
                }
                """
            )

            cell_layout = QVBoxLayout(
                cell
            )

            cell_layout.setContentsMargins(
                0,
                0,
                0,
                0
            )

            cell_layout.setSpacing(
                6
            )

            cell_layout.addWidget(
                label
            )

            cell_layout.addWidget(
                field
            )

            row = index // 2
            column = index % 2

            info_grid.addWidget(
                cell,
                row,
                column
            )

        info_grid.setColumnStretch(
            0,
            1
        )

        info_grid.setColumnStretch(
            1,
            1
        )

        card_layout.addLayout(
            info_grid
        )

        card_layout.addSpacing(
            16
        )

        # =====================================================
        # Feedback
        # =====================================================

        self.feedback_label = QLabel(
            ""
        )

        self.feedback_label.setAlignment(
            Qt.AlignCenter
        )

        self.feedback_label.setFont(
            Fonts.small()
        )

        self.feedback_label.setStyleSheet(
            """
            color: #16A34A;
            font-size: 9px;
            font-weight: bold;
            """
        )

        self.feedback_label.hide()

        self._feedback_timer = QTimer(
            self
        )

        self._feedback_timer.setSingleShot(
            True
        )

        self._feedback_timer.timeout.connect(
            self.feedback_label.hide
        )

        card_layout.addWidget(
            self.feedback_label
        )

        # =====================================================
        # Save Button
        # =====================================================

        self.save_button = PrimaryButton(
            "✓  ذخیره تغییرات"
        )

        self.save_button.setFixedWidth(
            230
        )

        self.save_button.setFixedHeight(
            42
        )

        self.save_button.clicked.connect(
            self.save_profile
        )

        card_layout.addWidget(
            self.save_button,
            alignment=Qt.AlignHCenter
        )

        # =====================================================
        # Add Card To Page
        # =====================================================

        main_layout.addWidget(
            self.card,
            alignment=Qt.AlignCenter
        )

        # =====================================================
        # Submit Widget Compatibility
        # =====================================================

        self.current_submit = (
            self.save_button
        )

    # =========================================================
    # Profile Field
    # =========================================================

    def _profile_field(
        self,
        label_text,
        editable=True
    ):

        label = QLabel(
            label_text
        )

        label.setFixedWidth(
            265
        )

        # عنوان فیلد همیشه سمت چپ
        label.setAlignment(
            Qt.AlignLeft |
            Qt.AlignVCenter
        )

        label.setStyleSheet(
            """
            QLabel {
                color: #475569;
                background: transparent;
                border: none;
                font-size: 11px;
                font-weight: bold;
                padding: 0 2px;
            }
            """
        )

        field = RoundedLineEdit(
            label_text
        )

        field.setFixedWidth(
            265
        )

        field.line_edit.setReadOnly(
            not editable
        )

        # هیچ Alignment اینجا اعمال نمی‌شود.
        # SmartLineEdit خودش بر اساس متن
        # فارسی / انگلیسی جهت را تعیین می‌کند.

        return label, field

    # =========================================================
    # Clear Focus
    # =========================================================

    def _clear_field_focus(
        self,
        event
    ):

        try:

            self.clearFocus()

            self.card.clearFocus()

            self.first_name.line_edit.clearFocus()

            self.last_name.line_edit.clearFocus()

            self.username_input.line_edit.clearFocus()

            self.national_code_input.line_edit.clearFocus()

        except RuntimeError:
            pass

        event.accept()

    # =========================================================
    # Pencil Icon
    # =========================================================

    def profile_pencil_icon(self):

        icons_dir = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "icons"
        )

        icon_names = (
            "prncil.svg",
            "prncil.png",
            "prncil.jpg",
            "prncil.jpeg",
            "pencil.svg",
            "pencil.png",
            "pencil.jpg",
            "pencil.jpeg",
            "user-pen.svg",
            "user-pen.png",
        )

        for icon_name in icon_names:

            icon_path = (
                icons_dir /
                icon_name
            )

            if icon_path.exists():

                return QIcon(
                    str(icon_path)
                )

        return QIcon()

    # =========================================================
    # Role
    # =========================================================

    def role_text(self):

        roles = {
            "admin": "مدیر سیستم",
            "administrator": "مدیر سیستم",
            "user": "کاربر",
            "employee": "کارمند",
        }

        return roles.get(
            str(
                self.role
            ).lower(),
            str(
                self.role or "کاربر"
            )
        )

    # =========================================================
    # Load Profile
    # =========================================================

    def load_profile(self):

        account = self.repository.get_profile(
            self.user_id,
            self.username
        )

        if account is None:

            self.username_input.setText(
                self.username
            )

            self.update_identity()

            self.update_avatar()

            return True

        self.username = (
            account["username"]
            or self.username
        )

        self.user_id = (
            account["user_id"]
            or self.user_id
        )

        if hasattr(
            account,
            "get"
        ):

            self.role = account.get(
                "role",
                self.role
            )

        self.first_name.setText(
            account["first_name"] or ""
        )

        self.last_name.setText(
            account["last_name"] or ""
        )

        self.username_input.setText(
            self.username
        )

        self.national_code_input.setText(
            account["national_code"] or ""
        )

        self.profile_image = (
            account["profile_image"] or ""
        )

        self.role_label.setText(
            self.role_text()
        )

        self.update_identity()

        self.update_avatar()

        return True

    # =========================================================
    # Identity
    # =========================================================

    def update_identity(self):

        first = (
            self.first_name
            .text()
            .strip()
        )

        last = (
            self.last_name
            .text()
            .strip()
        )

        full_name = (
            f"{first} {last}"
            .strip()
        )

        self.display_name.setText(
            full_name
            or self.username
            or "کاربر"
        )

    # =========================================================
    # Select Image
    # =========================================================

    def select_profile_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "انتخاب تصویر پروفایل",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if not file_path:
            return

        project_root = (
            Path(__file__).resolve().parents[2]
        )

        profiles_dir = (
            project_root
            / "assets"
            / "profiles"
        )

        profiles_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        extension = (
            Path(file_path)
            .suffix
            .lower()
        )

        destination = (
            profiles_dir
            / f"profile_{self.user_id or self.username}{extension}"
        )

        try:

            shutil.copy2(
                file_path,
                destination
            )

            self.profile_image = str(
                destination
            )

            self.update_avatar()

            self.show_feedback(
                "تصویر پروفایل انتخاب شد؛ برای ثبت نهایی ذخیره کنید."
            )

        except Exception as error:

            self.show_message(
                "خطا",
                f"ذخیره تصویر انجام نشد.\n{error}"
            )

    # =========================================================
    # Remove Image
    # =========================================================

    def remove_profile_image(self):

        if not self.profile_image:

            self.show_feedback(
                "تصویر پروفایلی برای حذف وجود ندارد."
            )

            return

        try:

            image_path = Path(
                self.profile_image
            )

            if image_path.exists():

                image_path.unlink()

            self.profile_image = ""

            self.update_avatar()

            self.show_feedback(
                "تصویر حذف شد؛ برای ثبت نهایی ذخیره کنید."
            )

        except Exception as error:

            self.show_message(
                "خطا",
                f"حذف تصویر انجام نشد.\n{error}"
            )

    # =========================================================
    # Update Avatar
    # =========================================================

    def update_avatar(self):

        if (
            self.profile_image
            and Path(
                self.profile_image
            ).exists()
        ):

            pixmap = QPixmap(
                self.profile_image
            )

            if not pixmap.isNull():

                self.avatar_label.setPixmap(
                    self.circular_pixmap(
                        pixmap,
                        124
                    )
                )

                self.avatar_label.setStyleSheet(
                    """
                    QLabel {
                        background: #FFFFFF;
                        border: 3px solid #D6E8F8;
                        border-radius: 65px;
                    }
                    """
                )

                self.remove_avatar_button.show()

                return

        self.avatar_label.clear()

        self.avatar_label.setText(
            self.get_initial()
        )

        self.avatar_label.setFont(
            Fonts.title()
        )

        self.avatar_label.setStyleSheet(
            """
            QLabel {
                background: #6FA8E6;
                color: white;
                border: 3px solid #D6E8F8;
                border-radius: 65px;
                font-size: 32px;
                font-weight: bold;
            }
            """
        )

        self.remove_avatar_button.hide()

    # =========================================================
    # Circular Pixmap
    # =========================================================

    def circular_pixmap(
        self,
        pixmap,
        size
    ):

        scaled = pixmap.scaled(
            size,
            size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        output = QPixmap(
            size,
            size
        )

        output.fill(
            Qt.transparent
        )

        painter = QPainter(
            output
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        path = QPainterPath()

        path.addEllipse(
            0,
            0,
            size,
            size
        )

        painter.setClipPath(
            path
        )

        painter.drawPixmap(
            0,
            0,
            scaled
        )

        painter.end()

        return output

    # =========================================================
    # Initial
    # =========================================================

    def get_initial(self):

        name = (
            self.first_name
            .text()
            .strip()
        )

        if name:
            return name[0].upper()

        if self.username:
            return self.username[0].upper()

        return "?"

    # =========================================================
    # Save Profile
    # =========================================================

    def save_profile(self):

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

        success = (
            self.repository.update_profile(
                self.user_id,
                self.username,
                first_name,
                last_name,
                self.profile_image
            )
        )

        if not success:

            self.show_message(
                "خطا",
                "ذخیره اطلاعات پروفایل انجام نشد."
            )

            return

        self.update_identity()

        self.update_avatar()

        self.profile_updated.emit(
            first_name,
            last_name,
            self.profile_image
        )

        self.show_feedback(
            "تغییرات با موفقیت ذخیره شد."
        )

    # =========================================================
    # Feedback
    # =========================================================

    def show_feedback(
        self,
        text
    ):

        if self._feedback_timer.isActive():

            self._feedback_timer.stop()

        self.feedback_label.setText(
            text
        )

        self.feedback_label.show()

        self._feedback_timer.start(
            2000
        )

    # =========================================================
    # Message
    # =========================================================

    def show_message(
        self,
        title,
        text
    ):

        msg = QMessageBox(
            self
        )

        msg.setWindowTitle(
            title
        )

        msg.setText(
            text
        )

        msg.setStyleSheet(
            """
            QMessageBox {
                background: white;
            }

            QMessageBox QLabel {
                color: #475569;
                font-size: 12px;
            }

            QMessageBox QPushButton {
                background: #2F80ED;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 20px;
                min-width: 70px;
            }

            QMessageBox QPushButton:hover {
                background: #2563EB;
            }
            """
        )

        msg.exec()