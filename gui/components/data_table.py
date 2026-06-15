# ==================================================
# Project : حضور
# File    : data_table.py
# Author  : Reyhane Sarabi
# Purpose : Professional Table Component
# ==================================================

from PySide6.QtWidgets import (
    QTableView,
    QAbstractItemView,
    QHeaderView,
    QStyledItemDelegate,
    QStyle,
    QApplication,
)

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QSortFilterProxyModel,
    QEvent
)

from PySide6.QtGui import (
    QColor,
    QPalette
)

from theme.colors import Colors


# ==================================================
# Delegate جدول
# ==================================================

class TableRowDelegate(QStyledItemDelegate):

    def __init__(
        self,
        table,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.table = table

    # ==================================================
    # Paint
    # ==================================================

    def paint(
        self,
        painter,
        option,
        index
    ):

        painter.save()

        # ------------------------------------------
        # حذف Hover پیش‌فرض Qt
        # ------------------------------------------

        option.state &= ~QStyle.State_MouseOver

        # ------------------------------------------
        # Selection
        # ------------------------------------------

        is_selected = False

        if self.table.selectionModel():

            is_selected = (
                self.table.selectionModel()
                .isRowSelected(
                    index.row(),
                    QModelIndex()
                )
            )

        # ------------------------------------------
        # Hover
        # ------------------------------------------

        is_hovered = (
            self.table.hovered_row != -1
            and index.row() == self.table.hovered_row
        )

        # ------------------------------------------
        # Row colors
        # ------------------------------------------

        if is_selected:

            # آبی ملایم برای Selected
            background_color = QColor(
                "#5699D7"
            )

        elif is_hovered:

            # Hover بسیار ظریف
            background_color = QColor(
                "#F3F8FD"
            )

        else:

            # سفید بسیار ملایم
            background_color = QColor(
                "#FCFDFE"
            )

        # ------------------------------------------
        # Rectangle
        # ------------------------------------------

        rect = option.rect

        row_rect = rect.adjusted(
            0,
            3,
            0,
            -3
        )

        column_count = 0

        if self.table.model() is not None:

            column_count = (
                self.table.model()
                .columnCount()
            )

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            background_color
        )

        # ------------------------------------------
        # First column
        # ------------------------------------------

        if index.column() == 0:

            painter.drawRoundedRect(
                row_rect,
                10,
                10
            )

            painter.drawRect(
                row_rect.left() + 10,
                row_rect.top(),
                row_rect.width() - 10,
                row_rect.height()
            )

        # ------------------------------------------
        # Last column
        # ------------------------------------------

        elif index.column() == column_count - 1:

            painter.drawRoundedRect(
                row_rect,
                10,
                10
            )

            painter.drawRect(
                row_rect.left(),
                row_rect.top(),
                row_rect.width() - 10,
                row_rect.height()
            )

        # ------------------------------------------
        # Middle columns
        # ------------------------------------------

        else:

            painter.drawRect(
                row_rect
            )

        painter.restore()

        # ------------------------------------------
        # Text colors
        # ------------------------------------------

        if is_selected:

            option.palette.setColor(
                QPalette.ColorRole.Text,
                QColor("#FFFFFF")
            )

            option.palette.setColor(
                QPalette.ColorRole.WindowText,
                QColor("#FFFFFF")
            )

        elif is_hovered:

            option.palette.setColor(
                QPalette.ColorRole.Text,
                QColor("#315A7D")
            )

            option.palette.setColor(
                QPalette.ColorRole.WindowText,
                QColor("#315A7D")
            )

        else:

            option.palette.setColor(
                QPalette.ColorRole.Text,
                QColor("#334155")
            )

            option.palette.setColor(
                QPalette.ColorRole.WindowText,
                QColor("#334155")
            )

        # ------------------------------------------
        # Remove default background
        # ------------------------------------------

        option.backgroundBrush = Qt.NoBrush

        # ------------------------------------------
        # Text
        # ------------------------------------------

        super().paint(
            painter,
            option,
            index
        )


# ==================================================
# Model جدول
# ==================================================

