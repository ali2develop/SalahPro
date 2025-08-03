import os
import subprocess
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl, QTimer, QTime
from PyQt5.QtWidgets import QMessageBox

class AzanReminder:
    def __init__(self, status_label, action_dropdown):
        self.status = status_label
        self.action_dropdown = action_dropdown
        self.target_times = {}
        self.triggered_flags = {}
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile("assets/azan.wav"))
        self.sound.setLoopCount(1)
        self.action_initiated = False

    def set_reminders(self, prayers):
        self.target_times.clear()
        self.triggered_flags.clear()
        self.action_initiated = False
        for name, widget in prayers.items():
            self.target_times[name] = widget.time()
            self.triggered_flags[name] = False
        self.status.setText("Timings activated!")

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

        if action == "Reminder with Shutdown":
            msg = QMessageBox()
            # Apply a custom stylesheet to make the popup dark
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #000000;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                }
                QMessageBox QPushButton {
                    background-color: #0059b3;
                    color: #ffffff;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #00478f;
                }
            """)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Time Alert")
            msg.setText("You are late! Shutting down in 30 seconds.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            subprocess.run(["shutdown", "/s", "/t", "30"])
        elif action == "Reminder with Sleep":
            self.status.setText("Going to sleep...")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            self.status.setText("Azan played. No further action taken.")
