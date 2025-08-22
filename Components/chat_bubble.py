from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ChatBubble(QWidget):
    def __init__(self, text="Merhaba 👋", is_user=True, parent=None):
        super().__init__(parent)

        self.label = QLabel(text)
        self.label.setFont(QFont("Arial", 11))
        self.label.setWordWrap(True)
        # Optional: make text selectable
        # self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_user:
            self.label.setStyleSheet("""
                background-color: #FFB6C1;
                color: white;
                border-radius: 12px;
                padding: 10px;
            """)
            alignment = Qt.AlignRight
        else:
            self.label.setStyleSheet("""
                background-color: #E6E6FA;
                color: #333;
                border-radius: 12px;
                padding: 10px;
            """)
            alignment = Qt.AlignLeft

        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=alignment)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
