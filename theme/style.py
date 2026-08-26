"""
==================================================
Project : حضور
File    : style.py
Author  : Reyhane Sarabi
Purpose : Global Application Styles
==================================================
"""


from theme.colors import Colors



class AppStyle:
    """
    استایل کلی برنامه

    تمام QSS های عمومی اینجا قرار می‌گیرند.
    """



    # ======================================
    # استایل اصلی برنامه
    # ======================================

    MAIN = f"""

    QWidget
    {{

        font-family: IRANSansX;

        color:{Colors.TEXT};

    }}



    QMainWindow
    {{

        background:{Colors.BACKGROUND};

    }}

    """



    # ======================================
    # کارت‌ها
    # ======================================

    CARD = f"""

    QFrame
    {{

        background:{Colors.CARD};

        border-radius:18px;

        border:1px solid {Colors.BORDER};

    }}

    """



    # ======================================
    # ScrollBar
    # ======================================

    SCROLLBAR = """

    QScrollBar:vertical

    {

        background:transparent;

        width:8px;

    }



    QScrollBar::handle:vertical

    {

        background:#B8C7D9;

        border-radius:4px;

    }



    QScrollBar::handle:vertical:hover

    {

        background:#7FA8D9;

    }

    """



    # ======================================
    # Table
    # ======================================

    TABLE = """

    QTableWidget

    {

        background:white;

        border:none;

        border-radius:15px;

        gridline-color:transparent;

    }



    QHeaderView::section

    {

        background:#EEF3F8;

        border:none;

        padding:10px;

        font-weight:bold;

    }



    QTableWidget::item

    {

        padding:8px;

    }



    QTableWidget::item:selected

    {

        background:#5B9DF9;

        color:white;

    }

    """



    # ======================================
    # گرفتن کل استایل
    # ======================================

    @staticmethod
    def get():

        return (

            AppStyle.MAIN

            +

            AppStyle.SCROLLBAR

            +

            AppStyle.TABLE

        )