import re
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import (
    QPixmap,
    QColor,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from gui.components.glass_card import GlassCard
from gui.components.rounded_input import RoundedLineEdit
from gui.components.primary_button import PrimaryButton
from gui.components.secondary_button import SecondaryButton
from gui.components.window_toolbar import WindowToolbar
from gui.components.username_suggestion import UsernameSuggestionDropdown
from gui.components.field_keyboard_navigation import FieldKeyboardNavigation

from controllers.auth_controller import AuthController

from theme.fonts import Fonts


class LoginPage(QWidget):

    # ==================================================
    # Signals
    # ==================================================

    # username + role + user_id
    #
    # role:
    #   admin -> مدیر
    #   user  -> کاربر عادی
    #
    login_success = Signal(str, str, object)

    # ==================================================
    # Init
    # ==================================================

    def __init__(self, parent=None):

        super().__init__(parent)

        self.repository = AuthController()

        # ------------------------------------------------
        # Success Message
        # ------------------------------------------------

        self.success_message = ""

        # ------------------------------------------------
        # Username Frequency for Suggestions
        # ------------------------------------------------

        self.username_freq = {}

        # ------------------------------------------------
        # Registration Info
        # ------------------------------------------------

        self.last_registered_first_name = ""
        self.last_registered_last_name = ""

        # ------------------------------------------------
        # Keyboard Navigation State
        # ------------------------------------------------

        self.keyboard_navigation = None

        # ------------------------------------------------
        # UI
        # ------------------------------------------------

        self.setup_window()
        self.setup_ui()

        # ------------------------------------------------
        # Focus
        # ------------------------------------------------

        self.setFocusPolicy(
            Qt.StrongFocus
        )

        self.setFocus()

    # ==================================================
    # Window
    # ==================================================

    def setup_window(self):

        self.setWindowTitle(
            "ورود به سیستم"
        )

        self.resize(
            1500,
            800
        )

        self.setMinimumSize(
            1000,
            650
        )

        # ------------------------------------------------
        # Remove Windows Default Title Bar
        # ------------------------------------------------

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window
        )

        self.setStyleSheet(
            """
            LoginPage
            {
                background: #F3F8FD;
            }
            """
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.main_layout = QVBoxLayout(
            self
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.main_layout.setSpacing(
            0
        )

        # ==================================================
        # Custom Window Toolbar
        # ==================================================

        self.window_toolbar = WindowToolbar(
            self.window(),
            self
        )

        self.main_layout.addWidget(
            self.window_toolbar
        )

        # ==================================================
        # Content Area
        # ==================================================

        self.content_widget = QWidget(
            self
        )

        self.content_widget.setStyleSheet(
            """
            QWidget
            {
                background: transparent;
                border: none;
            }
            """
        )

        self.content_layout = QVBoxLayout(
            self.content_widget
        )

        self.content_layout.setContentsMargins(
            40,
            40,
            40,
            40
        )

        self.content_layout.setSpacing(
            0
        )

        self.main_layout.addWidget(
            self.content_widget,
            1
        )

        # ==================================================
        # Card
        # ==================================================

        self.card = GlassCard()

        self.card.setFixedWidth(
            520
        )

        self.card.setFixedHeight(
            470
        )

        # ==================================================
        # Card Style
        # ==================================================

        self.card.setStyleSheet(
            """
            QWidget
            {
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 1,

                    stop: 0 #FFFFFF,
                    stop: 0.20 #FCFEFF,
                    stop: 0.45 #F6FAFF,
                    stop: 0.70 #EDF6FF,
                    stop: 1 #E2F0FF
                );

                border: 1px solid #C9DFF3;
                border-radius: 30px;
            }
            """
        )

        # ==================================================
        # Card Shadow
        # ==================================================

        card_shadow = QGraphicsDropShadowEffect(
            self.card
        )

        card_shadow.setBlurRadius(
            45
        )

        card_shadow.setOffset(
            0,
            14
        )

        card_shadow.setColor(
            QColor(
                37,
                99,
                235,
                50
            )
        )

        self.card.setGraphicsEffect(
            card_shadow
        )

        # ==================================================
        # Add Card
        # ==================================================

        self.content_layout.addWidget(
            self.card,
            alignment=Qt.AlignCenter
        )

        # ==================================================
        # Start Login
        # ==================================================

        self.show_login_mode()

    # ==================================================
    # Logo
    # ==================================================

    def create_logo(self):

        logo = QLabel()

        logo.setAlignment(
            Qt.AlignCenter
        )

        logo.setFixedHeight(
            90
        )

        logo.setStyleSheet(
            """
            QLabel
            {
                background: transparent;
                border: none;
            }
            """
        )

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        logo_path = (
            project_root
            / "assets"
            / "logo1.png"
        )

        logo_pixmap = QPixmap(
            str(logo_path)
        )

        if not logo_pixmap.isNull():

            logo.setPixmap(
                logo_pixmap.scaled(
                    90,
                    90,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        else:

            print(
                "Logo not found:",
                logo_path
            )

        return logo

    # ==================================================
    # Error Label
    # ==================================================

    def create_error_label(self):

        label = QLabel()

        label.setAlignment(
            Qt.AlignRight
        )

        label.setFont(
            Fonts.text()
        )

        label.setStyleSheet(
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

        label.hide()

        return label

    # ==================================================
    # Show Error
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
    # Hide Error
    # ==================================================

    def hide_field_error(
        self,
        label
    ):

        label.clear()

        label.hide()

    # ==================================================
    # Central Keyboard Navigation
    # ==================================================

    def _setup_keyboard_navigation(self, submit_widget):
        """Use the shared keyboard-navigation service for the active form."""
        if self.keyboard_navigation is None:
            self.keyboard_navigation = FieldKeyboardNavigation(
                self,
                submit_widget=submit_widget,
                key_handler=self._handle_special_field_key,
            )
        else:
            self.keyboard_navigation.submit_widget = submit_widget
            self.keyboard_navigation.refresh()

    def _handle_special_field_key(self, watched, event):
        """Handle username suggestions without duplicating field navigation."""
        key = event.key()

        dropdown = getattr(self, "username_dropdown", None)
        if (
            dropdown is None
            or not dropdown.is_visible_and_has_items()
            or watched is not getattr(self.username, "line_edit", None)
        ):
            if key == Qt.Key_Escape and dropdown is not None and dropdown.is_visible_and_has_items():
                dropdown.hide()
                return True
            return False

        if key == Qt.Key_Down:
            if dropdown.navigate_down():
                return True
            self.password.setFocus()
            dropdown.hide()
            return True

        if key == Qt.Key_Up:
            dropdown.navigate_up()
            return True

        if key in (Qt.Key_Return, Qt.Key_Enter):
            return dropdown.select_current()

        if key == Qt.Key_Escape:
            dropdown.hide()
            return True

        return False

    # ==================================================
    # Login Mode
    # ==================================================

    def show_login_mode(
        self,
        username=""
    ):

        if not isinstance(
            username,
            str
        ):

            username = ""

        # ------------------------------------------------
        # Card Height
        # ------------------------------------------------

        self.card.setFixedHeight(
            470
        )

        # ------------------------------------------------
        # Clear Previous Widgets
        # ------------------------------------------------

        self.clear_card()

        # ==================================================
        # Logo
        # ==================================================

        self.logo = self.create_logo()

        self.card.layout.addWidget(
            self.logo,
            alignment=Qt.AlignCenter
        )

        self.card.layout.addSpacing(
            5
        )

        # ==================================================
        # Success Message
        # ==================================================

        if self.success_message:

            success_label = QLabel(
                self.success_message
            )

            success_label.setAlignment(
                Qt.AlignCenter
            )

            success_label.setFont(
                Fonts.text()
            )

            success_label.setStyleSheet(
                """
                QLabel
                {
                    color: #16A34A;
                    background: transparent;
                    border: none;
                    font-size: 11px;
                    font-weight: bold;
                    padding-top: 5px;
                    padding-bottom: 2px;
                }
                """
            )

            self.card.layout.addWidget(
                success_label
            )

            self.success_message = ""

        # ==================================================
        # Subtitle
        # ==================================================

        subtitle = QLabel(
            "ورود به پنل مدیریت"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setFont(
            Fonts.input()
        )

        subtitle.setStyleSheet(
            """
            QLabel
            {
                color: #4A90E2;
                background: transparent;
                border: none;
            }
            """
        )

        self.card.layout.addWidget(
            subtitle
        )

        self.card.layout.addSpacing(
            25
        )

        # ==================================================
        # Username
        # ==================================================

        self.username = RoundedLineEdit(
            "نام کاربری"
        )

        self.username.setFixedWidth(
            280
        )


        if username:

            self.username.setText(
                username
            )

        # Username Suggestion Dropdown

        if getattr(self, "username_dropdown", None) is None:

            self.username_dropdown = UsernameSuggestionDropdown()
            self.username_dropdown.setAttribute(
                Qt.WidgetAttribute.WA_DeleteOnClose,
                False
            )

            self.username_dropdown.suggestion_selected.connect(
                self._on_username_suggestion
            )

        # Show dropdown when username field gets focus or text changes

        self.username.line_edit.textChanged.connect(
            self._on_username_text_changed
        )

        self.username.line_edit.textChanged.emit(
            self.username.line_edit.text()
        )

        self.card.layout.addWidget(
            self.username,
            alignment=Qt.AlignHCenter
        )

        # Username error label

        self.username_login_error = (
            self.create_error_label()
        )

        self.username_login_error.setFixedWidth(
            280
        )

        self.card.layout.addWidget(
            self.username_login_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Password + Forgot Password Group
        # ==================================================

        password_group = QWidget()

        password_group.setStyleSheet(
            """
            QWidget
            {
                background: transparent;
                border: none;
            }
            """
        )

        password_group_layout = QVBoxLayout(
            password_group
        )

        password_group_layout.setContentsMargins(
            0, 0, 0, 0
        )

        password_group_layout.setSpacing(
            1
        )

        # --- Password Field ---

        self.password = RoundedLineEdit(
            "رمز عبور"
        )

        self.password.setFixedWidth(
            280
        )


        self.password.setEchoMode(
            QLineEdit.Password
        )

        password_group_layout.addWidget(
            self.password,
            alignment=Qt.AlignHCenter
        )

        # --- Forgot Password Link ---

        self.forgot_password = QLabel(
            '<a href="#">رمز عبورم را فراموش کردم؟</a>'
        )

        self.forgot_password.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        self.forgot_password.setFont(
            Fonts.text()
        )

        self.forgot_password.setCursor(
            Qt.PointingHandCursor
        )

        self.forgot_password.setStyleSheet(
            """
            QLabel
            {
                color: #4A90E2;
                background: transparent;
                border: none;
                font-size: 10px;
                padding: 0px;
                margin: 0px;
            }

            QLabel a
            {
                color: #4A90E2;
                text-decoration: none;
            }

            QLabel a:hover
            {
                color: #357ABD;
            }
            """
        )

        self.forgot_password.linkActivated.connect(
            self.show_forgot_password_mode
        )

    
        self._restructure_password_eye_layout(
            self.password,
            self.forgot_password
        )

        # Password error label: keep it inside the password group so it
        # always appears directly under the password field / forgot link.
        self.password_login_error = (
            self.create_error_label()
        )

        self.password_login_error.setFixedWidth(
            280
        )

        password_group_layout.addWidget(
            self.password_login_error,
            alignment=Qt.AlignRight
        )

        self.card.layout.addWidget(
            password_group,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Login Button
        # ==================================================

        self.login_button = PrimaryButton(
            "ورود"
        )

        self.login_button.setFixedWidth(
            280
        )

        self.login_button.clicked.connect(
            self.login
        )

        self.card.layout.addWidget(
            self.login_button,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Register Question
        # ==================================================

        register_row = QLabel(
            'حساب کاربری ندارید؟ '
            '<a href="#">ثبت‌نام کنید</a>'
        )

        register_row.setAlignment(
            Qt.AlignCenter
        )

        register_row.setFont(
            Fonts.text()
        )

        register_row.setStyleSheet(
            """
            QLabel
            {
                color: #64748B;
                background: transparent;
                border: none;
                font-size: 11px;
                padding-top: 6px;
            }

            QLabel a
            {
                color: #4A90E2;
                text-decoration: none;
                font-weight: bold;
            }

            QLabel a:hover
            {
                color: #357ABD;
            }
            """
        )

        register_row.setCursor(
            Qt.PointingHandCursor
        )

        register_row.linkActivated.connect(
            lambda link:
            self.show_register_mode()
        )

        self.card.layout.addWidget(
            register_row,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addStretch()

        self.setFocus()

        self._setup_keyboard_navigation(self.login_button)

    # ==================================================
    # Username Suggestion Helpers
    # ==================================================

    def _on_username_suggestion(self, name):

        self.username.setText(name)

        self.password.setFocus()

    def _on_username_text_changed(self, text):

        if hasattr(self, 'username_dropdown'):

            self.username_dropdown.show_suggestions(
                self.username_freq,
                text,
                self.username.line_edit
            )

    # ==================================================
    # Helper: restructure eye icon layout
    # ==================================================

    def _restructure_password_eye_layout(
        self,
        rounded_input,
        left_widget=None
    ):
        """Reposition the eye button to the far right of the
        password row, matching the login-page layout.

        If *left_widget* is given it is placed on the far left
        of the same row (e.g. a "forgot password" link).
        """
        password_layout = rounded_input.password_layout
        eye_button = rounded_input.eye_button

        password_layout.removeWidget(eye_button)
        password_layout.removeWidget(
            rounded_input.password_text
        )

        if left_widget is not None:
            password_layout.removeWidget(left_widget)

        while password_layout.count():
            item = password_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        password_layout.setDirection(
            QHBoxLayout.Direction.LeftToRight
        )

        if left_widget is not None:
            password_layout.addWidget(
                left_widget,
                0,
                Qt.AlignLeft | Qt.AlignVCenter
            )

        password_layout.addStretch(1)

        password_layout.addWidget(
            rounded_input.password_text,
            0,
            Qt.AlignRight | Qt.AlignVCenter
        )

        password_layout.addWidget(
            eye_button,
            0,
            Qt.AlignRight | Qt.AlignVCenter
        )

    # ==================================================
    # Login
    # ==================================================

    def login(self):

        # ------------------------------------------------
        # Clear previous inline errors
        # ------------------------------------------------

        self.hide_field_error(
            self.username_login_error
        )

        self.hide_field_error(
            self.password_login_error
        )

        username = (
            self.username
            .text()
            .strip()
        )

        password = (
            self.password
            .text()
            .strip()
        )

        # ==================================================
        # Validation
        # ==================================================

        if not username:

            self.show_field_error(
                self.username_login_error,
                "نام کاربری را وارد کنید.",
                self.username
            )

            return

        if not password:

            self.show_field_error(
                self.password_login_error,
                "رمز عبور را وارد کنید.",
                self.password
            )

            return

        # ==================================================
        # Check Account
        # ==================================================

        account = (
            self.repository
            .get_login_account(
                username,
                password
            )
        )

        # ==================================================
        # Wrong Login
        # ==================================================

        if account is None:

            self.show_field_error(
                self.password_login_error,
                "نام کاربری یا رمز عبور اشتباه است.",
                self.password
            )

            self.password.clear()

            return

        # ==================================================
        # Save username frequency for suggestions
        # ==================================================

        if username in self.username_freq:

            self.username_freq[username] += 1

        else:

            self.username_freq[username] = 1

        # ==================================================
        # Get Role
        # ==================================================

        try:

            role = account["role"]

        except (TypeError, KeyError):

            role = "user"

        if role not in (
            "admin",
            "user"
        ):

            role = "user"

        # ==================================================
        # Successful Login
        # ==================================================

        user_id = account["user_id"]

        self.login_success.emit(
            username,
            role,
            user_id
        )

    # ==================================================
    # Forgot Password Mode
    # ==================================================

    def show_forgot_password_mode(self):

        self.card.setFixedHeight(
            570
        )

        self.clear_card()

        # ==================================================
        # Logo
        # ==================================================

        self.logo = self.create_logo()

        self.card.layout.addWidget(
            self.logo,
            alignment=Qt.AlignCenter
        )

        self.card.layout.addSpacing(
            20
        )

        # ==================================================
        # Title
        # ==================================================

        title = QLabel(
            "بازیابی رمز عبور"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            Fonts.input()
        )

        title.setStyleSheet(
            """
            QLabel
            {
                color: #4A90E2;
                background: transparent;
                border: none;
                padding: 0px;
            }
            """
        )

        self.card.layout.addWidget(
            title,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addSpacing(
            25
        )

        # ==================================================
        # Forgot Password Error Label
        # ==================================================

        self.forgot_error = self.create_error_label()

        self.forgot_error.setFixedWidth(
            280
        )

        self.card.layout.addWidget(
            self.forgot_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Username
        # ==================================================

        self.reset_username = RoundedLineEdit(
            "نام کاربری"
        )

        self.reset_username.setFixedWidth(
            280
        )


        self.card.layout.addWidget(
            self.reset_username,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addSpacing(
            8
        )

        # ==================================================
        # New Password
        # ==================================================

        self.reset_password = RoundedLineEdit(
            "رمز عبور جدید"
        )

        self.reset_password.setFixedWidth(
            280
        )


        self.reset_password.setEchoMode(
            QLineEdit.Password
        )

        self.card.layout.addWidget(
            self.reset_password,
            alignment=Qt.AlignHCenter
        )

        self._restructure_password_eye_layout(
            self.reset_password
        )

        self.card.layout.addSpacing(
            8
        )

        # ==================================================
        # Confirm Password
        # ==================================================

        self.reset_confirm_password = RoundedLineEdit(
            "تکرار رمز عبور جدید"
        )

        self.reset_confirm_password.setFixedWidth(
            280
        )


        self.reset_confirm_password.setEchoMode(
            QLineEdit.Password
        )

        self.card.layout.addWidget(
            self.reset_confirm_password,
            alignment=Qt.AlignHCenter
        )

        self._restructure_password_eye_layout(
            self.reset_confirm_password
        )
        self.card.layout.addSpacing(
            22
        )

        # ==================================================
        # Change Password Button
        # ==================================================

        change_button = PrimaryButton(
            "تغییر رمز عبور"
        )

        change_button.setFixedWidth(
            220
        )

        change_button.setFixedHeight(
            40
        )

        change_button.clicked.connect(
            self.change_password
        )

        self.card.layout.addWidget(
            change_button,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addSpacing(
            8
        )

        # ==================================================
        # Back To Login Button
        # ==================================================

        back_button = SecondaryButton(
            "بازگشت به ورود"
        )

        back_button.setFixedWidth(
            220
        )

        back_button.setFixedHeight(
            40
        )

        back_button.clicked.connect(
            lambda:
            self.show_login_mode("")
        )

        self.card.layout.addWidget(
            back_button,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addStretch()

        self._setup_keyboard_navigation(change_button)

        self.setFocus()

    # ==================================================
    # Change Password
    # ==================================================

    def change_password(self):

        username_value = (
            self.reset_username
            .text()
            .strip()
        )

        password_value = (
            self.reset_password
            .text()
            .strip()
        )

        confirm_value = (
            self.reset_confirm_password
            .text()
            .strip()
        )

        # ----------------------------------------------
        # Username
        # ----------------------------------------------

        self.hide_field_error(
            self.forgot_error
        )

        if not username_value:

            self.show_field_error(
                self.forgot_error,
                "نام کاربری را وارد کنید.",
                self.reset_username
            )

            return

        # ----------------------------------------------
        # Password
        # ----------------------------------------------

        if not password_value:

            self.show_field_error(
                self.forgot_error,
                "رمز عبور جدید را وارد کنید.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Password Length
        # ----------------------------------------------

        if len(password_value) < 8:

            self.show_field_error(
                self.forgot_error,
                "رمز عبور باید حداقل ۸ کاراکتر باشد.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Uppercase
        # ----------------------------------------------

        if not re.search(
            r"[A-Z]",
            password_value
        ):

            self.show_field_error(
                self.forgot_error,
                "رمز عبور باید حداقل یک حرف بزرگ داشته باشد.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Lowercase
        # ----------------------------------------------

        if not re.search(
            r"[a-z]",
            password_value
        ):

            self.show_field_error(
                self.forgot_error,
                "رمز عبور باید حداقل یک حرف کوچک داشته باشد.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Number
        # ----------------------------------------------

        if not re.search(
            r"\d",
            password_value
        ):

            self.show_field_error(
                self.forgot_error,
                "رمز عبور باید حداقل یک عدد داشته باشد.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Special Character
        # ----------------------------------------------

        if not re.search(
            r"[^\w\s]",
            password_value
        ):

            self.show_field_error(
                self.forgot_error,
                "رمز عبور باید حداقل یک کاراکتر ویژه داشته باشد.",
                self.reset_password
            )

            return

        # ----------------------------------------------
        # Confirm Password
        # ----------------------------------------------

        if not confirm_value:

            self.show_field_error(
                self.forgot_error,
                "تکرار رمز عبور را وارد کنید.",
                self.reset_confirm_password
            )

            return

        # ----------------------------------------------
        # Password Match
        # ----------------------------------------------

        if password_value != confirm_value:

            self.show_field_error(
                self.forgot_error,
                "تکرار رمز عبور یکسان نیست.",
                self.reset_confirm_password
            )

            self.reset_confirm_password.clear()

            return

        # ----------------------------------------------
        # Username Exists
        # ----------------------------------------------

        if not self.repository.login_username_exists(
            username_value
        ):

            self.show_field_error(
                self.forgot_error,
                "این نام کاربری وجود ندارد.",
                self.reset_username
            )

            return

        # ----------------------------------------------
        # Update Password
        # ----------------------------------------------

        success = (
            self.repository
            .update_login_password(
                username_value,
                password_value
            )
        )

        if not success:

            self.show_field_error(
                self.forgot_error,
                "تغییر رمز عبور انجام نشد.",
                self.reset_username
            )

            return

        # ----------------------------------------------
        # Success
        # ----------------------------------------------

        self.success_message = (
            "رمز عبور با موفقیت تغییر کرد ✓"
        )

        self.show_login_mode(
            username_value
        )

    # ==================================================
    # Register Mode
    # ==================================================

    def show_register_mode(self):

        self.card.setFixedHeight(
            620
        )

        self.clear_card()

        # ==================================================
        # Logo
        # ==================================================

        self.logo = self.create_logo()

        self.card.layout.addWidget(
            self.logo,
            alignment=Qt.AlignHCenter
        )

        self.card.layout.addSpacing(
            0
        )

        # ==================================================
        # Register Container
        # ==================================================

        register_container = QWidget()

        register_container.setStyleSheet(
            """
            QWidget
            {
                background: transparent;
                border: none;
            }
            """
        )

        register_layout = QVBoxLayout(
            register_container
        )

        register_layout.setContentsMargins(
            0,
            10,
            0,
            10
        )

        register_layout.setSpacing(
            6
        )

        register_layout.addStretch()

        # ==================================================
        # Title
        # ==================================================

        title = QLabel(
            "ایجاد حساب جدید"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            Fonts.input()
        )

        title.setStyleSheet(
            """
            QLabel
            {
                color: #4A90E2;
                background: transparent;
                border: none;
            }
            """
        )

        register_layout.addWidget(
            title,
            alignment=Qt.AlignHCenter
        )

        register_layout.addSpacing(
            30
        )

        # ==================================================
        # First Name
        # ==================================================

        self.register_first_name = RoundedLineEdit(
            "نام"
        )

        self.register_first_name.setFixedWidth(
            280
        )


        register_layout.addWidget(
            self.register_first_name,
            alignment=Qt.AlignHCenter
        )

        self.first_name_error = (
            self.create_error_label()
        )

        self.first_name_error.setFixedWidth(
            280
        )

        register_layout.addWidget(
            self.first_name_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Last Name
        # ==================================================

        self.register_last_name = RoundedLineEdit(
            "نام خانوادگی"
        )

        self.register_last_name.setFixedWidth(
            280
        )


        register_layout.addWidget(
            self.register_last_name,
            alignment=Qt.AlignHCenter
        )

        self.last_name_error = (
            self.create_error_label()
        )

        self.last_name_error.setFixedWidth(
            280
        )

        register_layout.addWidget(
            self.last_name_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Username
        # ==================================================

        self.register_username = RoundedLineEdit(
            "نام کاربری"
        )

        self.register_username.setFixedWidth(
            280
        )


        register_layout.addWidget(
            self.register_username,
            alignment=Qt.AlignHCenter
        )

        self.username_error = (
            self.create_error_label()
        )

        self.username_error.setFixedWidth(
            280
        )

        register_layout.addWidget(
            self.username_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Password
        # ==================================================

        self.register_password = RoundedLineEdit(
            "رمز عبور"
        )

        self.register_password.setFixedWidth(
            280
        )


        self.register_password.setEchoMode(
            QLineEdit.Password
        )

        register_layout.addWidget(
            self.register_password,
            alignment=Qt.AlignHCenter
        )

        self._restructure_password_eye_layout(
            self.register_password
        )

        self.password_error = (
            self.create_error_label()
        )

        self.password_error.setFixedWidth(
            280
        )

        register_layout.addWidget(
            self.password_error,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Confirm Password
        # ==================================================

        self.register_confirm_password = RoundedLineEdit(
            "تکرار رمز عبور"
        )

        self.register_confirm_password.setFixedWidth(
            280
        )


        self.register_confirm_password.setEchoMode(
            QLineEdit.Password
        )

        register_layout.addWidget(
            self.register_confirm_password,
            alignment=Qt.AlignHCenter
        )

        self._restructure_password_eye_layout(
            self.register_confirm_password
        )

        self.confirm_password_error = (
            self.create_error_label()
        )

        self.confirm_password_error.setFixedWidth(
            280
        )

        register_layout.addWidget(
            self.confirm_password_error,
            alignment=Qt.AlignHCenter
        )
        # ==================================================
        # Register Button
        # ==================================================

        register_layout.addSpacing(
            25
        )

        register_button = PrimaryButton(
            "ثبت‌نام"
        )

        register_button.setFixedWidth(
            220
        )

        register_button.setFixedHeight(
            40
        )

        register_button.clicked.connect(
            self.register_account
        )

        register_layout.addWidget(
            register_button,
            alignment=Qt.AlignHCenter
        )

        # ==================================================
        # Back Button
        # ==================================================

        back_button = SecondaryButton(
            "بازگشت به ورود"
        )

        back_button.setFixedWidth(
            220
        )

        back_button.setFixedHeight(
            40
        )

        back_button.clicked.connect(
            lambda:
            self.show_login_mode("")
        )

        register_layout.addWidget(
            back_button,
            alignment=Qt.AlignHCenter
        )

        register_layout.addStretch()

        self.card.layout.addWidget(
            register_container
        )

        self._setup_keyboard_navigation(register_button)

        self.setFocus()

    # ==================================================
    # Register Account
    # ==================================================

    def register_account(self):

        # ==================================================
        # Clear Previous Errors
        # ==================================================

        self.hide_field_error(
            self.first_name_error
        )

        self.hide_field_error(
            self.last_name_error
        )

        self.hide_field_error(
            self.username_error
        )

        self.hide_field_error(
            self.password_error
        )

        self.hide_field_error(
            self.confirm_password_error
        )

        # ==================================================
        # Get Values
        # ==================================================

        first_name = (
            self.register_first_name
            .text()
            .strip()
        )

        last_name = (
            self.register_last_name
            .text()
            .strip()
        )

        username = (
            self.register_username
            .text()
            .strip()
        )

        password = (
            self.register_password
            .text()
            .strip()
        )

        confirm_password = (
            self.register_confirm_password
            .text()
            .strip()
        )

        # ==================================================
        # First Name
        # ==================================================

        if not first_name:

            self.show_field_error(
                self.first_name_error,
                "نام را وارد کنید.",
                self.register_first_name
            )

            return

        # ==================================================
        # Last Name
        # ==================================================

        if not last_name:

            self.show_field_error(
                self.last_name_error,
                "نام خانوادگی را وارد کنید.",
                self.register_last_name
            )

            return

        # ==================================================
        # Username
        # ==================================================

        if not username:

            self.show_field_error(
                self.username_error,
                "نام کاربری را وارد کنید.",
                self.register_username
            )

            return

        # ==================================================
        # Duplicate Username
        # ==================================================

        if self.repository.login_username_exists(
            username
        ):

            self.show_field_error(
                self.username_error,
                "این نام کاربری قبلاً ثبت شده است.",
                self.register_username
            )

            return

        # ==================================================
        # Password Empty
        # ==================================================

        if not password:

            self.show_field_error(
                self.password_error,
                "رمز عبور را وارد کنید.",
                self.register_password
            )

            return

        # ==================================================
        # Password Length
        # ==================================================

        if len(password) < 8:

            self.show_field_error(
                self.password_error,
                "رمز عبور باید حداقل ۸ کاراکتر باشد.",
                self.register_password
            )

            return

        # ==================================================
        # Uppercase
        # ==================================================

        if not re.search(
            r"[A-Z]",
            password
        ):

            self.show_field_error(
                self.password_error,
                "رمز عبور باید حداقل یک حرف انگلیسی بزرگ داشته باشد.",
                self.register_password
            )

            return

        # ==================================================
        # Lowercase
        # ==================================================

        if not re.search(
            r"[a-z]",
            password
        ):

            self.show_field_error(
                self.password_error,
                "رمز عبور باید حداقل یک حرف انگلیسی کوچک داشته باشد.",
                self.register_password
            )

            return

        # ==================================================
        # Number
        # ==================================================

        if not re.search(
            r"\d",
            password
        ):

            self.show_field_error(
                self.password_error,
                "رمز عبور باید حداقل یک عدد داشته باشد.",
                self.register_password
            )

            return

        # ==================================================
        # Special Character
        # ==================================================

        if not re.search(
            r"[^\w\s]",
            password
        ):

            self.show_field_error(
                self.password_error,
                "رمز عبور باید حداقل یک کاراکتر ویژه داشته باشد.",
                self.register_password
            )

            return

        # ==================================================
        # Confirm Password Empty
        # ==================================================

        if not confirm_password:

            self.show_field_error(
                self.confirm_password_error,
                "تکرار رمز عبور را وارد کنید.",
                self.register_confirm_password
            )

            return

        # ==================================================
        # Confirm Password
        # ==================================================

        if password != confirm_password:

            self.show_field_error(
                self.confirm_password_error,
                "تکرار رمز عبور با رمز عبور یکسان نیست.",
                self.register_confirm_password
            )

            self.register_confirm_password.clear()

            return

        # ==================================================
        # Create Account
        # ==================================================

        success = (
            self.repository
            .create_login_account(
                username,
                password,
                role="user",
                first_name=first_name,
                last_name=last_name
            )
        )

        if not success:

            self.show_field_error(
                self.username_error,
                "ثبت حساب انجام نشد. نام کاربری دیگری انتخاب کنید.",
                self.register_username
            )

            return

        # ==================================================
        # Save Registration Info
        # ==================================================

        self.last_registered_first_name = (
            first_name
        )

        self.last_registered_last_name = (
            last_name
        )

        # ==================================================
        # Success Message
        # ==================================================

        self.success_message = (
            f"حساب کاربری «{first_name} {last_name}» "
            "با موفقیت ایجاد شد ✓"
        )

        # ==================================================
        # Show Login Again
        # ==================================================

        self.show_login_mode(
            username
        )

    # ==================================================
    # Clear Card
    # ==================================================

    def clear_card(self):
        dropdown = getattr(self, "username_dropdown", None)
        if dropdown is not None:
            try:
                dropdown.hide()
            except RuntimeError:
                self.username_dropdown = None


        focused = self.focusWidget()

        if focused is not None:

            focused.clearFocus()

        while self.card.layout.count():

            item = self.card.layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

    # ==================================================
    # Message
    # ==================================================

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
            QMessageBox
            {
                background: white;
            }

            QMessageBox QLabel
            {
                color: #475569;
                font-family: "IRANSans";
                font-size: 12px;
            }

            QMessageBox QPushButton
            {
                background: #4A90E2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 20px;
                min-width: 70px;
                font-family: "IRANSans";
            }

            QMessageBox QPushButton:hover
            {
                background: #357ABD;
            }
            """
        )

        msg.exec()

    # ==================================================
    # Mouse Press
    # ==================================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.setFocus()

        super().mousePressEvent(
            event
        )