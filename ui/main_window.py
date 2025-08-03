from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTimeEdit,
    QPushButton, QComboBox, QMainWindow, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QIcon, QPixmap
from core.azan_logic import AzanReminder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Azan Reminder App")
        self.setFixedSize(400, 500)

        # This line sets the window icon, which is what you want for the taskbar
        self.setWindowIcon(QIcon("assets/logo.png"))

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Removed the app logo label from the layout

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
        self.action_dropdown.setObjectName("action_dropdown")
        self.action_dropdown.addItems([
            "None",
            "Shutdown on time",
            "Sleep on time"
        ])
        layout.addWidget(self.action_dropdown)

        # Spacer to push the next button downwards
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set reminder button
        self.set_btn = QPushButton("Set Reminders")
        layout.addWidget(self.set_btn)

        # Status label
        self.status_label = QLabel("Status: Waiting for input...")
        self.status_label.setObjectName("status_label")
        self.status_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        layout.addWidget(self.status_label)

        # Spacer to separate the status label from the new close button
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # New layout for the close button and the brand logo
        close_button_layout = QHBoxLayout()

        # This is your brand logo, kept in the layout as you requested
        brand_logo_label = QLabel()
        brand_logo_label.setObjectName("codenixLogo")
        brand_pixmap = QPixmap("assets/codenix_logo.png")
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
