
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

 # Load .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_API_KEY")


# Create OpenAI client for new API
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)



class IceCreamBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Location Bot")
        self.setGeometry(300, 300, 500, 600)

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Custom title: Ice Cream Bot
        font_path = os.path.join("Assets", "Gluten-VariableFont_slnt,wght.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"
        self.title_label = QLabel()
        self.title_label.setText("<span style=\"color:#FF714B;\">ice</span> <span style=\"color:#6A0066;\">cream</span> <span style=\"color:#7ADAA5;\">bot</span>")
        self.title_label.setFont(QFont(family, 30, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background: transparent; margin-bottom: 10px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Add SearchBarWidget (single language, no localization)
        from Components.search_bar import SearchBarWidget
        self.search_bar_widget = SearchBarWidget(
            self.handle_search,
            self.open_place_url,
            self
        )
        self.layout.addWidget(self.search_bar_widget, alignment=Qt.AlignCenter)


        self.setLayout(self.layout)
        self.set_background()


    def set_language(self, lang):
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
        self.search_bar_widget.results_list.clear()
        self.place_urls = []

        if not query:
            self.search_bar_widget.results_list.addItem("⚠️ Please enter a search.")
            return

        from icecream import ask_openai
        try:
            ai_response = ask_openai(openai_client, query)
            self.search_bar_widget.results_list.addItem(ai_response)

            # Prompt yanıtından maps_query çıkar, linki ayrı satır olarak ekle
            import re
            maps_query = None
            # 1. Tırnak içinde aramaya çalış
            output_match = re.search(r'"([^"]+)"|“([^”]+)”', ai_response)
            if output_match:
                maps_query = output_match.group(1) or output_match.group(2)
            # 2. "Here is the place you asking for : ..." veya benzeri bir yapı varsa onu al
            if not maps_query:
                colon_match = re.search(r':\s*(.+)$', ai_response)
                if colon_match:
                    maps_query = colon_match.group(1).strip()
            # 3. Hala bulamazsa, yanıtın tamamını maps_query olarak kullan (örnek: "best bakery Napoli")
            if not maps_query and len(ai_response.split()) <= 6:
                maps_query = ai_response.strip()
            # maps_query bulunduysa Google Maps linki oluştur (sadece ayrı satır olarak)
            if maps_query:
                from PyQt5.QtWidgets import QListWidgetItem
                gmaps_url = f"https://www.google.com/maps/search/{maps_query.replace(' ', '+')}"
                item = QListWidgetItem(f"🔗 Google Maps: {gmaps_url}")
                item.setData(Qt.UserRole, gmaps_url)
                self.search_bar_widget.results_list.addItem(item)
        except Exception as e:
            self.search_bar_widget.results_list.addItem(f"❌ Error: {e}")

    def open_place_url(self, item):
        # Sadece Google Maps link satırına tıklanınca işlem yap
        from PyQt5.QtWidgets import QApplication, QLabel
        from PyQt5.QtCore import Qt, QTimer
        import webbrowser
        link = item.data(Qt.UserRole)
        if link:
            # Panoya kopyala
            clipboard = QApplication.clipboard()
            clipboard.setText(link)
            # Tarayıcıda aç
            webbrowser.open(link)
            # Küçük bir hint popup göster (2 sn)
            hint = QLabel("Link copied!")
            hint.setWindowFlags(Qt.ToolTip)
            hint.setStyleSheet("background-color: #222; color: #fff; font-size: 16px; padding: 10px; border-radius: 8px;")
            hint.setAlignment(Qt.AlignCenter)
            hint.setFixedWidth(180)
            hint.move(self.geometry().center().x() - 90, self.geometry().center().y() - 30)
            hint.setParent(self)
            hint.show()
            QTimer.singleShot(2000, hint.close)

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
