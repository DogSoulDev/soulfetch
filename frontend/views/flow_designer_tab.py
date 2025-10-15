from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QTextEdit
from PySide6.QtCore import Qt

class FlowDesignerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("API Flow Designer"))
        self.flow_list = QListWidget()
        layout.addWidget(self.flow_list)
        self.add_step_btn = QPushButton("Add Step")
        self.add_step_btn.clicked.connect(self.add_step)
        layout.addWidget(self.add_step_btn)
        self.step_method = QLineEdit()
        self.step_method.setPlaceholderText("Method (GET/POST)")
        layout.addWidget(self.step_method)
        self.step_url = QLineEdit()
        self.step_url.setPlaceholderText("URL")
        layout.addWidget(self.step_url)
        self.step_body = QTextEdit()
        self.step_body.setPlaceholderText("Body (optional)")
        layout.addWidget(self.step_body)
        self.run_flow_btn = QPushButton("Run Flow")
        self.run_flow_btn.clicked.connect(self.run_flow)
        layout.addWidget(self.run_flow_btn)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        self.setLayout(layout)
        self.steps = []

    def add_step(self):
        method = self.step_method.text().upper()
        url = self.step_url.text()
        body = self.step_body.toPlainText()
        self.steps.append((method, url, body))
        self.flow_list.addItem(f"{method} {url}")
        self.step_method.clear()
        self.step_url.clear()
        self.step_body.clear()

    def set_env_vars(self, env_vars):
        self._env_vars = env_vars
    def set_auth_config(self, auth_config):
        self._auth_config = auth_config
    def run_flow(self):
        import requests, os
        base_url = os.getenv("SOULFETCH_API_URL", "")
        results = []
        for method, url, body in self.steps:
            # Aplicar variables de entorno
            if hasattr(self, '_env_vars') and self._env_vars:
                for k, v in self._env_vars.items():
                    url = url.replace(f'{{{{{k}}}}}', v)
                    body = body.replace(f'{{{{{k}}}}}', v)
            headers = {}
            # Aplicar autenticación
            if hasattr(self, '_auth_config') and self._auth_config:
                if self._auth_config.get('type') == 'API Key':
                    headers['X-Api-Key'] = self._auth_config.get('api_key', '')
                elif self._auth_config.get('type') == 'JWT':
                    headers['Authorization'] = f"Bearer {self._auth_config.get('payload','')}"
                elif self._auth_config.get('type') == 'OAuth 2.0':
                    headers['Authorization'] = f"Bearer {self._auth_config.get('client_secret','')}"
                elif self._auth_config.get('type') == 'Custom Header':
                    headers[self._auth_config.get('header','')] = self._auth_config.get('value','')
            # If url is relative, prepend base_url
            if base_url and url.startswith("/"):
                url = base_url + url
            try:
                if method == "GET":
                    r = requests.get(url, headers=headers)
                else:
                    r = requests.request(method, url, data=body, headers=headers)
                results.append(f"{method} {url}: {r.status_code}")
            except Exception as e:
                results.append(f"{method} {url}: Error {e}")
        self.result_label.setText("\n".join(results))
