
import sys
import os
from dotenv import load_dotenv
import openai
import googlemaps
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

# .env dosyasını yükle
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

        # Ana dikey layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Arama barı ve butonunu yatayda ortalanmış şekilde koy
        search_row = QWidget()
        search_row_layout = QHBoxLayout()
        search_row_layout.setContentsMargins(0, 0, 0, 0)
        search_row_layout.setSpacing(0)
        search_row_layout.setAlignment(Qt.AlignCenter)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Bir şehir ve dondurma isteğini yaz (örn: Milano’da dondurma)")
        self.input.setFixedHeight(38)
        self.input.setFixedWidth(320)
        self.input.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; padding: 0 12px; font-size: 16px;")

        self.button = QPushButton("Ara", self)
        self.button.setFixedHeight(38)
        self.button.setFixedWidth(70)
        self.button.setStyleSheet("border-radius: 18px; background-color: #FFB6C1; color: white; font-weight: bold; font-size: 15px;")
        self.button.clicked.connect(self.handle_search)
        self.input.returnPressed.connect(self.handle_search)  # Enter tuşu ile arama

        search_row_layout.addWidget(self.input)
        search_row_layout.addSpacing(10)
        search_row_layout.addWidget(self.button)
        search_row.setLayout(search_row_layout)
        self.layout.addSpacing(30)
        self.layout.addWidget(search_row, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

        # Sonuç listesi (daha estetik ve ortalanmış)
        self.results_list = QListWidget(self)
        self.results_list.setFixedHeight(220)
        self.results_list.setFixedWidth(400)
        self.results_list.setStyleSheet("border-radius: 18px; border: 2px solid #FFD1DC; background: rgba(255,255,255,0.85); font-size: 15px; padding: 10px;")
        self.results_list.itemClicked.connect(self.open_place_url)
        self.layout.addWidget(self.results_list, alignment=Qt.AlignCenter)

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
        self.place_urls = []  # Sonuçların URL'lerini burada tutacağız

        # 1. OpenAI’den kullanıcı isteğini daha net bir formata dönüştür
        refined_query = self.ask_openai(query)

        # 2. Google Maps’te yer ara
        places = self.find_places(refined_query)

        if not places:
            self.results_list.addItem("❌ İlgili bir arama yapınız...")
            return

        # 3. İlk 3 sonucu listele (sadece isim ve adres, url gizli tutulacak)
        for place in places:
            display_text = f"{place['name']} - {place['address']} (⭐ {place['rating']})"
            self.results_list.addItem(display_text)
            self.place_urls.append(place['url'])

    def open_place_url(self, item):
        # Tıklanan mekanın sırasına göre URL'yi bul ve aç
        import webbrowser
        row = self.results_list.row(item)
        if hasattr(self, 'place_urls') and 0 <= row < len(self.place_urls):
            webbrowser.open(self.place_urls[row])

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
