import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QListWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from Components.search_bar import SearchBar

import os
from dotenv import load_dotenv
import googlemaps
import openai

# .env dosyasından API anahtarlarını yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
openai.api_key = OPENAI_API_KEY
if not openai.api_key:
    print("OpenAI API anahtarı bulunamadı!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Bot")
        self.setGeometry(100, 100, 900, 600)

        # Arka planı icbBackground.jpg olarak ayarla
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(Assets/icbBackground.jpg);
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Başlık (Ice Cream Bot)
        self.title_label = QLabel("Ice Cream Bot")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-family: 'Comic Sans MS', 'Comic Neue', Arial, sans-serif;
                color: #FF69B4;
                font-weight: bold;
                margin-top: 60px;
                margin-bottom: 30px;
                background: transparent;
                letter-spacing: 2px;
                text-shadow: 2px 2px 8px #fff;
            }
        """)
        self.layout.addWidget(self.title_label)

        # Ortada arama barı (SearchBar)
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout()
        search_bar_layout.setContentsMargins(0, 0, 0, 0)
        search_bar_layout.setSpacing(0)
        search_bar_container.setLayout(search_bar_layout)
        search_bar_container.setFixedHeight(80)
        search_bar_container.setStyleSheet("background: transparent;")

        self.search_bar = SearchBar(
            placeholder="Bir tatlıcı, pastane, fırın veya dondurmacı arayın"
        )
        self.search_bar.setFixedHeight(56)
        self.search_bar.setFixedWidth(500)
        self.search_bar.search_submitted.connect(self.handle_search)
        search_bar_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        search_bar_layout.addWidget(self.search_bar)
        search_bar_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addWidget(search_bar_container)

        # Sonuç kutusu (ortalanmış, transparan)
        self.results_list = QListWidget()
        self.results_list.setMinimumHeight(200)
        self.results_list.setMaximumHeight(350)
        self.results_list.setFixedWidth(500)
        self.results_list.setStyleSheet("""
            QListWidget {
                background: rgba(255,255,255,0.7);
                border: 2px solid #FFD1DC;
                border-radius: 24px;
                color: #444;
                font-size: 16px;
                font-family: 'Comic Sans MS', 'Comic Neue', Arial, sans-serif;
                padding: 18px;
                margin-top: 24px;
            }
            QListWidget::item {
                padding: 10px 6px;
            }
        """)
        results_container = QWidget()
        results_layout = QHBoxLayout()
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        results_layout.addWidget(self.results_list)
        results_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        results_container.setLayout(results_layout)
        self.layout.addWidget(results_container)

        self.layout.addStretch()

    def handle_search(self, query):
        self.results_list.clear()
        self.results_list.addItem("Yanıt bekleniyor...")

        try:
            # 1. OpenAI API'ye soruyu gönder
            openai_response = self.ask_openai(query)
            if not openai_response:
                self.results_list.clear()
                self.results_list.addItem("OpenAI'dan yanıt alınamadı. Lütfen terminaldeki hata mesajını kontrol edin.")
                return

            # 2. OpenAI yanıtını Google Maps aramasında kullan
            places = self.find_places(openai_response)
            self.results_list.clear()
            if places:
                for place in places:
                    self.results_list.addItem(f"{place['name']} - {place['address']}")
            else:
                self.results_list.addItem("Üzgünüm, aradığınız kriterlere uygun bir yer bulamadım.")
        except Exception as e:
            self.results_list.clear()
            self.results_list.addItem(f"Hata oluştu: {e}")

    def ask_openai(self, user_query):
        """
        Kullanıcıdan gelen soruyu OpenAI API'ye gönderir ve yanıtı döndürür.
        Yanıtı, Google Maps aramasında kullanılacak şekilde sadeleştirir.
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Kullanıcıdan gelen arama cümlesini, Google Maps'te yer araması için uygun kısa bir anahtar kelimeye veya kategoriye dönüştür. Sadece anahtar kelime veya kategori döndür (ör: 'dondurmacı', 'pastane', 'bakery', 'ice cream shop')."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=16,
                temperature=0
            )
            # openai>=1.0.0 için:
            result = response.choices[0].message.content.strip()
            return result
        except Exception as e:
            print(f"OpenAI API hatası: {e}")
            return None

    def find_places(self, query):
        # Google Maps Places API ile arama yap
        try:
            # Türkiye merkezli arama için örnek bir konum (Ankara)
            location = (39.9334, 32.8597)
            results = gmaps.places(
                query=query,
                location=location,
                radius=10000,  # 10 km yarıçap
                language="tr"
            )
            places = []
            for place in results.get("results", []):
                name = place.get("name", "")
                address = place.get("formatted_address") or place.get("vicinity", "")
                places.append({"name": name, "address": address})
            return places
        except Exception as e:
            print(f"Google Maps API hatası: {e}")
            return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