class TableModel(
    QAbstractTableModel
):

    def __init__(
        self,
        headers,
        data=None
    ):

        super().__init__()

        self.headers = (
            headers or []
        )

        self.data_list = (
            data or []
        )

    # ==================================================
    # Row Count
    # ==================================================

    def rowCount(
        self,
        parent=QModelIndex()
    ):

        if parent.isValid():

            return 0

        return len(
            self.data_list
        )

    # ==================================================
    # Column Count
    # ==================================================

    def columnCount(
        self,
        parent=QModelIndex()
    ):

        if parent.isValid():

            return 0

        return len(
            self.headers
        )

    # ==================================================
    # Data
    # ==================================================

    def data(
        self,
        index,
        role=Qt.DisplayRole
    ):

        if not index.isValid():

            return None
        
        if role == Qt.TextAlignmentRole:

            return (
                Qt.AlignmentFlag.AlignCenter
                | Qt.AlignmentFlag.AlignVCenter
            )

        if role == Qt.DisplayRole:

            row = index.row()

            column = index.column()

            if (
                0 <= row < len(
                    self.data_list
                )
                and
                0 <= column < len(
                    self.data_list[row]
                )
            ):

                value = (
                    self.data_list[row][column]
                )

                if value is None:

                    return ""

                return str(
                    value
                )

        return None

    # ==================================================
    # Header
    # ==================================================

    def headerData(
        self,
        section,
        orientation,
        role=Qt.DisplayRole
    ):

        if role != Qt.DisplayRole:

            return None

        if orientation == Qt.Horizontal:

            if (
                0 <= section
                < len(self.headers)
            ):

                return self.headers[
                    section
                ]

        return None

    # ==================================================
    # Update Data
    # ==================================================

    def update_data(
        self,
        new_data
    ):

        self.beginResetModel()

        self.data_list = (
            new_data or []
        )

        self.endResetModel()

    # ==================================================
    # Remove Row
    # ==================================================

    def remove_row(
        self,
        row
    ):

        if row < 0:

            return

        if row >= len(
            self.data_list
        ):

            return

        self.beginRemoveRows(
            QModelIndex(),
            row,
            row
        )

        self.data_list.pop(
            row
        )

        self.endRemoveRows()


# ==================================================
# Data Table
# ==================================================

