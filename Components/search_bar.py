from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from localization import texts

class SearchBarWidget(QWidget):
	def __init__(self, current_language, search_callback, open_url_callback, parent=None):
		super().__init__(parent)
		self.current_language = current_language
		self.search_callback = search_callback
		self.open_url_callback = open_url_callback

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignCenter)

		# Search bar and button row
		search_row = QWidget()
		search_row_layout = QHBoxLayout()
		search_row_layout.setContentsMargins(0, 0, 0, 0)
		search_row_layout.setSpacing(0)
		search_row_layout.setAlignment(Qt.AlignCenter)

		self.input = QLineEdit(self)
		self.input.setPlaceholderText(texts[self.current_language]['placeholder'])
		self.input.setFixedHeight(38)
		self.input.setFixedWidth(320)
		self.input.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; padding: 0 12px; font-size: 16px;")

		self.button = QPushButton(texts[self.current_language]['search'], self)
		self.button.setFixedHeight(38)
		self.button.setFixedWidth(70)
		self.button.setStyleSheet("""
			QPushButton {
				border-radius: 18px;
				background-color: #B6FFF4;
				color: white;
				font-weight: bold;
				font-size: 15px;
			}
			QPushButton:hover {
				background-color: #FFB6C1;
			}
		""")

		search_row_layout.addWidget(self.input)
		search_row_layout.addSpacing(10)
		search_row_layout.addWidget(self.button)
		search_row.setLayout(search_row_layout)
		layout.addSpacing(30)
		layout.addWidget(search_row, alignment=Qt.AlignCenter)
		layout.addSpacing(20)

		# Results list
		self.results_list = QListWidget(self)
		self.results_list.setFixedHeight(220)
		self.results_list.setFixedWidth(600)
		self.results_list.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; background: rgba(255,255,255,0.85); font-size: 15px; padding: 10px;")
		self.results_list.itemClicked.connect(self.open_url_callback)
		layout.addWidget(self.results_list, alignment=Qt.AlignCenter)
		self.setLayout(layout)
		self.button.clicked.connect(self.search_callback)
		self.input.returnPressed.connect(self.search_callback)

	# Remove any code outside __init__

	def update_language(self, lang):
		self.current_language = lang
		self.input.setPlaceholderText(texts[self.current_language]['placeholder'])
		self.button.setText(texts[self.current_language]['search'])
