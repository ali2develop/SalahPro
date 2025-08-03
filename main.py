from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from ui.styles import get_dark_theme_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application icon with the correct path
    app.setWindowIcon(QIcon("assets/logo.png"))

    # Apply the stylesheet to the entire application
    app.setStyleSheet(get_dark_theme_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



