from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QTimeEdit, QComboBox
)
from PyQt5.QtCore import QTimer
from core.azan_logic import AzanReminder
from ui.styles import dark_style


class MainPage(QWidget):
    def __init__(self, switch_to_reminder):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Welcome to SalahPro 🕌")
        label.setStyleSheet("font-size: 18px;")
        button = QPushButton("Open Namaz Reminder")
        button.clicked.connect(switch_to_reminder)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


class ReminderPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.status = QLabel("")

        self.prayers = {
            "Fajr": QTimeEdit(),
            "Dhuhr": QTimeEdit(),
            "Asr": QTimeEdit(),
            "Maghrib": QTimeEdit(),
            "Isha": QTimeEdit()
        }

        for name, widget in self.prayers.items():
            widget.setDisplayFormat("HH:mm")
            layout.addWidget(QLabel(f"{name} Time:"))
            layout.addWidget(widget)

        self.action_dropdown = QComboBox()
        self.action_dropdown.addItems(["Do Nothing", "Sleep on time", "Shutdown on time"])
        layout.addWidget(QLabel("Action after Azan:"))
        layout.addWidget(self.action_dropdown)

        self.reminder = AzanReminder(self.status, self.action_dropdown)

        activate_btn = QPushButton("Activate Reminder")
        activate_btn.clicked.connect(lambda: self.reminder.set_reminders(self.prayers))

        close_btn = QPushButton("Close Program")
        close_btn.clicked.connect(self.close_app)

        layout.addWidget(activate_btn)
        layout.addWidget(self.status)
        layout.addWidget(close_btn)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.reminder.check_times)
        self.timer.start(10000)

    def close_app(self):
        self.timer.stop()
        self.window().close()  # Closes the main window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SalahPro - Namaz Reminder")
        self.setStyleSheet(dark_style)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_page = MainPage(self.show_reminder_page)
        self.reminder_page = ReminderPage()

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.reminder_page)

    def show_reminder_page(self):
        self.stack.setCurrentWidget(self.reminder_page)

    def closeEvent(self, event):
        # Gracefully stop reminder timer if open
        if hasattr(self.reminder_page, "timer"):
            self.reminder_page.timer.stop()
        event.accept()
