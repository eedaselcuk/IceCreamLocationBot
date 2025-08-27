
import sys
import os
from dotenv import load_dotenv
import openai
import googlemaps

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from Components.language_selector import LanguageSelector
from localization import texts

 # Load .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_API_KEY")

openai.api_key = OPENAI_API_KEY
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)



class IceCreamBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Location Bot")
        self.setGeometry(300, 300, 500, 600)

        # ...existing code...

        # Language state
        self.current_language = 'tr'  # default

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Language selector (top right, new component)
        self.lang_selector = LanguageSelector(self.current_language, self.set_language, self)
        self.lang_selector.move(self.width() - self.lang_selector.width() - 18, 18)
        self.lang_selector.raise_()
        # Reposition on resize
        self.old_resizeEvent = self.resizeEvent
        def new_resizeEvent(event):
            self.lang_selector.move(self.width() - self.lang_selector.width() - 18, 18)
            if hasattr(self, 'old_resizeEvent'):
                self.old_resizeEvent(event)
        self.resizeEvent = new_resizeEvent

        # Custom title: Ice Cream Bot
        font_path = os.path.join("Assets", "Gluten-VariableFont_slnt,wght.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"
        self.title_label = QLabel()
        self.title_label.setText(texts[self.current_language]['title'])
        self.title_label.setFont(QFont(family, 30, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background: transparent; margin-bottom: 10px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)


        # Add SearchBarWidget before set_language is called
        from Components.search_bar import SearchBarWidget
        self.search_bar_widget = SearchBarWidget(
            self.current_language,
            self.handle_search,
            self.open_place_url,
            self
        )
        self.layout.addWidget(self.search_bar_widget, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

        # Set background image
        self.set_background()


    def set_language(self, lang):
        self.current_language = lang
        self.title_label.setText(texts[self.current_language]['title'])
        self.search_bar_widget.update_language(lang)

    def set_background(self):
        palette = QPalette()
        background_path = os.path.join("Assets", "icbBackground.jpg")
        if os.path.exists(background_path):
            pixmap = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)

    def resizeEvent(self, event):
        """When the window is resized, the background is also rescaled"""
        self.set_background()
        super().resizeEvent(event)

    def handle_search(self):
        query = self.search_bar_widget.input.text().strip()

        if not query:
            self.search_bar_widget.results_list.addItem(texts[self.current_language]['warn_empty'])
            return

        from icecream import ask_openai, find_places
        refined_query = ask_openai(openai, query)

        self.search_bar_widget.results_list.clear()
        self.place_urls = []  # Store the URLs of the results here

        places = find_places(gmaps, texts, self.current_language, refined_query)

        if not places:
            self.search_bar_widget.results_list.addItem(texts[self.current_language]['no_result'])
            return

        # 3. List the first 3 results (only name and address, url is kept hidden)
        for place in places:
            display_text = f"{place['name']} - {place['address']} (⭐ {place['rating']})"
            self.search_bar_widget.results_list.addItem(display_text)
            self.place_urls.append(place['url'])

    def open_place_url(self, item):
        # Open the URL of the clicked place
        import webbrowser
        row = self.search_bar_widget.results_list.row(item)
        if hasattr(self, 'place_urls') and 0 <= row < len(self.place_urls):
            webbrowser.open(self.place_urls[row])

    def ask_openai(self, user_query):
        """
        Reads the prompt from prompt.txt and sends it to OpenAI, filling in the user_query.
        """
        try:
            with open("prompt.txt", "r", encoding="utf-8") as f:
                prompt_template = f.read()
            prompt = prompt_template.replace("{user_query}", user_query)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0
            )
            refined = response["choices"][0]["message"]["content"].strip()
            return refined
        except Exception as e:
            print(f"OpenAI API hatası: {e}")
            return user_query  # fallback

    # ...existing code...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamBot()
    window.show()
    sys.exit(app.exec_())
