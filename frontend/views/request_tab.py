from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTextEdit, QLabel, QCompleter, QMenu, QMessageBox, QFileDialog, QInputDialog, QTabWidget, QProgressBar, QSizePolicy,
    QListWidget, QListWidgetItem, QToolTip
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor, QColor, QIcon

## Eliminada definición duplicada de RequestTab y métodos, manteniendo solo la clase principal más abajo
class RequestTab(QWidget):
    def _get_current_word(self, text, pos):
        if not text or pos == 0:
            return ''
        left = text[:pos]
        import re
        match = re.search(r'(\w+|\{\{\w+\}\})$', left)
        return match.group(0) if match else ''

    def _insert_body_completion(self, item):
        cursor = self.body_edit.textCursor()
        text = self.body_edit.toPlainText()
        pos = cursor.position()
        word = self._get_current_word(text, pos)
        if word:
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, len(word))
            cursor.removeSelectedText()
            cursor.insertText(item.text())
            self.body_edit.setTextCursor(cursor)
        if self._body_popup:
            self._body_popup.hide()
    response_visualize = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SoulFetch')
        self.setWindowIcon(QIcon('assets/soulfetch_icon.png'))
        layout = QVBoxLayout()
        # Terminal/log panel mejorado
        from PySide6.QtWidgets import QPlainTextEdit
        self.terminal_log = QPlainTextEdit()
        self.terminal_log.setReadOnly(True)
        self.terminal_log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.terminal_log.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.terminal_log.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(QLabel("Terminal / Log:"))
        layout.addWidget(self.terminal_log)
        # El resto de la inicialización de widgets debe ir aquí, antes de cualquier uso de layout
        
    # Métodos de autocompletado y utilidades deben ir después de la inicialización de widgets
        # Request builder controls
        req_layout = QHBoxLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter request URL...")
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
        endpoints = [base_url, "https://api.github.com", "https://httpbin.org/get", "https://jsonplaceholder.typicode.com/posts"]
        completer = QCompleter(endpoints)
        try:
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        except Exception:
            pass
        self.url_input.setCompleter(completer)
        self.send_btn = QPushButton("Send")
        req_layout.addWidget(self.method_box)
        req_layout.addWidget(self.url_input, 3)
        req_layout.addWidget(self.send_btn)
        self.send_btn.clicked.connect(self._send_request_with_feedback)
        layout.addLayout(req_layout)
        # Smart Request Templates
        template_layout = QHBoxLayout()
        self.template_box = QComboBox()
        self.template_box.addItems([
            "None",
            "REST: Create User",
            "REST: Login",
            "GraphQL: Query",
            "SOAP: Envelope",
            "Form: Login",
            "Custom: API Key"
        ])
        self.template_btn = QPushButton("Auto-Fill")
        self.template_btn.clicked.connect(self.apply_template)
        template_layout.addWidget(QLabel("Template:"))
        template_layout.addWidget(self.template_box)
        template_layout.addWidget(self.template_btn)
        layout.addLayout(template_layout)
        # Authentication helpers
        auth_layout = QHBoxLayout()
        self.auth_type = QComboBox()
        self.auth_type.addItems(["None", "Bearer Token", "Basic Auth"])
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("Token or username:password")
        auth_layout.addWidget(QLabel("Auth:"))
        auth_layout.addWidget(self.auth_type)
        auth_layout.addWidget(self.auth_input)
        layout.addLayout(auth_layout)
        # Inline Environment Variable Preview
        self.env_vars = {"API_URL": "https://api.example.com", "TOKEN": "abcdef123456"}
        self.env_preview_btn = QPushButton("Preview Environment Variables")
        self.env_preview_btn.setToolTip("Show and edit environment variables used in requests.")
        self.env_preview_btn.clicked.connect(self.show_env_preview)
        layout.addWidget(self.env_preview_btn)
        # Request body
        from PySide6.QtWidgets import QListWidget, QListWidgetItem, QToolTip
        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText("Request body (JSON, form, etc.)")
        examples = [
            '{\n    "username": "your_username",\n    "password": "your_password"\n}',
            "{\"search\": \"admin' OR '1'='1\"}",
            '{\n    "comment": "<script>alert(1)</script>"\n}',
            '{\n    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."\n}',
            '<user>\n  <name>admin</name>\n  <pass>1234</pass>\n</user>',
            'username=admin&password=1234',
            '{\n    "X-Api-Key": "your_api_key"\n}',
            '{\n    "cmd": "cat /etc/passwd"\n}',
            '{\n    "url": "http://127.0.0.1:80"\n}'
        ]
        self.body_edit.setText(examples[0])
        layout.addWidget(QLabel("Body:"))
        layout.addWidget(self.body_edit)
        self._add_context_menu(self.body_edit, format_json=True, format_xml=True, quick_save=True)
        # Autocompletado avanzado para body_edit
        self._body_suggestions = [
            'username', 'password', 'token', 'email', 'search', 'comment', 'X-Api-Key', 'cmd', 'url',
            'Content-Type', 'Authorization', 'Bearer', 'Basic', 'admin', 'user', 'id', 'name', 'value',
            'form-data', 'application/json', 'application/xml', 'application/x-www-form-urlencoded',
        ]
        self._body_suggestions += [f'{{{{{k}}}}}' for k in self.env_vars.keys()]
        self.body_edit.textChanged.connect(self._show_body_suggestions)
        self.body_edit.cursorPositionChanged.connect(self._show_body_tooltip)
        self._body_popup = None
        # Advanced Response Panel
        layout.addWidget(QLabel("Response:"))
        self.response_tabs = QTabWidget()
        self.response_request = QTextEdit()
        self.response_request.setReadOnly(True)
        self.response_pretty = QTextEdit()
        self.response_pretty.setReadOnly(True)
        self.response_raw = QTextEdit()
        self.response_raw.setReadOnly(True)
        self.response_headers = QTextEdit()
        self.response_headers.setReadOnly(True)
        self.response_cookies = QTextEdit()
        self.response_cookies.setReadOnly(True)
        self.response_preview = QWebEngineView()
        self._preview_plain_text = ""
        self.response_tabs.addTab(self.response_request, "Request")
        self.response_tabs.addTab(self.response_pretty, "Pretty")
        self.response_tabs.addTab(self.response_raw, "Raw")
        self.response_tabs.addTab(self.response_headers, "Headers")
        self.response_tabs.addTab(self.response_cookies, "Cookies")
        self.response_tabs.addTab(self.response_preview, "Preview")
        self.response_time_chart = QWebEngineView()
        self.response_tabs.addTab(self.response_time_chart, "Time Chart")
        layout.addWidget(self.response_tabs)
        self.response_info = QLabel()
        layout.addWidget(self.response_info)
        self.response_progress = QProgressBar()
        self.response_progress.setVisible(False)
        layout.addWidget(self.response_progress)
        btn_layout = QHBoxLayout()
        self.copy_btn = QPushButton("Copy Response")
        self.copy_btn.clicked.connect(self.copy_response)
        self.save_btn = QPushButton("Save Response")
        self.save_btn.clicked.connect(self.save_response)
        self.download_btn = QPushButton("Download Response")
        self.download_btn.clicked.connect(self.download_response)
        btn_layout.addWidget(self.download_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        self.visualize_btn = QPushButton("Visualizar en Response Visualizer")
        self.visualize_btn.setToolTip("Enviar la respuesta actual al visualizador de respuestas.")
        self.visualize_btn.clicked.connect(self._emit_response_visualize)
        layout.addWidget(self.visualize_btn)
        self.setLayout(layout)

    def _show_body_suggestions(self):
        cursor = self.body_edit.textCursor()
        text = self.body_edit.toPlainText()
        pos = cursor.position()
        word = self._get_current_word(text, pos)
        filtered = [s for s in self._body_suggestions if word and word.lower() in s.lower()]
        if not filtered or not word:
            if self._body_popup is not None:
                self._body_popup.hide()
            return
        if not self._body_popup:
            self._body_popup = QListWidget(self.body_edit)
            self._body_popup.setWindowFlags(Qt.WindowType.Popup)
            self._body_popup.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self._body_popup.setMouseTracking(True)
            self._body_popup.itemClicked.connect(self._insert_body_completion)
        self._body_popup.clear()
        for s in filtered:
            item = QListWidgetItem(s)
            self._body_popup.addItem(item)
        rect = self.body_edit.cursorRect()
        global_pos = self.body_edit.mapToGlobal(rect.bottomRight())
        self._body_popup.move(global_pos)
        self._body_popup.setFixedWidth(220)
        self._body_popup.setFixedHeight(min(120, 24 * len(filtered)))
        self._body_popup.show()

    def _show_body_tooltip(self):
        cursor = self.body_edit.textCursor()
        text = self.body_edit.toPlainText()
        pos = cursor.position()
        word = self._get_current_word(text, pos)
        if word:
            tip = self._get_body_tooltip(word)
            if tip:
                QToolTip.showText(self.body_edit.mapToGlobal(self.body_edit.cursorRect().bottomRight()), tip)

    def _get_body_tooltip(self, word):
        tooltips = {
            'username': 'Nombre de usuario para autenticación/login.',
            'password': 'Contraseña para autenticación/login.',
            'token': 'Token de autenticación (JWT, OAuth, etc).',
            'email': 'Correo electrónico del usuario.',
            'search': 'Texto de búsqueda para endpoints de filtrado.',
            'comment': 'Comentario o texto libre.',
            'X-Api-Key': 'Clave API para autenticación.',
            'cmd': 'Comando para pruebas de seguridad.',
            'url': 'URL objetivo de la petición.',
            'Content-Type': 'Tipo de contenido del body (JSON, XML, etc).',
            'Authorization': 'Cabecera de autenticación.',
            'Bearer': 'Token tipo Bearer.',
            'Basic': 'Autenticación básica.',
            'admin': 'Usuario administrador.',
            'user': 'Usuario estándar.',
            'id': 'Identificador único.',
            'name': 'Nombre.',
            'value': 'Valor genérico.',
            'form-data': 'Formato para envío de formularios.',
            'application/json': 'Formato JSON.',
            'application/xml': 'Formato XML.',
            'application/x-www-form-urlencoded': 'Formato de formulario.',
        }
        if isinstance(word, str) and word.startswith('{{') and word.endswith('}}'):
            var = word[2:-2]
            return f'Variable de entorno: {var} = {self.env_vars.get(var, "(no definida)")}'
        return tooltips.get(word, '')

    def _send_request_with_feedback(self):
        import requests, time
        method = self.method_box.currentText()
        url = self.url_input.text()
        body = self.body_edit.toPlainText()
        headers = {}
        # Simple header parsing from auth and env
        if self.auth_type.currentText() == "Bearer Token" and self.auth_input.text():
            headers["Authorization"] = f"Bearer {self.auth_input.text()}"
        elif self.auth_type.currentText() == "Basic Auth" and self.auth_input.text():
            headers["Authorization"] = f"Basic {self.auth_input.text()}"
        # Replace env vars in URL/body
        url = self.replace_env_vars(url, self.env_vars)
        body = self.replace_env_vars(body, self.env_vars)
        self.response_progress.setVisible(True)
        self.response_progress.setValue(0)
        self.log_terminal(f"[SEND] {method} {url}")
        start = time.time()
        error = None
        response = None
        try:
            response = requests.request(method, url, headers=headers, data=body, timeout=30)
            elapsed = time.time() - start
            self.log_terminal(f"[RESPONSE] Status: {response.status_code} | Time: {elapsed:.2f}s | Size: {len(response.content)} bytes")
            self.response_progress.setValue(100)
            self.update_response_panel(
                status=response.status_code,
                headers=response.headers,
                body=response.text,
                elapsed=elapsed,
                error=None,
                previous_times=None,
                request_data={
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'params': {},
                    'body': body
                }
            )
        except Exception as e:
            elapsed = time.time() - start
            error = str(e)
            self.log_terminal(f"[ERROR] {error}")
            self.response_progress.setValue(0)
            self.update_response_panel(
                status='ERR',
                headers={},
                body='',
                elapsed=elapsed,
                error=error,
                previous_times=None,
                request_data={
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'params': {},
                    'body': body
                }
            )
        self.response_progress.setVisible(False)
        # Log full response for debugging
        if response:
            self.terminal_log.appendPlainText(f"--- Response Start ---\n{response.text}\n--- Response End ---")

    # Métodos lógicos y de UI
    def log_terminal(self, message):
        from datetime import datetime
        ts = datetime.now().strftime('%H:%M:%S')
        # Evitar mensajes repetidos consecutivos
        last = self.terminal_log.toPlainText().splitlines()[-1] if self.terminal_log.toPlainText() else ""
        new_msg = f"[{ts}] {message}"
        if last != new_msg:
            self.terminal_log.appendPlainText(new_msg)

    def apply_template(self):
        template = self.template_box.currentText()
                # Fragmentos inválidos eliminados
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
        if template == "REST: Create User":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/users")
            self.body_edit.setText('{"username": "new_user", "password": "pass123"}')
        elif template == "REST: Login":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/login")
            self.body_edit.setText('{"username": "admin", "password": "admin123"}')
        elif template == "GraphQL: Query":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/graphql")
            self.body_edit.setText('query { user(id: 1) { name email } }')
        elif template == "SOAP: Envelope":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/soap")
            self.body_edit.setText('<soapenv:Envelope>...</soapenv:Envelope>')
        elif template == "Form: Login":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/login")
            self.body_edit.setText('username=admin&password=1234')
        elif template == "Custom: API Key":
            self.method_box.setCurrentText("GET")
            self.url_input.setText(f"{base_url}/data")
            self.body_edit.setText('{"X-Api-Key": "your_api_key"}')
        else:
            self.body_edit.clear()
        self.body_edit.setFocus()

    def show_env_preview(self):
        env_text = "Environment Variables:\n"
        for k, v in self.env_vars.items():
            env_text += f"{k}: {v}\n"
        msg = QMessageBox(self)
        msg.setWindowTitle("Environment Variables")
        msg.setText(env_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()
        var, ok = QInputDialog.getText(self, "Edit Variable", "Enter variable name to edit:")
        if ok and var in self.env_vars:
            val, ok2 = QInputDialog.getText(self, "Edit Value", f"New value for {var}:")
            if ok2:
                self.env_vars[var] = val

    def _add_context_menu(self, widget, format_json=False, format_xml=False, quick_save=False):
        def context_menu(point):
            menu = QMenu()
            menu.addAction("Copy", lambda: widget.copy() if hasattr(widget, 'copy') else None)
            menu.addAction("Paste", lambda: widget.paste() if hasattr(widget, 'paste') else None)
            menu.addAction("Cut", lambda: widget.cut() if hasattr(widget, 'cut') else None)
            menu.addAction("Select All", lambda: widget.selectAll() if hasattr(widget, 'selectAll') else None)
            if format_json:
                menu.addAction("Format JSON", lambda: self._format_json(widget))
            if format_xml:
                menu.addAction("Format XML", lambda: self._format_xml(widget))
            if quick_save:
                menu.addAction("Quick Save", lambda: self._quick_save(widget))
            menu.exec_(widget.mapToGlobal(point))
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(context_menu)

    def _format_json(self, widget):
        try:
            import json
            text = widget.toPlainText()
            formatted = json.dumps(json.loads(text), indent=4)
            widget.setText(formatted)
        except Exception:
            pass

    def _format_xml(self, widget):
        try:
            import xml.dom.minidom
            text = widget.toPlainText()
            dom = xml.dom.minidom.parseString(text)
            pretty = dom.toprettyxml()
            widget.setText(pretty)
        except Exception:
            pass

    def _quick_save(self, widget):
        text = widget.toPlainText() if hasattr(widget, 'toPlainText') else widget.text()
        fname, _ = QFileDialog.getSaveFileName(self, "Save Content", "", "Text Files (*.txt)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)

    def run_security_audit(self):
        body = self.body_edit.toPlainText()
        url = self.url_input.text()
        auth = self.auth_input.text()
        issues = []
        if "' OR '1'='1" in body or "' OR 1=1" in body:
            issues.append("Possible SQL Injection pattern detected in body.")
        if "<script>" in body or "</script>" in body:
            issues.append("Possible XSS pattern detected in body.")
        if "cat /etc/passwd" in body:
            issues.append("Possible command injection pattern detected in body.")
        if "password" in body and "1234" in body:
            issues.append("Weak password example detected in body.")
        if "token" in body and len(body) < 20:
            issues.append("Token value may be too short.")
        if "admin" in url:
            issues.append("URL contains 'admin', check for privilege escalation risks.")
        if ":" in auth and "password" in auth:
            issues.append("Basic Auth with password detected, consider using tokens.")
        if "api_key" in body or "X-Api-Key" in body:
            issues.append("API key detected in body. Ensure it is not exposed.")
        if "http://" in url:
            issues.append("Non-HTTPS URL detected. Use HTTPS for security.")
        if not issues:
            issues.append("No obvious vulnerabilities detected.")
        QMessageBox.information(self, "Security Audit Results", "\n".join(issues))

    def update_response_panel(self, status, headers, body, elapsed, error=None, previous_times=None, request_data=None):
        """
        Update all response tabs and info bar with latest data.
        """
        import json
        # Actualizar pestaña Request si se proporciona request_data
        if request_data:
            req_text = (
                "Method: " + str(request_data.get('method','')) + "\n" +
                "URL: " + str(request_data.get('url','')) + "\n" +
                "Headers: " + json.dumps(request_data.get('headers',{}), indent=2) + "\n" +
                "Params: " + json.dumps(request_data.get('params',{}), indent=2) + "\n" +
                "Body:\n" + str(request_data.get('body',''))
            )
            self.response_request.setPlainText(req_text)
        # Info bar
        size = len(body.encode("utf-8")) if body else 0
        content_type = headers.get("Content-Type", "?") if isinstance(headers, dict) else str(headers)
        # Status code color indicator
        status_color = "lightgreen" if str(status).startswith("2") else ("red" if str(status).startswith(("4", "5")) else "yellow")
        info = f"<span style='color:{status_color};font-weight:bold'>Status: {status}</span> | Time: {elapsed:.2f}s | Size: {size} bytes | Content-Type: {content_type}"
        if error:
            info += f" | <span style='color:red'>Error: {error}</span>"
        self.response_info.setText(info)
        self.response_info.setTextFormat(Qt.TextFormat.RichText)
        # Headers tab
        if isinstance(headers, dict):
            headers_text = "\n".join([f"{k}: {v}" for k, v in headers.items()])
        else:
            headers_text = str(headers)
        self.response_headers.setPlainText(headers_text)
        # Cookies tab (if present)
        cookies = headers.get('Set-Cookie', '') if isinstance(headers, dict) else ''
        if hasattr(self, 'response_cookies'):
            self.response_cookies.setPlainText(cookies if cookies else 'No cookies received.')
        # Raw tab
        self.response_raw.setPlainText(body)
        # Pretty tab
        # Syntax highlighting for JSON/XML (basic)
        def highlight_json(text):
            import re
            # Simple color for keys and values
            text = re.sub(r'("[^"]+": )', r'<span style="color:#8be9fd">\1</span>', text)
            text = re.sub(r'(: "[^"]+")', r'<span style="color:#f1fa8c">\1</span>', text)
            return text
        def highlight_xml(text):
            import re
            text = re.sub(r'(&lt;[^&]+&gt;)', r'<span style="color:#ff79c6">\1</span>', text)
            return text
        try:
            parsed = json.loads(body)
            pretty = json.dumps(parsed, indent=2)
            self.response_pretty.setHtml(highlight_json(pretty))
            self.response_pretty.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        except Exception:
            # Try XML
            from html import escape
            if content_type.startswith("application/xml") or content_type.startswith("text/xml"):
                pretty = escape(body)
                self.response_pretty.setHtml(highlight_xml(pretty))
                self.response_pretty.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            else:
                # Error highlighting for invalid JSON/XML
                self.response_pretty.setHtml(f'<span style="color:red">Invalid JSON/XML or unsupported format.</span><br><pre>{escape(body)}</pre>')
                self.response_pretty.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        # Preview tab (HTML/XML) - use QWebEngineView for rich rendering
        from html import escape
        try:
            if content_type.startswith("text/html"):
                self.response_preview.setHtml(body)
                self._preview_plain_text = body
            elif content_type.startswith("application/xml") or content_type.startswith("text/xml"):
                self.response_preview.setHtml(f"<pre>{escape(body)}</pre>")
                self._preview_plain_text = body
            elif content_type.startswith("image/"):
                # Show image
                self.response_preview.setHtml(f'<img src="data:{content_type};base64,{body.encode("utf-8").hex()}" />')
                self._preview_plain_text = '[Image content]'
            elif content_type.startswith("application/pdf"):
                self.response_preview.setHtml('<span style="color:orange">PDF preview not supported. Please download.</span>')
                self._preview_plain_text = '[PDF content]'
            elif content_type.startswith("application/octet-stream"):
                self.response_preview.setHtml('<span style="color:orange">Binary preview not supported. Please download.</span>')
                self._preview_plain_text = '[Binary content]'
            else:
                # Fall back to preformatted text for other types
                self.response_preview.setHtml(f"<pre>{escape(body)}</pre>")
                self._preview_plain_text = body
        except Exception:
            # If preview widget isn't HTML-capable, keep plain text
            self._preview_plain_text = body

        # Response time chart (if previous_times provided)
        if previous_times and hasattr(self, 'response_time_chart'):
            # Native HTML bar chart (no matplotlib)
            times = previous_times + [elapsed]
            bars = ''.join([f'<div style="display:inline-block;width:20px;height:{max(5,int(t*30))}px;background:#8be9fd;margin-right:2px" title="{t:.2f}s"></div>' for t in times])
            chart_html = f'<div style="height:100px">{bars}</div><div>Response Times (s): {", ".join([f"{t:.2f}" for t in times])}</div>'
            self.response_time_chart.setHtml(chart_html)

    def copy_response(self):
        # Copy current tab content
        current = self.response_tabs.currentWidget()
        from PySide6.QtWidgets import QApplication
        text = ""
        if isinstance(current, QTextEdit):
            text = current.toPlainText()
        elif isinstance(current, QWebEngineView):
            text = self._preview_plain_text
        if text:
            QApplication.clipboard().setText(text)
            self.log_terminal("Response copied to clipboard.")

    def save_response(self):
        text = self.response_pretty.toPlainText()
        fname, _ = QFileDialog.getSaveFileName(self, "Save Response", "response.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)
            self.log_terminal(f"Response saved to {fname}.")

    def download_response(self):
        text = self.response_raw.toPlainText()
        fname, _ = QFileDialog.getSaveFileName(self, "Download Response", "response_raw.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)
            self.log_terminal(f"Raw response downloaded to {fname}.")

        # Solo la lógica de descarga, sin inicialización duplicada

    # Método duplicado eliminado

    def disable_privacy_mode(self):
        self.privacy_mode = False
        msg = QMessageBox(self)
        msg.setWindowTitle("Privacy Mode Disabled")
        msg.setText("Session ended. Requests and history will now be saved.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def run_test(self, test_code, response_text):
        """
        Ejecuta un test Python sobre la respuesta de la petición.
        test_code: string con código Python (asserts, validaciones)
        response_text: string con la respuesta de la API
        """
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        result = ""
        try:
            local_vars = {'response': response_text}
            exec(test_code, {}, local_vars)
            result = mystdout.getvalue() or "Test passed."
        except AssertionError as e:
            result = f"Assertion failed: {e}"
        except Exception as e:
            result = f"Error: {e}"
        finally:
            sys.stdout = old_stdout
        msg = QMessageBox(self)
        msg.setWindowTitle("Test Result")
        msg.setText(result)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def generate_code_snippet(self, method, url, headers, body):
        """
        Genera snippets de código para la petición actual en varios lenguajes.
        """
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
        if url.startswith("/"):
            url = base_url + url
        curl = f"curl -X {method} '{url}'"
        for k, v in headers.items():
            curl += f" -H '{k}: {v}'"
        if body:
            curl += f" -d '{body}'"
        python = f"import requests\nresponse = requests.{method.lower()}('{url}', headers={headers}, data={repr(body)})\nprint(response.text)"
        js = f"fetch('{url}', {{\n  method: '{method}',\n  headers: {headers},\n  body: {repr(body)}\n}}).then(r => r.text()).then(console.log)"
        msg = QMessageBox(self)
        msg.setWindowTitle("Code Snippets")
        msg.setText(f"cURL:\n{curl}\n\nPython:\n{python}\n\nJavaScript:\n{js}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    # Colecciones y carpetas (estructura básica)
    def save_collection(self, name, requests):
        """
        Guarda una colección de peticiones en SQLite.
        name: nombre de la colección
        requests: lista de dicts con datos de cada petición
        """
        import sqlite3
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        import json
        c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (name, json.dumps(requests)))
        conn.commit()
        conn.close()
        msg = QMessageBox(self)
        msg.setWindowTitle("Colección guardada")
        msg.setText(f"Colección '{name}' guardada correctamente.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def load_collections(self):
        """
        Carga todas las colecciones guardadas desde SQLite.
        """
        import sqlite3
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        rows = c.execute('SELECT name, requests FROM collections').fetchall()
        conn.close()
        import json
        collections = []
        for name, requests in rows:
            collections.append({'name': name, 'requests': json.loads(requests)})
        return collections

    # Panel de variables globales y de entorno
    def save_env_vars(self, env_name, variables):
        """
        Guarda un conjunto de variables de entorno en SQLite.
        env_name: nombre del entorno
        variables: dict de variables
        """
        import sqlite3, json
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS env_vars (env_name TEXT, variables TEXT)')
        c.execute('INSERT OR REPLACE INTO env_vars (env_name, variables) VALUES (?, ?)', (env_name, json.dumps(variables)))
        conn.commit()
        conn.close()
        msg = QMessageBox(self)
        msg.setWindowTitle("Variables de entorno guardadas")
        msg.setText(f"Variables para '{env_name}' guardadas correctamente.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def load_env_vars(self):
        """
        Carga todos los entornos y variables guardadas desde SQLite.
        """
        import sqlite3, json
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS env_vars (env_name TEXT, variables TEXT)')
        rows = c.execute('SELECT env_name, variables FROM env_vars').fetchall()
        conn.close()
        envs = {}
        for env_name, variables in rows:
            envs[env_name] = json.loads(variables)
        return envs

    def replace_env_vars(self, text, env_vars):
        """
        Reemplaza variables en el texto usando el dict env_vars.
        """
        for k, v in env_vars.items():
            text = text.replace(f'{{{{{k}}}}}', str(v))
        return text

    # Monitorización y programación de peticiones
    def schedule_request(self, method, url, headers, body, interval_sec):
        """
        Programa una petición recurrente cada interval_sec segundos.
        """
        import threading, time, requests
        def task():
            while True:
                try:
                    resp = requests.request(method, url, headers=headers, data=body)
                    status = resp.status_code
                    if not str(status).startswith('2'):
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Alerta de monitorización")
                        msg.setText(f"Petición a {url} falló con status {status}.")
                        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        msg.exec_()
                except Exception as e:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Alerta de monitorización")
                    msg.setText(f"Error en petición a {url}: {e}")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec_()
                time.sleep(interval_sec)
        t = threading.Thread(target=task, daemon=True)
        t.start()
        msg = QMessageBox(self)
        msg.setWindowTitle("Monitorización iniciada")
        msg.setText(f"Monitorización de {url} cada {interval_sec} segundos.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def _emit_response_visualize(self):
        self.response_visualize.emit(self.response_pretty.toPlainText())

    def set_env_vars(self, variables_str):
        # Recibe variables en formato key1=value1;key2=value2 y las aplica al request
        env_vars = {}
        for pair in variables_str.split(';'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                env_vars[k.strip()] = v.strip()
        self.env_vars = env_vars
        self.log_terminal(f"[ENV] Variables actualizadas: {env_vars}")

    def set_auth_config(self, config):
        self.log_terminal(f"[AUTH] Configuración aplicada: {config}")
        self._auth_config = config
