from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox, QFileDialog, QMessageBox

class CodeGenTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Multi-language Code Generation"))
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Python", "JavaScript", "Go", "Java", "C#"])
        layout.addWidget(self.language_selector)
        self.code_edit = QTextEdit()
        layout.addWidget(self.code_edit)
        self.generate_btn = QPushButton("Generate Code")
        self.generate_btn.clicked.connect(self.generate_code)
        layout.addWidget(self.generate_btn)
        self.export_btn = QPushButton("Export Code")
        self.export_btn.clicked.connect(self.export_code)
        layout.addWidget(self.export_btn)
        self.setLayout(layout)
    def generate_code(self):
        import requests
        lang = self.language_selector.currentText()
        # Example payload, could be extended with UI fields for method, url, body
        payload = {
            "language": lang,
            "method": "GET",
            "url": "https://api.example.com",
            "body": "{}"
        }
        try:
            resp = requests.post("http://localhost:8000/codegen", json=payload, timeout=10)
            resp.raise_for_status()
            code = resp.json().get("code", "")
            self.code_edit.setText(code)
            QMessageBox.information(self, "Code Generation", f"{lang} code generated.")
        except Exception as e:
            self.code_edit.setText("")
            QMessageBox.critical(self, "Code Generation Error", f"Failed to generate code: {e}")
    def export_code(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Code", "code.txt")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(self.code_edit.toPlainText())
            QMessageBox.information(self, "Export", f"Code exported to {fname}.")
