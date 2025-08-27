from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QFontDatabase, QFont, QCursor
from PyQt5.QtCore import Qt
import os

class LanguageSelector(QWidget):
    def __init__(self, current_language, callback, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(48)
        self.setFixedWidth(140)
        self.setStyleSheet('background: transparent;')
        self.callback = callback
        self.current_language = current_language

        # Load custom font
        font_path = os.path.join('Assets', 'Gluten-VariableFont_slnt,wght.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path) if font_path else -1
        family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"
        lang_font = QFont(family, 14, QFont.Bold)

        lang_layout = QHBoxLayout()
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(0)  # No extra spacing between widgets

        self.tr_label = QLabel('TR', self)
        self.tr_label.setFont(lang_font)
        self.tr_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.tr_label.setStyleSheet('color: #F5275B; padding: 0 4px;')
        self.tr_label.mousePressEvent = lambda e: self.set_language('tr')

        self.eng_label = QLabel('ENG', self)
        self.eng_label.setFont(lang_font)
        self.eng_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.eng_label.setStyleSheet('color: #F5275B; padding: 0 4px;')
        self.eng_label.mousePressEvent = lambda e: self.set_language('en')

        lang_layout.addWidget(self.tr_label)
        lang_layout.addWidget(self.eng_label)
        self.setLayout(lang_layout)

    def set_language(self, lang):
        self.current_language = lang
        if lang == 'tr':
            self.tr_label.setStyleSheet('color: #C227F5; background: #F6F6F6; border-radius: 10px; padding: 0 8px;')
            self.eng_label.setStyleSheet('color: #C227F5; background: transparent; padding: 0 8px;')
        else:
            self.tr_label.setStyleSheet('color: #C227F5; background: transparent; padding: 0 8px;')
            self.eng_label.setStyleSheet('color: #C227F5; background: #F6F6F6; border-radius: 10px; padding: 0 8px;')
        if self.callback:
            self.callback(lang)
