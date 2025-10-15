from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFormLayout, QMessageBox
from PySide6.QtCore import Signal
import sqlite3, json, base64

class AuthTab(QWidget):
    auth_config_changed = Signal(dict)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Autenticación avanzada"))
        form = QFormLayout()
        self.auth_type = QComboBox()
        self.auth_type.addItems(["API Key", "OAuth 2.0", "JWT", "Custom Header"])
        self.auth_type.currentTextChanged.connect(self.update_form)
        form.addRow("Tipo de autenticación:", self.auth_type)
        self.api_key = QLineEdit()
        form.addRow("API Key:", self.api_key)
        self.jwt_payload = QTextEdit()
        self.jwt_secret = QLineEdit()
        self.jwt_algo = QLineEdit()
        self.oauth_client_id = QLineEdit()
        self.oauth_client_secret = QLineEdit()
        self.oauth_scope = QLineEdit()
        self.oauth_redirect = QLineEdit()
        self.custom_header = QLineEdit()
        self.save_btn = QPushButton("Guardar configuración")
        self.save_btn.clicked.connect(self.save_auth)
        layout.addLayout(form)
        layout.addWidget(self.save_btn)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        self.setLayout(layout)
        self.update_form(self.auth_type.currentText())

    def update_form(self, auth_type):
        # Oculta todos los campos
        self.api_key.hide()
        self.jwt_payload.hide()
        self.jwt_secret.hide()
        self.jwt_algo.hide()
        self.oauth_client_id.hide()
        self.oauth_client_secret.hide()
        self.oauth_scope.hide()
        self.oauth_redirect.hide()
        self.custom_header.hide()
        if auth_type == "API Key":
            self.api_key.show()
        elif auth_type == "JWT":
            self.jwt_payload.show()
            self.jwt_secret.show()
            self.jwt_algo.show()
        elif auth_type == "OAuth 2.0":
            self.oauth_client_id.show()
            self.oauth_client_secret.show()
            self.oauth_scope.show()
            self.oauth_redirect.show()
        elif auth_type == "Custom Header":
            self.custom_header.show()

    def save_auth(self):
        auth_type = self.auth_type.currentText()
        data = {"type": auth_type}
        if auth_type == "API Key":
            data["api_key"] = self.api_key.text()
        elif auth_type == "JWT":
            data["payload"] = self.jwt_payload.toPlainText()
            data["secret"] = self.jwt_secret.text()
            data["algo"] = self.jwt_algo.text()
        elif auth_type == "OAuth 2.0":
            data["client_id"] = self.oauth_client_id.text()
            data["client_secret"] = self.oauth_client_secret.text()
            data["scope"] = self.oauth_scope.text()
            data["redirect_uri"] = self.oauth_redirect.text()
        elif auth_type == "Custom Header":
            data["header"] = self.custom_header.text()
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS auth_configs (id INTEGER PRIMARY KEY, config TEXT)')
        c.execute('INSERT OR REPLACE INTO auth_configs (id, config) VALUES (?, ?)', (1, json.dumps(data)))
        conn.commit()
        conn.close()
        self.result_label.setText("Configuración de autenticación guardada.")
        self.auth_config_changed.emit(data)

    def get_auth_config(self):
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS auth_configs (id INTEGER PRIMARY KEY, config TEXT)')
        row = c.execute('SELECT config FROM auth_configs WHERE id=1').fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None

    def generate_jwt(self, payload, secret, algo):
        import hmac, hashlib, json, base64
        header = {"alg": algo, "typ": "JWT"}
        def b64url(data):
            return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b'=').decode()
        segments = [b64url(header), b64url(json.loads(payload))]
        signing_input = '.'.join(segments)
        if algo == "HS256":
            sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
        else:
            sig = b''
        segments.append(base64.urlsafe_b64encode(sig).rstrip(b'=').decode())
        return '.'.join(segments)
