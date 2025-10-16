from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class AccessibilityTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Accessibility & i18n"))
        self.high_contrast_btn = QPushButton("Toggle High Contrast")
        self.high_contrast_btn.setCheckable(True)
        self.high_contrast_btn.clicked.connect(self.toggle_contrast)
        layout.addWidget(self.high_contrast_btn)
        self.language_btn = QPushButton("Change Language")
        self.language_btn.clicked.connect(self.change_language)
        layout.addWidget(self.language_btn)
        self.setLayout(layout)
    def toggle_contrast(self):
        if self.high_contrast_btn.isChecked():
            QMessageBox.information(self, "Accessibility", "High contrast mode enabled.")
        else:
            QMessageBox.information(self, "Accessibility", "High contrast mode disabled.")
    def change_language(self):
        import requests
        from PySide6.QtWidgets import QInputDialog
        lang, ok = QInputDialog.getText(self, "Change Language", "Enter language code (en/es):")
        if ok and lang:
            try:
                resp = requests.get(f"http://localhost:8000/i18n/{lang}", timeout=10)
                resp.raise_for_status()
                translations = resp.json()
                # Example: update button texts and label
                self.high_contrast_btn.setText(translations.get("accessibility", "Accessibility"))
                self.language_btn.setText(translations.get("sync", "Sync Now"))
                parent = self.parentWidget()
                # Only update window title if parent is QMainWindow
                from PySide6.QtWidgets import QMainWindow
                if isinstance(parent, QMainWindow):
                    parent.setWindowTitle(translations.get("welcome", "Welcome to SoulFetch!"))
                QMessageBox.information(self, "i18n", f"Language switched to {lang}.")
            except Exception as e:
                QMessageBox.critical(self, "i18n Error", f"Failed to switch language: {e}")
