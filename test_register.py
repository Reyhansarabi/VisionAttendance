import sys

from PySide6.QtWidgets import QApplication

from gui.pages.register_page import RegisterPage



app = QApplication(sys.argv)

window = RegisterPage()

window.resize(1200, 700)

window.show()

sys.exit(app.exec())