"""
==================================================
Project : حضور
File    : main.py
Purpose : Program Entry Point
==================================================
"""

import sys

from PySide6.QtWidgets import QApplication

from database.database import DatabaseManager

from gui.pages.login_page import LoginPage
from core.app import MainWindow


def main():

    # ==================================================
    # Database
    # ==================================================

    database = DatabaseManager()

    database.create_tables()

    # ==================================================
    # Qt App
    # ==================================================

    app = QApplication(
        sys.argv
    )

    # ==================================================
    # Login Window
    # ==================================================

    login = LoginPage()

    # نگه داشتن پنجره اصلی
    window = None

    # ==================================================
    # Open Main Window After Login
    # ==================================================

    def open_main_window(
        username,
        role,
        user_id
    ):

        nonlocal window

        # اگر قبلاً پنجره اصلی ساخته شده،
        # آن را حذف می‌کنیم.
        if window is not None:

            window.close()

            window = None

        # ==================================================
        # ساخت MainWindow با نقش کاربر
        # ==================================================

        window = MainWindow(
            username=username,
            role=role,
            user_id=user_id,
            login_window=login
        )

        # ==================================================
        # نمایش
        # ==================================================

        window.show()

        # Login فقط مخفی شود
        login.hide()

    # ==================================================
    # Login Signal
    # ==================================================
    #
    # LoginPage در پروژه فعلی سه مقدار ارسال می‌کند:
    # username, role, user_id
    # ==================================================

    login.login_success.connect(
        open_main_window
    )

    # ==================================================
    # Show Login
    # ==================================================

    login.show()

    # ==================================================
    # Run
    # ==================================================

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()