from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class SearchBar(QWidget):
    search_submitted = pyqtSignal(str)

    def __init__(self, placeholder="Search..."):
        super().__init__()

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setFixedHeight(56)
        self.input.setFont(QFont("Comic Sans MS", 18))
        self.input.returnPressed.connect(self.emit_search_submitted)

        # Görsele uygun pastel ve yuvarlatılmış stil
        self.input.setStyleSheet("""
            QLineEdit {
                border: 4px solid #FFD1DC;
                border-radius: 32px;
                padding-left: 24px;
                padding-right: 48px;
                background-color: #FFF8FB;
                color: #444;
                font-size: 20px;
            }
            QLineEdit:focus {
                border: 4px solid #FFB6C1;
                background-color: #FFFFFF;
            }
        """)

        # Sağda büyüteç ikonu
        self.icon = QLabel()
        pixmap = QPixmap("Assets/search_icon.png")  # search_icon.png dosyasını Assets klasörüne ekleyin
        if not pixmap.isNull():
            self.icon.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon.setFixedSize(40, 40)
        self.icon.setStyleSheet("background: transparent; margin-left: -44px;")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.input)
        layout.addWidget(self.icon)
        self.setLayout(layout)

    def emit_search_submitted(self):
        self.search_submitted.emit(self.input.text())