class DataTable(
    QTableView
):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        # ------------------------------------------
        # Models
        # ------------------------------------------

        self.table_model = None

        self.proxy = None

        # ------------------------------------------
        # Selection
        # ------------------------------------------

        self.selected_row = -1

        # ------------------------------------------
        # Hover
        # ------------------------------------------

        self.hovered_row = -1

        # ------------------------------------------
        # UI
        # ------------------------------------------

        self.setup_ui()

        # ------------------------------------------
        # Click
        # ------------------------------------------

        self.clicked.connect(
            self.row_selected
        )

        # ------------------------------------------
        # Global Mouse Event
        # ------------------------------------------

        app = QApplication.instance()

        if app is not None:

            app.installEventFilter(
                self
            )

    # ==================================================
    # Event Filter
    # ==================================================

    def eventFilter(
        self,
        watched,
        event
    ):

        if event.type() == QEvent.Type.MouseButtonPress:

            position = (
                event.globalPosition()
                .toPoint()
            )

            table_position = (
                self.mapFromGlobal(
                    position
                )
            )

            index = self.indexAt(
                table_position
            )

            # ------------------------------------------
            # کلیک خارج از ردیف
            # ------------------------------------------

            if not index.isValid():

                if self.selected_row != -1:

                    self.clearSelection()

                    self.setCurrentIndex(
                        QModelIndex()
                    )

                    self.selected_row = -1

                    self.hovered_row = -1

                    self.viewport().update()

        return super().eventFilter(
            watched,
            event
        )

    # ==================================================
    # Search
    # ==================================================

    def search(
        self,
        text
    ):

        if self.proxy is None:

            return

        self.proxy.setFilterFixedString(
            text
        )

    # ==================================================
    # VIEWPORT EVENT
    # ==================================================

    def viewportEvent(
        self,
        event
    ):

        if event.type() == QEvent.Type.MouseButtonPress:

            position = (
                event.position()
                .toPoint()
            )

            index = self.indexAt(
                position
            )

            if not index.isValid():

                self.clearSelection()

                self.setCurrentIndex(
                    QModelIndex()
                )

                self.selected_row = -1

                self.hovered_row = -1

                self.viewport().update()

                event.accept()

                return True

        return super().viewportEvent(
            event
        )

    # ==================================================
    # Setup UI
    # ==================================================

    def setup_ui(self):

        self.setObjectName(
            "DataTable"
        )

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet(
            f"""

            /* ==========================================
               TABLE
               ========================================== */

            QTableView#DataTable
            {{
                background: transparent;

                border: none;

                border-radius: 18px;

                gridline-color: transparent;

                outline: none;

                selection-background-color: transparent;

                selection-color: white;

                padding: 0px;

                show-decoration-selected: 0;
            }}


            /* ==========================================
               CELLS
               ========================================== */

            QTableView#DataTable::item
            {{
                background: transparent;

                color: #334155;

                padding: 11px 16px;

                border: none;
            }}


            /* ==========================================
               HOVER
               ========================================== */

            QTableView#DataTable::item:hover
            {{
                background: transparent;
            }}


            /* ==========================================
               SELECTED
               ========================================== */

            QTableView#DataTable::item:selected
            {{
                background: transparent;

                color: white;

                border: none;
            }}


            QTableView#DataTable::item:selected:hover
            {{
                background: transparent;

                color: white;
            }}


            /* ==========================================
               HEADER
               ========================================== */

            QHeaderView::section
            {{
                background: #F1F6FB;

                color: #334155;

                border: none;

                padding: 12px 16px;

                font-weight: 600;

                border-bottom: 1px solid #E5EDF5;
            }}


            /* ==========================================
               HEADER CORNERS
               ========================================== */

            QHeaderView::section:first
            {{
                border-top-left-radius: 12px;

                border-bottom-left-radius: 12px;
            }}


            QHeaderView::section:last
            {{
                border-top-right-radius: 12px;

                border-bottom-right-radius: 12px;
            }}


            /* ==========================================
               HEADER VIEW
               ========================================== */

            QTableView#DataTable QHeaderView
            {{
                background: transparent;

                border: none;
            }}


            /* ==========================================
               SCROLLBAR VERTICAL
               ========================================== */

            QScrollBar:vertical
            {{
                background: transparent;

                width: 5px;

                margin: 8px 1px 8px 1px;
            }}


            QScrollBar::handle:vertical
            {{
                background: #C9D9E8;

                border-radius: 3px;

                min-height: 32px;
            }}


            QScrollBar::handle:vertical:hover
            {{
                background: #AFC7DC;
            }}


            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical
            {{
                height: 0px;

                background: transparent;
            }}


            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical
            {{
                background: transparent;
            }}


            /* ==========================================
               SCROLLBAR HORIZONTAL
               ========================================== */

            QScrollBar:horizontal
            {{
                background: transparent;

                height: 5px;

                margin: 1px 8px 1px 8px;
            }}


            QScrollBar::handle:horizontal
            {{
                background: #C9D9E8;

                border-radius: 3px;

                min-width: 32px;
            }}


            QScrollBar::handle:horizontal:hover
            {{
                background: #AFC7DC;
            }}


            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal
            {{
                width: 0px;

                background: transparent;
            }}


            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal
            {{
                background: transparent;
            }}

            """
        )

        # ==================================================
        # SELECT ROW
        # ==================================================

        self.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        # ==================================================
        # SINGLE SELECTION
        # ==================================================

        self.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        # ==================================================
        # READ ONLY
        # ==================================================

        self.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        # ==================================================
        # VERTICAL SCROLL
        # ==================================================

        self.setVerticalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )

        # ==================================================
        # HORIZONTAL SCROLL
        # ==================================================

        self.setHorizontalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )

        # ==================================================
        # COLUMN SIZE
        # ==================================================

        header = (
            self.horizontalHeader()
        )

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        # ==================================================
        # HIDE ROW NUMBERS
        # ==================================================

        self.verticalHeader().setVisible(
            False
        )

        # ==================================================
        # ROW HEIGHT
        # ==================================================

        self.verticalHeader().setDefaultSectionSize(
            54
        )

        # ==================================================
        # NO FOCUS RECTANGLE
        # ==================================================

        self.setFocusPolicy(
            Qt.NoFocus
        )

        # ==================================================
        # MOUSE TRACKING
        # ==================================================

        self.setMouseTracking(
            True
        )

        self.viewport().setMouseTracking(
            True
        )

        # ==================================================
        # REMOVE GRID
        # ==================================================

        self.setShowGrid(
            False
        )

        # ==================================================
        # DELEGATE
        # ==================================================

        self.setItemDelegate(
            TableRowDelegate(
                self,
                self
            )
        )

    # ==================================================
    # Set Table Data
    # ==================================================

    def set_table_data(
        self,
        headers,
        data
    ):

        self.table_model = (
            TableModel(
                headers,
                data
            )
        )

        self.proxy = (
            QSortFilterProxyModel(
                self
            )
        )

        self.proxy.setSourceModel(
            self.table_model
        )

        self.proxy.setFilterCaseSensitivity(
            Qt.CaseInsensitive
        )

        self.proxy.setFilterKeyColumn(
            -1
        )

        self.setModel(
            self.proxy
        )

        self.selected_row = -1

        self.hovered_row = -1

        self.viewport().update()

    # ==================================================
    # Update Table Data
    # ==================================================

    def update_table_data(
        self,
        data
    ):

        if self.table_model is None:

            return

        self.table_model.update_data(
            data
        )

        self.clearSelection()

        self.setCurrentIndex(
            QModelIndex()
        )

        self.selected_row = -1

        self.hovered_row = -1

        self.viewport().update()

    # ==================================================
    # Row Selected
    # ==================================================

    def row_selected(
        self,
        proxy_index
    ):

        if not proxy_index.isValid():

            self.selected_row = -1

            self.viewport().update()

            return

        self.selected_row = (
            proxy_index.row()
        )

        self.viewport().update()

        print(
            "Selected Proxy Row:",
            self.selected_row
        )

    # ==================================================
    # Hover Row
    # ==================================================

    def mouseMoveEvent(
        self,
        event
    ):

        position = (
            event.position()
            .toPoint()
        )

        index = (
            self.indexAt(
                position
            )
        )

        new_hovered_row = -1

        if index.isValid():

            new_hovered_row = (
                index.row()
            )

        if (
            new_hovered_row
            != self.hovered_row
        ):

            self.hovered_row = (
                new_hovered_row
            )

            self.viewport().update()

        super().mouseMoveEvent(
            event
        )

    # ==================================================
    # Leave Table
    # ==================================================

    def leaveEvent(
        self,
        event
    ):

        if self.hovered_row != -1:

            self.hovered_row = -1

            self.viewport().update()

        super().leaveEvent(
            event
        )

    # ==================================================
    # Mouse Press
    # ==================================================

    def mousePressEvent(
        self,
        event
    ):

        index = self.indexAt(
            event.position().toPoint()
        )

        # ------------------------------------------
        # اگر کلیک روی خود ردیف نبود
        # ------------------------------------------

        if not index.isValid():

            self.clearSelection()

            self.setCurrentIndex(
                QModelIndex()
            )

            self.selected_row = -1

            self.hovered_row = -1

            self.viewport().update()

            event.accept()

            return

        # ------------------------------------------
        # کلیک روی ردیف
        # ------------------------------------------

        super().mousePressEvent(
            event
        )

    # ==================================================
    # Get Selected Source Row
    # ==================================================

    def get_selected_source_row(
        self
    ):

        if self.selected_row == -1:

            return -1

        if self.proxy is None:

            return -1

        proxy_index = (
            self.proxy.index(
                self.selected_row,
                0
            )
        )

        if not proxy_index.isValid():

            return -1

        source_index = (
            self.proxy.mapToSource(
                proxy_index
            )
        )

        if not source_index.isValid():

            return -1

        return source_index.row()

    # ==================================================
    # Get Selected Row Data
    # ==================================================

    def get_selected_row_data(
        self
    ):

        source_row = (
            self.get_selected_source_row()
        )

        if source_row == -1:

            return None

        if self.table_model is None:

            return None

        if source_row >= len(
            self.table_model.data_list
        ):

            return None

        return (
            self.table_model.data_list[
                source_row
            ]
        )

    # ==================================================
    # Remove Selected Row
    # ==================================================

    def remove_selected_row(
        self
    ):

        source_row = (
            self.get_selected_source_row()
        )

        if source_row == -1:

            return

        self.table_model.remove_row(
            source_row
        )

        self.clearSelection()

        self.setCurrentIndex(
            QModelIndex()
        )

        self.selected_row = -1

        self.hovered_row = -1

        self.viewport().update()

    # ==================================================
    # Clear Table
    # ==================================================

    def clear_table(
        self
    ):

        if self.table_model is None:

            return

        self.table_model.update_data(
            []
        )

        self.clearSelection()

        self.setCurrentIndex(
            QModelIndex()
        )

        self.selected_row = -1

        self.hovered_row = -1

        self.viewport().update()

