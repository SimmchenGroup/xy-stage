import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XY Stage Control")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Example Controls
        self.status_label = QLabel("Status: Disconnected")
        layout.addWidget(self.status_label)

        # Command input and send button
        command_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command e.g. X+100")
        command_layout.addWidget(self.command_input)
        self.send_button = QPushButton("Send Command")
        command_layout.addWidget(self.send_button)

        layout.addLayout(command_layout)

        self.setLayout(layout)

        # Connect button signal to a slot
        self.send_button.clicked.connect(self.send_command)

    def send_command(self):
        command = self.command_input.text()
        # For now just print command to console
        print(f"Command sent: {command}")
        self.status_label.setText(f"Last command: {command}")
        self.command_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
