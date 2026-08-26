from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QToolButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QSize
)

from PySide6.QtGui import QIcon

from theme.colors import Colors
from theme.fonts import Fonts
from gui.components.smart_line_edit import SmartLineEdit


class RoundedLineEdit(QWidget):

    # ==================================================
    # Signals
    # ==================================================

    password_visibility_changed = Signal(bool)

    # ==================================================
    # Init
    # ==================================================

    def __init__(
        self,
        placeholder="",
        parent=None
    ):

        super().__init__(parent)

        self.placeholder = placeholder

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.main_layout.setSpacing(2)

        # ==================================================
        # Real Line Edit
        # ==================================================

        self.line_edit = SmartLineEdit()

        self.line_edit.setPlaceholderText(
            self.placeholder
        )

        self.line_edit.setMinimumHeight(
            42
        )

        self.line_edit.setFont(
            Fonts.input()
        )

        self.line_edit.setCursor(
            Qt.IBeamCursor
        )

        self.line_edit.setStyleSheet(
            f"""
            QLineEdit
            {{
                background: transparent;

                color: #111827;

                border: none;

                border-bottom:
                    1px solid #CBD5E1;

                border-radius: 0px;

                padding:
                    8px
                    4px
                    8px
                    4px;

            }}

            QLineEdit:hover
            {{
                border-bottom:
                    1px solid #94A3B8;
            }}

            QLineEdit:focus
            {{
                border: none;

                border-bottom:
                    2px solid {Colors.PRIMARY};

                border-radius: 0px;

                padding:
                    8px
                    4px
                    7px
                    4px;

            }}
            """
        )

        self.main_layout.addWidget(
            self.line_edit
        )
        # ==================================================
        # Password Toggle Row
        # ==================================================

        self.password_row = QWidget()

        self.password_row.setFixedHeight(24)

        self.password_row.setStyleSheet(
            """
            QWidget
            {
                background: transparent;
                border: none;
            }
            """
        )

        self.password_layout = QHBoxLayout(
            self.password_row
        )

        self.password_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.password_layout.setSpacing(4)

        # ==================================================
        # Eye Button
        # ==================================================

        self.eye_button = QToolButton(
            self.password_row
        )

        self.eye_button.setFixedSize(
            16,
            16
        )

        self.eye_button.setIconSize(
            QSize(14, 14)
        )

        self.eye_button.setCursor(
            Qt.PointingHandCursor
        )

        self.eye_button.setFocusPolicy(
            Qt.NoFocus
        )

        self.eye_button.setStyleSheet(
            """
            QToolButton
            {
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }

            QToolButton:hover
            {
                background: transparent;
                border: none;
            }

            QToolButton:pressed
            {
                background: transparent;
                border: none;
            }
            """
        )

        # ==================================================
        # Password Text
        # ==================================================

        self.password_text = QLabel(
            "نمایش رمز"
        )

        self.password_text.setFont(
            Fonts.text()
        )

        self.password_text.setStyleSheet(
            """
            QLabel
            {
                color: #64748B;

                background: transparent;

                border: none;

                font-size: 9px;

                padding: 0px;
            }
            """
        )

        self.password_text.setCursor(
            Qt.PointingHandCursor
        )

        # ==================================================
        # Row Layout
        # ==================================================

        self.password_layout.addWidget(
            self.eye_button
        )

        self.password_layout.addWidget(
            self.password_text
        )

        self.password_layout.addStretch()

        self.main_layout.addWidget(
            self.password_row
        )

        # ==================================================
        # Initial State
        # ==================================================

        self.password_row.hide()

        # ==================================================
        # Connections
        # ==================================================

        self.eye_button.clicked.connect(
            self.toggle_password_visibility
        )

        self.password_text.mousePressEvent = (
            self.password_text_clicked
        )

    # ==================================================
    # Add Password Action
    # ==================================================

    def set_password_action(
        self,
        widget
    ):

        if widget is None:
            return

        self.password_layout.insertWidget(
            0,
            widget
        )

    # ==================================================
    # Set Echo Mode
    # ==================================================

    def setEchoMode(
        self,
        mode
    ):

        self.line_edit.setEchoMode(
            mode
        )

        if mode == QLineEdit.Password:

            self.password_row.show()

            self.set_password_icon(
                False
            )

        else:

            self.password_row.hide()

        self.adjustSize()

    # ==================================================
    # Toggle Password
    # ==================================================

    def toggle_password_visibility(
        self
    ):

        if (
            self.line_edit.echoMode()
            == QLineEdit.Password
        ):

            self.line_edit.setEchoMode(
                QLineEdit.Normal
            )

            self.set_password_icon(
                True
            )

        else:

            self.line_edit.setEchoMode(
                QLineEdit.Password
            )

            self.set_password_icon(
                False
            )

        self.password_row.show()

        self.password_visibility_changed.emit(
            self.line_edit.echoMode()
            == QLineEdit.Normal
        )

        self.adjustSize()

        # فوکوس دوباره روی خود فیلد
        self.line_edit.setFocus()

    # ==================================================
    # Text Click
    # ==================================================

    def password_text_clicked(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.toggle_password_visibility()

        event.accept()

    # ==================================================
    # Set Password Icon
    # ==================================================

    def set_password_icon(
        self,
        visible
    ):

        if visible:

            self.eye_button.setIcon(
                QIcon(
                    "assets/icons/eye.svg"
                )
            )

            self.password_text.setText(
                "پنهان کردن رمز"
            )

        else:

            self.eye_button.setIcon(
                QIcon(
                    "assets/icons/eye-off.svg"
                )
            )

            self.password_text.setText(
                "نمایش رمز"
            )

        self.eye_button.show()

        self.password_text.show()

    # ==================================================
    # Text
    # ==================================================

    def text(
        self
    ):

        return self.line_edit.text()

    # ==================================================
    # Set Text
    # ==================================================

    def setText(
        self,
        text
    ):

        self.line_edit.setText(
            text
        )

    # ==================================================
    # Clear
    # ==================================================

    def clear(
        self
    ):

        self.line_edit.clear()

    # ==================================================
    # Set Focus
    # ==================================================

    def setFocus(
        self,
        reason=Qt.OtherFocusReason
    ):

        return self.line_edit.setFocus(
            reason
        )

    # ==================================================
    # Clear Focus
    # ==================================================

    def clearFocus(
        self
    ):

        self.line_edit.clearFocus()

    # ==================================================
    # Placeholder
    # ==================================================

    def setPlaceholderText(
        self,
        text
    ):

        self.line_edit.setPlaceholderText(
            text
        )

    # ==================================================
    # Echo Mode
    # ==================================================

    def echoMode(
        self
    ):

        return self.line_edit.echoMode()

    # ==================================================
    # Size
    # ==================================================

    def setFixedWidth(
        self,
        width
    ):

        super().setFixedWidth(
            width
        )

    # ==================================================
    # Font
    # ==================================================

    def setFont(
        self,
        font
    ):

        self.line_edit.setFont(
            font
        )