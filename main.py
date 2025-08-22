import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox
from Components.search_bar import SearchBar
from Components.chat_bubble import ChatBubble

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IceCream Desktop Bot")
        self.setGeometry(100, 100, 400, 500)

        self.setStyleSheet("""
            QMainWindow {
                background-image: url('Assets/background.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Search bar with improved prompt
        self.search_bar = SearchBar(
            placeholder="Bir tatlıcı, pastane, fırın veya dondurmacı arayın (örn: 'Yakındaki pastaneler')"
        )
        self.search_bar.search_submitted.connect(self.handle_search)
        self.layout.addWidget(self.search_bar)

        # Chat area
        self.chat_area = QVBoxLayout()
        self.layout.addLayout(self.chat_area)

        # Initial greeting
        self.add_bot_message("Merhaba! Size yakın tatlıcı, pastane, fırın veya dondurmacı bulmamı ister misiniz? Lütfen ne aradığınızı yazın.")

    def add_bot_message(self, text):
        bubble = ChatBubble(text, is_user=False)
        self.chat_area.addWidget(bubble)

    def add_user_message(self, text):
        bubble = ChatBubble(text, is_user=True)
        self.chat_area.addWidget(bubble)

    def handle_search(self, query):
        self.add_user_message(query)
        if not any(word in query.lower() for word in ["tatlıcı", "pastane", "fırın", "dondurmacı", "bakery", "patisserie", "dessert", "ice cream"]):
            self.add_bot_message("Lütfen bir tatlıcı, pastane, fırın veya dondurmacı aradığınızı belirtin.")
            return

        # Placeholder for actual search logic
        try:
            results = self.find_places(query)
            if results:
                for place in results:
                    self.add_bot_message(f"{place['name']} - {place['address']}")
            else:
                self.add_bot_message("Üzgünüm, aradığınız kriterlere uygun bir yer bulamadım.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")

    def find_places(self, query):
        # TODO: Replace with actual API call or search logic
        return [
            {"name": "Örnek Dondurmacı", "address": "Örnek Cad. No:1"},
            {"name": "Lezzetli Pastane", "address": "Tatlı Sok. No:2"}
        ]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
