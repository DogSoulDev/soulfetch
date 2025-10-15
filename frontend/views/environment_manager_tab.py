from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QFileDialog
from PySide6.QtCore import Signal
import sqlite3, base64

class EnvironmentManagerTab(QWidget):
    environment_switched = Signal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Environment Manager"))
        self.env_combo = QComboBox()
        self.load_environments()
        layout.addWidget(self.env_combo)
        self.var_edit = QTextEdit()
        self.var_edit.setPlaceholderText("key1=value1;key2=value2")
        layout.addWidget(self.var_edit)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Environment")
        self.save_btn.clicked.connect(self.save_environment)
        btn_layout.addWidget(self.save_btn)
        self.switch_btn = QPushButton("Switch Environment")
        self.switch_btn.clicked.connect(self.switch_environment)
        btn_layout.addWidget(self.switch_btn)
        self.encrypt_btn = QPushButton("Encrypt (base64)")
        self.encrypt_btn.clicked.connect(self.encrypt_variables)
        btn_layout.addWidget(self.encrypt_btn)
        self.xor_btn = QPushButton("Encrypt (XOR)")
        self.xor_btn.clicked.connect(self.xor_encrypt_variables)
        btn_layout.addWidget(self.xor_btn)
        self.decrypt_btn = QPushButton("Decrypt (base64)")
        self.decrypt_btn.clicked.connect(self.decrypt_variables)
        btn_layout.addWidget(self.decrypt_btn)
        self.xor_dec_btn = QPushButton("Decrypt (XOR)")
        self.xor_dec_btn.clicked.connect(self.xor_decrypt_variables)
        btn_layout.addWidget(self.xor_dec_btn)
        layout.addLayout(btn_layout)

        btn2_layout = QHBoxLayout()
        self.export_btn = QPushButton("Export Environments")
        self.export_btn.clicked.connect(self.export_environments)
        btn2_layout.addWidget(self.export_btn)
        self.import_btn = QPushButton("Import Environments")
        self.import_btn.clicked.connect(self.import_environments)
        btn2_layout.addWidget(self.import_btn)
        self.copy_btn = QPushButton("Copy Variables")
        self.copy_btn.clicked.connect(self.copy_variables)
        btn2_layout.addWidget(self.copy_btn)
        self.clear_btn = QPushButton("Clear Variables")
        self.clear_btn.clicked.connect(self.clear_variables)
        btn2_layout.addWidget(self.clear_btn)
        self.show_btn = QPushButton("Show/Hide Variables")
        self.show_btn.setCheckable(True)
        self.show_btn.clicked.connect(self.toggle_show_variables)
        btn2_layout.addWidget(self.show_btn)
        layout.addLayout(btn2_layout)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        self.security_label = QLabel()
        layout.addWidget(self.security_label)
        self.var_edit.textChanged.connect(self.validate_variables)
        self.setLayout(layout)

    def load_environments(self):
        self.env_combo.clear()
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS env_vars (env_name TEXT, variables TEXT)')
        rows = c.execute('SELECT env_name FROM env_vars').fetchall()
        conn.close()
        for row in rows:
            self.env_combo.addItem(row[0])

    def save_environment(self):
        name = self.env_combo.currentText() or "default"
        variables = self.var_edit.toPlainText()
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS env_vars (env_name TEXT, variables TEXT)')
        c.execute('INSERT OR REPLACE INTO env_vars (env_name, variables) VALUES (?, ?)', (name, variables))
        conn.commit()
        conn.close()
        self.result_label.setText(f"Saved environment '{name}'")
        self.load_environments()

    def switch_environment(self):
        name = self.env_combo.currentText()
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('SELECT variables FROM env_vars WHERE env_name=?', (name,))
        row = c.fetchone()
        conn.close()
        if row:
            self.var_edit.setText(row[0])
            self.result_label.setText(f"Switched to environment '{name}'")
            self.environment_switched.emit(row[0])
        else:
            self.result_label.setText("Environment not found")

    def encrypt_variables(self):
        text = self.var_edit.toPlainText()
        encrypted = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        self.var_edit.setText(encrypted)
        self.result_label.setText("Variables encrypted (base64)")

    def xor_encrypt_variables(self):
        text = self.var_edit.toPlainText()
        key = "SoulFetchKey"
        encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
        self.var_edit.setText(base64.b64encode(encrypted.encode('utf-8')).decode('utf-8'))
        self.result_label.setText("Variables encrypted (XOR)")

    def xor_decrypt_variables(self):
        text = self.var_edit.toPlainText()
        key = "SoulFetchKey"
        try:
            decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            decrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))
            self.var_edit.setText(decrypted)
            self.result_label.setText("Variables decrypted (XOR)")
        except Exception:
            self.result_label.setText("XOR decryption failed")

    def decrypt_variables(self):
        text = self.var_edit.toPlainText()
        try:
            decrypted = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            self.var_edit.setText(decrypted)
            self.result_label.setText("Variables decrypted")
        except Exception:
            self.result_label.setText("Decryption failed")

    def export_environments(self):
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        rows = c.execute('SELECT env_name, variables FROM env_vars').fetchall()
        conn.close()
        fname, _ = QFileDialog.getSaveFileName(self, "Export Environments", "environments.json", "JSON Files (*.json)")
        if fname:
            import json
            with open(fname, "w", encoding="utf-8") as f:
                json.dump([{"env_name": n, "variables": v} for n, v in rows], f, indent=2)
            self.result_label.setText(f"Exported to {fname}")

    def import_environments(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Import Environments", "", "JSON Files (*.json)")
        if fname:
            import json
            with open(fname, "r", encoding="utf-8") as f:
                data = json.load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS env_vars (env_name TEXT, variables TEXT)')
            for env in data:
                c.execute('INSERT OR REPLACE INTO env_vars (env_name, variables) VALUES (?, ?)', (env["env_name"], env["variables"]))
            conn.commit()
            conn.close()
            self.result_label.setText(f"Imported environments from {fname}")
            self.load_environments()

    def copy_variables(self):
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.clipboard().setText(self.var_edit.toPlainText())
        self.result_label.setText("Variables copied to clipboard")

    def clear_variables(self):
        self.var_edit.clear()
        self.result_label.setText("Variables cleared")

    def toggle_show_variables(self):
        if not hasattr(self, '_hidden_text'):
            self._hidden_text = None
        if self.show_btn.isChecked():
            # Mostrar texto real
            if self._hidden_text is not None:
                self.var_edit.setPlainText(self._hidden_text)
                self._hidden_text = None
            self.result_label.setText("Variables visibles")
        else:
            # Ocultar texto (asteriscos)
            text = self.var_edit.toPlainText()
            self._hidden_text = text
            self.var_edit.setPlainText('*' * len(text))
            self.result_label.setText("Variables ocultas")

    def validate_variables(self):
        text = self.var_edit.toPlainText()
        insecure_keys = ["password", "token", "secret", "apikey", "jwt"]
        found = [k for k in insecure_keys if k in text.lower()]
        if found:
            self.security_label.setText(f"⚠️ Insecure keys detected: {', '.join(found)}")
            self.security_label.setToolTip("Avoid storing sensitive secrets in plaintext. Use encryption and environment separation.")
        else:
            self.security_label.setText("")
            self.security_label.setToolTip("Variables are safe.")
