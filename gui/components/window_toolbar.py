"""
==================================================
Project : حضور
File    : window_toolbar.py
Purpose : Custom window controls for the main window
==================================================
"""

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class WindowToolbar(QFrame):

    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.window = window
        self.drag_position = None

        self.setObjectName("WindowToolbar")
        self.setFixedHeight(44)

        # ------------------------------------------------
        # Keep toolbar layout independent from parent RTL
        # ------------------------------------------------

        self.setLayoutDirection(
            Qt.LayoutDirection.LeftToRight
        )

        self.setStyleSheet(
            """
            QFrame#WindowToolbar {
                background: #E8F0F7;
                border: none;
                border-bottom: 1px solid #D5E1EC;
                border-radius: 0px;
            }

            QLabel#WindowTitle {
                color: #526579;
                background: transparent;
                border: none;
                border-radius: 0px;
                font-size: 11px;
                font-weight: 600;
                padding-right: 10px;
            }

            QPushButton.WindowControl {
                background: transparent;
                color: #526579;
                border: none;
                border-radius: 0px;
                min-width: 36px;
                max-width: 36px;
                min-height: 30px;
                max-height: 30px;
                font-size: 17px;
                font-weight: 500;
            }

            QPushButton.WindowControl:hover {
                background: #CBD8E5;
                color: #26384A;
            }

            QPushButton.WindowControl:pressed {
                background: #B9C9D8;
                color: #1F3040;
            }

            QPushButton#CloseButton {
                background: transparent;
                color: #526579;
                border: none;
                border-radius: 0px;
                min-width: 36px;
                max-width: 36px;
                min-height: 30px;
                max-height: 30px;
                font-size: 18px;
                font-weight: 500;
            }

            QPushButton#CloseButton:hover {
                background: #FECACA;
                color: #DC2626;
            }

            QPushButton#CloseButton:pressed {
                background: #FCA5A5;
                color: #B91C1C;
            }
            """
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            10,
            5,
            10,
            5
        )

        layout.setSpacing(3)

        # ==================================================
        # Title
        # ==================================================

        self.title = QLabel("حضور")

        self.title.setObjectName(
            "WindowTitle"
        )

        self.title.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        # Handle double-click even when Qt delivers
        # the event through a child/title area.
        self.installEventFilter(self)
        self.title.installEventFilter(self)

        # ==================================================
        # Minimize Button
        # ==================================================

        self.minimize_button = QPushButton(
            "−"
        )

        self.minimize_button.setObjectName(
            "MinimizeButton"
        )

        self.minimize_button.setProperty(
            "class",
            "WindowControl"
        )

        self.minimize_button.setToolTip(
            "کوچک کردن"
        )

        self.minimize_button.clicked.connect(
            self.window.showMinimized
        )

        # ==================================================
        # Maximize Button
        # ==================================================

        self.maximize_button = QPushButton(
            "□"
        )

        self.maximize_button.setObjectName(
            "MaximizeButton"
        )

        self.maximize_button.setProperty(
            "class",
            "WindowControl"
        )

        self.maximize_button.setToolTip(
            "بزرگ کردن"
        )

        self.maximize_button.clicked.connect(
            self.toggle_maximize
        )

        # ==================================================
        # Close Button
        # ==================================================

        self.close_button = QPushButton(
            "×"
        )

        self.close_button.setObjectName(
            "CloseButton"
        )

        self.close_button.setToolTip(
            "خروج"
        )

        self.close_button.clicked.connect(
            self.window.close
        )

        # ==================================================
        # Final Order
        # ==================================================
        # Left:
        #   حضور
        #
        # Right:
        #   Minimize - Maximize - Close
        # ==================================================

        layout.addWidget(
            self.title
        )

        layout.addStretch()

        layout.addWidget(
            self.minimize_button
        )

        layout.addWidget(
            self.maximize_button
        )

        layout.addWidget(
            self.close_button
        )

    def toggle_maximize(self):

        if self.window.isMaximized():

            self.window.showNormal()

            self.maximize_button.setText(
                "□"
            )

            self.maximize_button.setToolTip(
                "بزرگ کردن"
            )

        else:

            self.window.showMaximized()

            self.maximize_button.setText(
                "❐"
            )

            self.maximize_button.setToolTip(
                "بازگردانی اندازه"
            )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.window.frameGeometry().topLeft()
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(self, event):

        if (
            self.drag_position is not None
            and event.buttons()
            & Qt.MouseButton.LeftButton
        ):

            if self.window.isMaximized():

                self.window.showNormal()

                self.maximize_button.setText(
                    "□"
                )

                self.maximize_button.setToolTip(
                    "بزرگ کردن"
                )

                self.drag_position = QPoint(
                    self.window.width() // 2,
                    10,
                )

            self.window.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(self, event):

        self.drag_position = None

        super().mouseReleaseEvent(
            event
        )

    def eventFilter(self, watched, event):

        # Only react to a double-click on
        # the toolbar/title area.
        # Window-control buttons are intentionally excluded.

        if event.type() == event.Type.MouseButtonDblClick:

            if (
                event.button()
                == Qt.MouseButton.LeftButton
                and watched in (
                    self,
                    self.title
                )
            ):

                self.toggle_maximize()

                event.accept()

                return True

        return super().eventFilter(
            watched,
            event
        )

    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.toggle_maximize()

            event.accept()

            return

        super().mouseDoubleClickEvent(
            event
        )