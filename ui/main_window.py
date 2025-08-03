from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTimeEdit,
    QPushButton, QComboBox, QMainWindow, QFrame
)
from PyQt5.QtCore import QTimer, QTime
from core.azan_logic import AzanReminder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Azan Reminder App")
        self.setFixedSize(400, 400)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Prayer times UI
        self.prayers = {}
        prayer_names = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        for name in prayer_names:
            row = QHBoxLayout()
            label = QLabel(f"{name} time:")
            time_edit = QTimeEdit()
            time_edit.setDisplayFormat("hh:mm AP")
            time_edit.setTime(QTime.currentTime())
            self.prayers[name] = time_edit
            row.addWidget(label)
            row.addWidget(time_edit)
            layout.addLayout(row)

        # Action dropdown
        self.action_dropdown = QComboBox()
        self.action_dropdown.addItems([
            "None",
            "Shutdown on time",
            "Sleep on time"
        ])
        layout.addWidget(self.action_dropdown)

        # Set reminder button
        self.set_btn = QPushButton("Set Reminders")
        layout.addWidget(self.set_btn)

        # Status label
        self.status_label = QLabel("Status: Waiting for input...")
        self.status_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        layout.addWidget(self.status_label)

        # Setup logic
        self.reminder = AzanReminder(self.status_label, self.action_dropdown)
        self.set_btn.clicked.connect(lambda: self.reminder.set_reminders(self.prayers))

        # Timer to check every 10 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.reminder.check_times)
        self.timer.start(10000)
