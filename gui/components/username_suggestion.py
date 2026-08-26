"""
==================================================
Project : حضور
File    : username_suggestion.py
Purpose : Username Suggestion Dropdown with Frequency Sorting
==================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import QColor

from PySide6.QtCore import Qt, Signal

from theme.fonts import Fonts


class UsernameSuggestionDropdown(QFrame):
    """
    Dropdown popup that shows username suggestions
    sorted by frequency (only usernames with count > 1).

    Signals:
        suggestion_selected(str) - emitted when user clicks a suggestion
    """

    suggestion_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._items = []
        self._selected_index = -1

        self.setWindowFlags(
            Qt.Popup
        )

        self.setFixedWidth(280)

        self.setStyleSheet(
            """
            QFrame {
                background: #FFFFFF;
                border: 1px solid #D9E3EE;
                border-radius: 10px;
            }
            """
        )

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        # Layout
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 4, 0, 4)
        self._layout.setSpacing(0)

    # ==================================================
    # Show Suggestions
    # ==================================================

    def show_suggestions(
        self, freq_map, typed_text="", anchor=None
    ):
        """
        Show suggestions from freq_map.
        freq_map: dict like {"Ali": 3, "Reza": 2, "Sara": 1}
        typed_text: current text in QLineEdit to filter
        """

        # Clear old items
        for item in self._items:
            item.setParent(None)
            item.deleteLater()
        self._items.clear()
        self._selected_index = -1

        # Filter: only count > 1, and match typed text
        suggestions = [
            (name, count)
            for name, count in freq_map.items()
            if count > 1
        ]

        if typed_text.strip():
            suggestions = [
                (name, count)
                for name, count in suggestions
                if name.startswith(typed_text.strip())
            ]

        # Sort by frequency (desc), then alphabetically
        suggestions.sort(
            key=lambda x: (-x[1], x[0])
        )

        if not suggestions:
            self.hide()
            return

        # Build items
        font = Fonts.text()

        for name, count in suggestions:
            item_label = QLabel(
                f"{name}  ({count})"
            )

            item_label.setFont(font)

            item_label.setFixedHeight(32)

            item_label.setStyleSheet(
                """
                QLabel {
                    color: #334155;
                    background: transparent;
                    border: none;
                    padding: 4px 14px;
                    border-radius: 0px;
                }
                QLabel:hover {
                    background: #EDF2F7;
                }
                """
            )

            item_label.setCursor(
                Qt.PointingHandCursor
            )

            item_label.mousePressEvent = (
                lambda event, n=name: (
                    self.suggestion_selected.emit(n),
                    self.hide()
                )
            )

            self._layout.addWidget(item_label)

            self._items.append(item_label)

        self.adjustSize()

        # Position below the live username field. The dropdown is a top-level
        # popup, so it is not destroyed when the login card is rebuilt.
        if anchor is not None:
            pos = anchor.mapToGlobal(
                anchor.rect().bottomLeft()
            )
            self.move(pos.x(), pos.y() + 4)

        self.show()

    # ==================================================
    # Keyboard Navigation in Dropdown
    # ==================================================

    def navigate_up(self):
        if not self._items:
            return False

        if self._selected_index > 0:
            self._select_item(
                self._selected_index - 1
            )
            return True

        return False

    def navigate_down(self):
        if not self._items:
            return False

        if self._selected_index < (
            len(self._items) - 1
        ):
            self._select_item(
                self._selected_index + 1
            )
            return True

        return False

    def select_current(self):
        if (
            0
            <= self._selected_index
            < len(self._items)
        ):
            name = self._items[
                self._selected_index
            ].text().split("  (")[0]

            self.suggestion_selected.emit(name)

            self.hide()

            return True

        return False

    def is_at_top(self):
        return self._selected_index <= 0

    def is_at_bottom(self):
        return self._selected_index >= (
            len(self._items) - 1
        )

    def is_visible_and_has_items(self):
        try:
            return bool(self.isVisible()) and bool(self._items)
        except RuntimeError:
            return False

    # ==================================================
    # Private
    # ==================================================

    def _select_item(self, index):
        # Deselect old
        if (
            0
            <= self._selected_index
            < len(self._items)
        ):
            self._items[
                self._selected_index
            ].setStyleSheet(
                """
                QLabel {
                    color: #334155;
                    background: transparent;
                    border: none;
                    padding: 4px 14px;
                }
                QLabel:hover {
                    background: #EDF2F7;
                }
                """
            )

        self._selected_index = index

        # Select new
        self._items[index].setStyleSheet(
            """
            QLabel {
                color: #334155;
                background: #EBF0F7;
                border: none;
                padding: 4px 14px;
            }
            """
        )

    # ==================================================
    # Hide
    # ==================================================

    def hideEvent(self, event):
        self._selected_index = -1

        for item in self._items:
            item.setStyleSheet(
                """
                QLabel {
                    color: #334155;
                    background: transparent;
                    border: none;
                    padding: 4px 14px;
                }
                QLabel:hover {
                    background: #EDF2F7;
                }
                """
            )

        super().hideEvent(event)


    def closeEvent(self, event):
        self.hide()
        event.accept()
