from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class SearchBar(QWidget):
    search_submitted = pyqtSignal(str)

    def __init__(self, placeholder="Search..."):
        super().__init__()

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setFixedHeight(40)
        self.input.setFont(QFont("Arial", 12))
        self.input.returnPressed.connect(self.emit_search_submitted)

        # Tatlı pastel arka plan + yuvarlatılmış köşe
        self.input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FFB6C1;
                border-radius: 15px;
                padding-left: 12px;
                background-color: #FFF0F5;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #FF69B4;
                background-color: #FFFFFF;
            }
        """)

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def emit_search_submitted(self):
        self.search_submitted.emit(self.input.text())
