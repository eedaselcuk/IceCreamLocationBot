import sys
import os
import openai
import googlemaps
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

# API key'lerini ortam değişkeninden oku
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

openai.api_key = OPENAI_API_KEY
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


class IceCreamBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Location Bot")
        self.setGeometry(300, 300, 500, 600)

        # Layout
        self.layout = QVBoxLayout()

        # Input alanı
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Bir şehir ve dondurma isteğini yaz (örn: Milano’da dondurma)")
        self.layout.addWidget(self.input)

        # Buton
        self.button = QPushButton("Ara", self)
        self.button.clicked.connect(self.handle_search)
        self.layout.addWidget(self.button)

        # Sonuç listesi
        self.results_list = QListWidget(self)
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

        # Arkaplan resmi ayarla
        self.set_background()

    def set_background(self):
        palette = QPalette()
        background_path = os.path.join("Assets", "icbBackground.jpg")
        if os.path.exists(background_path):
            pixmap = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)

    def resizeEvent(self, event):
        """Pencere yeniden boyutlanınca arkaplan da yeniden ölçeklensin"""
        self.set_background()
        super().resizeEvent(event)

    def handle_search(self):
        query = self.input.text().strip()
        if not query:
            self.results_list.addItem("⚠️ Lütfen bir arama giriniz.")
            return

        self.results_list.clear()

        # 1. OpenAI’den kullanıcı isteğini daha net bir formata dönüştür
        refined_query = self.ask_openai(query)

        # 2. Google Maps’te yer ara
        places = self.find_places(refined_query)

        if not places:
            self.results_list.addItem("❌ Sonuç bulunamadı.")
            return

        # 3. İlk 3 sonucu listele
        for place in places:
            self.results_list.addItem(
                f"{place['name']} - {place['address']} (⭐ {place['rating']})\n{place['url']}\n"
            )

    def ask_openai(self, user_query):
        """
        Kullanıcının sorusunu basit hale getirip sadece şehir + dondurma gibi bir query üretmesi için.
        """
        try:
            prompt = f"""
            Kullanıcı şu isteği yazdı: "{user_query}".
            Bunu Google Maps araması için basit hale getir. Sadece şehir adı ve 'dondurma' kelimesini döndür.
            Örn: 'Milano dondurma'
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen bir yardımcı asistanısın."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0
            )
            refined = response["choices"][0]["message"]["content"].strip()
            return refined
        except Exception as e:
            print(f"OpenAI API hatası: {e}")
            return user_query  # fallback

    def find_places(self, query):
        """
        Google Maps üzerinde query’ye göre mekan arar, ilk 3 sonucu döndürür.
        """
        try:
            # Şehir ismini koordinata çevir
            geocode = gmaps.geocode(query)
            if not geocode:
                return []

            location = geocode[0]["geometry"]["location"]
            latlng = (location["lat"], location["lng"])

            # Places API çağrısı
            results = gmaps.places(
                query=query,
                location=latlng,
                radius=10000,
                language="tr"
            )

            places = []
            for place in results.get("results", [])[:3]:  # sadece ilk 3
                name = place.get("name", "")
                address = place.get("formatted_address") or place.get("vicinity", "")
                rating = place.get("rating", "N/A")
                url = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                places.append({
                    "name": name,
                    "address": address,
                    "rating": rating,
                    "url": url
                })
            return places
        except Exception as e:
            print(f"Google Maps API hatası: {e}")
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamBot()
    window.show()
    sys.exit(app.exec_())
