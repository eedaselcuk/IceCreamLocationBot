from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont


class SweetButton(QPushButton):
    def __init__(self, text="Click Me!"):
        super().__init__(text)

        self.setFont(QFont("Arial", 12, QFont.Bold))
        self.setFixedHeight(40)

        self.setStyleSheet("""
            QPushButton {
                background-color: #FFB6C1;
                border: none;
                border-radius: 15px;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #FF69B4;
            }
            QPushButton:pressed {
                background-color: #DB7093;
            }
        """)
