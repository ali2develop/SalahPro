import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QLabel, QTimeEdit, QMessageBox,
    QStackedWidget, QComboBox
)
from PyQt5.QtCore import QTimer, QTime, QUrl
from PyQt5.QtMultimedia import QSoundEffect


class MainPage(QWidget):
    def __init__(self, switch_to_reminder):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to the App")
        self.button = QPushButton("Namaz Reminder")
        self.button.clicked.connect(switch_to_reminder)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)


class ReminderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.status = QLabel("")

        self.target_times = {}
        self.triggered_flags = {}

        # Namaz time inputs
        self.prayers = {
            "Fajr": QTimeEdit(),
            "Dhuhr": QTimeEdit(),
            "Asr": QTimeEdit(),
            "Maghrib": QTimeEdit(),
            "Isha": QTimeEdit()
        }

        for name, widget in self.prayers.items():
            widget.setDisplayFormat("HH:mm")
            label = QLabel(f"{name} Time:")
            self.layout.addWidget(label)
            self.layout.addWidget(widget)

        # Action selection dropdown
        self.action_label = QLabel("Action after Azan:")
        self.action_dropdown = QComboBox()
        self.action_dropdown.addItems(["Do Nothing", "Sleep on time", "Shutdown on time"])
        self.layout.addWidget(self.action_label)
        self.layout.addWidget(self.action_dropdown)

        # Set Reminder Button
        self.set_button = QPushButton("Activate Reminder")
        self.set_button.clicked.connect(self.set_reminders)
        self.layout.addWidget(self.set_button)

        self.layout.addWidget(self.status)

        # Close Program Button
        self.close_button = QPushButton("Close Program")
        self.close_button.clicked.connect(self.close_app)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile("azan.wav"))
        self.sound.setLoopCount(1)

        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.check_times)
        self.main_timer.start(10000)

        self.action_initiated = False

    def set_reminders(self):
        self.target_times.clear()
        self.triggered_flags.clear()
        self.action_initiated = False

        for name, widget in self.prayers.items():
            self.target_times[name] = widget.time()
            self.triggered_flags[name] = False

        self.status.setText("Reminders activated!")

    def check_times(self):
        if not self.target_times:
            return

        now = QTime.currentTime()
        for name, target in self.target_times.items():
            if now.hour() == target.hour() and now.minute() == target.minute():
                if not self.triggered_flags.get(name, False):
                    self.status.setText(f"{name} Azan time! Playing sound...")
                    self.sound.play()
                    self.triggered_flags[name] = True

                    if not self.action_initiated:
                        QTimer.singleShot(60000, self.perform_action)

    def perform_action(self):
        if self.action_initiated:
            return

        self.action_initiated = True

        action = self.action_dropdown.currentText()

        if action == "Shutdown on time":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Time Alert")
            msg.setText("You are late! Shutting down in 30 seconds.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            subprocess.run(["shutdown", "/s", "/t", "30"])

        elif action == "Sleep on time":
            self.status.setText("Going to sleep...")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        else:
            self.status.setText("Azan played. No further action taken.")

    def close_app(self):
        QApplication.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Namaz Reminder App")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_page = MainPage(self.show_reminder_page)
        self.reminder_page = ReminderPage()

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.reminder_page)

    def show_reminder_page(self):
        self.stack.setCurrentWidget(self.reminder_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
