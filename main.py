
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

        # Place the search bar and button horizontally centered
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
        self.button.setStyleSheet("border-radius: 18px; background-color: #FFB6C1; color: white; font-weight: bold; font-size: 15px;")
        self.button.clicked.connect(self.handle_search)
        self.input.returnPressed.connect(self.handle_search)  # Search with Enter key

        search_row_layout.addWidget(self.input)
        search_row_layout.addSpacing(10)
        search_row_layout.addWidget(self.button)
        search_row.setLayout(search_row_layout)
        self.layout.addSpacing(30)
        self.layout.addWidget(search_row, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

        # Results list (more aesthetic and centered)
        self.results_list = QListWidget(self)
        self.results_list.setFixedHeight(220)
        self.results_list.setFixedWidth(400)
        self.results_list.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; background: rgba(255,255,255,0.85); font-size: 15px; padding: 10px;")
        self.results_list.itemClicked.connect(self.open_place_url)
        self.layout.addWidget(self.results_list, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        # Set background image
        self.set_background()

        # Set initial language after all UI is ready
        self.set_language(self.current_language)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Location Bot")
        self.setGeometry(300, 300, 500, 600)

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

        # Place the search bar and button horizontally centered
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
        self.button.setStyleSheet("border-radius: 18px; background-color: #FFB6C1; color: white; font-weight: bold; font-size: 15px;")
        self.button.clicked.connect(self.handle_search)
        self.input.returnPressed.connect(self.handle_search)  # Search with Enter key

        search_row_layout.addWidget(self.input)
        search_row_layout.addSpacing(10)
        search_row_layout.addWidget(self.button)
        search_row.setLayout(search_row_layout)
        self.layout.addSpacing(30)
        self.layout.addWidget(search_row, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

        # Results list (more aesthetic and centered)
        self.results_list = QListWidget(self)
        self.results_list.setFixedHeight(220)
        self.results_list.setFixedWidth(400)
        self.results_list.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; background: rgba(255,255,255,0.85); font-size: 15px; padding: 10px;")
        self.results_list.itemClicked.connect(self.open_place_url)
        self.layout.addWidget(self.results_list, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        # Set background image
        self.set_background()


    def set_language(self, lang):
        self.current_language = lang
        self.title_label.setText(texts[self.current_language]['title'])
        self.input.setPlaceholderText(texts[self.current_language]['placeholder'])
        self.button.setText(texts[self.current_language]['search'])

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
        query = self.input.text().strip()

        if not query:
            self.results_list.addItem(texts[self.current_language]['warn_empty'])
            return

        self.results_list.clear()
        self.place_urls = []  # Store the URLs of the results here

        # 1. Refine the user's request with OpenAI
        refined_query = self.ask_openai(query)

        # 2. Search for places on Google Maps
        places = self.find_places(refined_query)

        if not places:
            self.results_list.addItem(texts[self.current_language]['no_result'])
            return

        # 3. List the first 3 results (only name and address, url is kept hidden)
        for place in places:
            display_text = f"{place['name']} - {place['address']} (⭐ {place['rating']})"
            self.results_list.addItem(display_text)
            self.place_urls.append(place['url'])

    def open_place_url(self, item):
        # Open the URL of the clicked place
        import webbrowser
        row = self.results_list.row(item)
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

    def find_places(self, query):
        """
        Searches for cafes, bakeries, ice cream shops, and patisseries on Google Maps, using search_types from localization.py for filtering.
        If no results are found in the current language, tries the alternative language's search_types as fallback.
        """
        try:
            # Convert city name to coordinates
            geocode = gmaps.geocode(query)
            if not geocode:
                return []

            location = geocode[0]["geometry"]["location"]
            latlng = (location["lat"], location["lng"])

            # Supported types
            allowed_types = ["cafe", "bakery", "restaurant"]

            def get_places(search_types, lang_code):
                found = []
                for place_type in allowed_types:
                    results = gmaps.places_nearby(
                        location=latlng,
                        radius=5000,  # 5 km
                        type=place_type,
                        language=lang_code
                    )
                    for place in results.get("results", []):
                        name = place.get("name", "").lower()
                        if any(word in name for word in search_types):
                            address = place.get("vicinity", "")
                            rating = place.get("rating", "N/A")
                            url = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                            found.append({
                                "name": place.get("name", ""),
                                "address": address,
                                "rating": rating,
                                "url": url
                            })
                return found

            # Try current language search_types first
            search_types = [s.lower() for s in texts[self.current_language].get('search_types', [])]
            lang_code = self.current_language if self.current_language == 'tr' else 'en'
            places = get_places(search_types, lang_code)

            # If no results, try the other language's search_types as fallback
            if not places:
                alt_lang = 'en' if self.current_language == 'tr' else 'tr'
                alt_search_types = [s.lower() for s in texts[alt_lang].get('search_types', [])]
                alt_lang_code = alt_lang if alt_lang == 'tr' else 'en'
                places = get_places(alt_search_types, alt_lang_code)

            return places[:3]

        except Exception as e:
            print(f"mistakes by Google Maps API: {e}")
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamBot()
    window.show()
    sys.exit(app.exec_())
