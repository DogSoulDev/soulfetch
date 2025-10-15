from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView

class GeminiTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.webview.setUrl("https://gemini.google.com/app")
        self.webview.loadFinished.connect(self.handle_load)
        layout.addWidget(self.webview, stretch=1)
        self.setLayout(layout)
        self.setMinimumSize(600, 400)

    def handle_load(self, ok):
        from PySide6.QtWidgets import QMessageBox
        if not ok:
            QMessageBox.critical(self, "Error", "No se pudo cargar Gemini. Verifica tu conexión o permisos de WebEngine.")
