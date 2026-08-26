"""
==================================================
Project : حضور
File    : fonts.py
Purpose : Font Manager
==================================================
"""

from PySide6.QtGui import QFont


class Fonts:

    FAMILY = "IRANSans"


    # ==========================
    # Dashboard Main Title
    # ==========================
    @staticmethod
    def large_title():

        font = QFont(
            Fonts.FAMILY,
            28
        )

        font.setBold(True)

        return font



    # ==========================
    # Page Title
    # ==========================
    @staticmethod
    def title():

        font = QFont(
            Fonts.FAMILY,
            20
        )

        font.setBold(True)

        return font



    # ==========================
    # Section Title
    # ==========================
    @staticmethod
    def heading():

        font = QFont(
            Fonts.FAMILY,
            13
        )

        font.setBold(False)

        return font



    # ==========================
    # Button
    # ==========================
    @staticmethod
    def button():

        font = QFont(
            Fonts.FAMILY,
            11
        )

        font.setBold(True)

        return font



    # ==========================
    # Normal Text
    # ==========================
    @staticmethod
    def text():

        return QFont(
            Fonts.FAMILY,
            10
        )



    # ==========================
    # Input
    # ==========================
    @staticmethod
    def input():

        return QFont(
            Fonts.FAMILY,
            10
        )



    # ==========================
    # Small Text
    # ==========================
    @staticmethod
    def small():

        return QFont(
            Fonts.FAMILY,
            9
        )