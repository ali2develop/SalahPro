import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTimeEdit,
    QPushButton, QComboBox, QMainWindow, QFrame, QSpacerItem, QSizePolicy,
    QSystemTrayIcon, QMenu, QAction, QApplication
)
from PyQt5.QtCore import QTimer, QTime, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from core.azan_logic import AzanReminder


# This function is crucial for PyInstaller to find the assets folder
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SalahPRO App")
        self.setFixedSize(400, 500)

        # Use the resource_path function to get the correct path for the icon
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        self.should_quit = False
        self.create_tray_icon()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.prayers = {}
        prayer_names = ["Fajr", "Zhuhr", "Asr", "Maghrib", "Isha"]
        for name in prayer_names:
            row = QHBoxLayout()
            label = QLabel(f"{name} time:")
            time_edit = QTimeEdit()
            time_edit.setDisplayFormat("hh:mm AP")

            if name == "Fajr":
                time_edit.setTime(QTime(0, 0))
            else:
                time_edit.setTime(QTime(12, 0))

            self.prayers[name] = time_edit
            row.addWidget(label)
            row.addWidget(time_edit)
            layout.addLayout(row)

        self.action_dropdown = QComboBox()
        self.action_dropdown.setObjectName("action_dropdown")
        self.action_dropdown.addItems([
            "Only Reminder",
            "Reminder with Shutdown",
            "Reminder with Sleep"
        ])
        layout.addWidget(self.action_dropdown)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.set_btn = QPushButton("Set Timings")
        layout.addWidget(self.set_btn)

        self.status_label = QLabel("Status: Waiting for Entry...")
        self.status_label.setObjectName("status_label")
        self.status_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        layout.addWidget(self.status_label)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        close_button_layout = QHBoxLayout()

        brand_logo_label = QLabel()
        brand_logo_label.setObjectName("codenixLogo")
        # Use the resource_path function for the brand logo
        brand_pixmap = QPixmap(resource_path("assets/codenix_logo.png"))
        if not brand_pixmap.isNull():
            scaled_brand_pixmap = brand_pixmap.scaled(100, 100)
            brand_logo_label.setPixmap(scaled_brand_pixmap)

        close_button_layout.addWidget(brand_logo_label)
        close_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.clicked.connect(self.close)
        close_button_layout.addWidget(self.close_btn)

        layout.addLayout(close_button_layout)

        self.reminder = AzanReminder(self.status_label, self.action_dropdown)

        self.set_btn.clicked.connect(lambda: self.reminder.set_reminders(self.prayers))

        self.timer = QTimer()
        self.timer.timeout.connect(self.reminder.check_times)
        self.timer.start(10000)

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("assets/logo.png")))
        self.tray_icon.setToolTip("SalahPRO App")

        tray_menu = QMenu()
        show_action = QAction("Open SalahPRO", self)
        show_action.triggered.connect(self.restore_window)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def restore_window(self):
        self.show()
        self.activateWindow()

    def quit_app(self):
        self.should_quit = True
        QApplication.quit()

    def closeEvent(self, event):
        if self.should_quit:
            event.accept()
        else:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Reminder !",
                "SalahPRO minimized to tray.",
                QSystemTrayIcon.Information,
                2000
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
