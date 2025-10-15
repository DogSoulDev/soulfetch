from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel
import requests

class MockTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mock Endpoint Creator"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("/mock/your-endpoint")
        layout.addWidget(self.path_input)
        self.method_input = QLineEdit()
        self.method_input.setPlaceholderText("GET/POST/PUT/DELETE")
        layout.addWidget(self.method_input)
        self.response_edit = QTextEdit()
        self.response_edit.setPlaceholderText("Mock response body")
        layout.addWidget(self.response_edit)
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Status code (e.g. 200)")
        layout.addWidget(self.status_input)
        self.add_btn = QPushButton("Add Mock Endpoint")
        self.add_btn.clicked.connect(self.add_mock)
        layout.addWidget(self.add_btn)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def add_mock(self):
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
        path = self.path_input.text()
        method = self.method_input.text().upper()
        response = self.response_edit.toPlainText()
        status = int(self.status_input.text() or "200")
        payload = {"path": path, "method": method, "response": response, "status": status}
        try:
            r = requests.post(f"{base_url}/mock", json=payload)
            self.result_label.setText(str(r.json()))
        except Exception as e:
            self.result_label.setText(f"Error: {e}")
