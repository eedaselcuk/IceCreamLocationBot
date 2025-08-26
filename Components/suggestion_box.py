from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont


class SuggestionBox(QWidget):
    def __init__(self, text="Sweet suggestion box 💡"):
        super().__init__()

        self.label = QLabel(text)
        self.label.setFont(QFont("Arial", 11))
        self.label.setWordWrap(True)
        # Style for the suggestion box
        self.label.setStyleSheet("""
            QLabel {
                background-color: #FFE4E1;
                border: 1px solid #FFB6C1;
                border-radius: 12px;
                padding: 10px;
                color: #444;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
