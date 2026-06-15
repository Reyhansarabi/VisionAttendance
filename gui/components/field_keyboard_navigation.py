from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtWidgets import QLineEdit


class FieldKeyboardNavigation(QObject):
    """Up/Down field navigation and Enter submit for a page."""

    def __init__(self, page, submit_widget=None, key_handler=None):
        super().__init__(page)
        self.page = page
        self.submit_widget = submit_widget
        self.key_handler = key_handler
        self.fields = []
        self.refresh()

    def refresh(self):
        # Remove this filter from fields belonging to the previous form mode.
        for field in getattr(self, "fields", []):
            try:
                field.removeEventFilter(self)
            except RuntimeError:
                pass

        self.fields = [
            widget
            for widget in self.page.findChildren(QLineEdit)
            if widget.isEnabled() and not widget.isReadOnly()
        ]
        self.fields.sort(key=self._position_key)
        for field in self.fields:
            field.installEventFilter(self)

    def _position_key(self, widget):
        pos = widget.mapTo(self.page, widget.rect().topLeft())
        return (pos.y(), pos.x())

    def _is_active(self, field):
        return field in self.fields and field.isVisible() and field.isEnabled()

    def eventFilter(self, watched, event):
        if not isinstance(watched, QLineEdit):
            return super().eventFilter(watched, event)
        if event.type() != QEvent.Type.KeyPress:
            return super().eventFilter(watched, event)
        if not self._is_active(watched):
            return super().eventFilter(watched, event)

        # Optional page-specific behavior (for example a suggestion popup).
        # Field navigation itself remains centralized in this class.
        if self.key_handler is not None:
            try:
                if self.key_handler(watched, event):
                    return True
            except RuntimeError:
                pass

        key = event.key()
        if key in (Qt.Key_Up, Qt.Key_Down):

            step = -1 if key == Qt.Key_Up else 1
            visible_fields = [field for field in self.fields if field.isVisible() and field.isEnabled()]
            if len(visible_fields) <= 1:
                return super().eventFilter(watched, event)
            try:
                current = visible_fields.index(watched)
            except ValueError:
                return super().eventFilter(watched, event)
            # Circular navigation: moving down from the last field
            # goes back to the first; moving up from the first goes
            # to the last.
            if key == Qt.Key_Down:
                next_index = (current + 1) % len(visible_fields)
            else:
                next_index = (current - 1) % len(visible_fields)

            target = visible_fields[next_index]
            target.setFocus(Qt.FocusReason.ShortcutFocusReason)
            return True

        if key in (Qt.Key_Return, Qt.Key_Enter):
            if self.submit_widget is not None and self.submit_widget.isVisible() and self.submit_widget.isEnabled():
                self.submit_widget.click()
                return True

        return super().eventFilter(watched, event)
