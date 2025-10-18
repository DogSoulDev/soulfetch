from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTextEdit, QLabel, QMenu, QMessageBox, QFileDialog, QInputDialog, QTabWidget, QProgressBar, QSizePolicy,
    QListWidget, QListWidgetItem, QToolTip, QPlainTextEdit
)
from PySide6.QtCore import QThread, Signal, QObject, Qt
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView

class RequestWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)
    def __init__(self, method, url, headers, body, timeout=30):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.timeout = timeout
    def run(self):
        import requests, time
        result = {}
        try:
            start = time.time()
            response = requests.request(self.method, self.url, headers=self.headers, data=self.body, timeout=self.timeout)
            elapsed = time.time() - start
            result = {
                'status': response.status_code,
                'headers': dict(response.headers),
                'body': response.text,
                'elapsed': elapsed,
                'error': None,
                'content': response.content
            }
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class RequestTab(QWidget):
    response_visualize = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SoulFetch')
        self.setWindowIcon(QIcon('assets/soulfetch_icon.png'))
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._setup_request_controls()
        self._setup_template_box()
        self._setup_auth_controls()
        self._setup_env_controls()
        self._setup_body_edit()
        self._setup_script_edits()
        self._setup_response_tabs()
        self._setup_info_and_log()
        self._setup_progress_bar()
        self._setup_shortcuts()

    def _setup_shortcuts(self):
        from PySide6.QtGui import QShortcut, QKeySequence
        from PySide6.QtCore import Qt
        # ENTER triggers SEND if focus is on url_input or body_edit
        enter_shortcut = QShortcut(QKeySequence('Return'), self)
        enter_shortcut.activated.connect(self._trigger_send_if_focused)
        enter_shortcut2 = QShortcut(QKeySequence('Enter'), self)
        enter_shortcut2.activated.connect(self._trigger_send_if_focused)
        # Ctrl+Enter triggers SEND always
        ctrl_enter_shortcut = QShortcut(QKeySequence('Ctrl+Return'), self)
        ctrl_enter_shortcut.activated.connect(self._send_request_with_feedback)
        # Ctrl+S for quick save of body_edit
        ctrl_s_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        ctrl_s_shortcut.activated.connect(lambda: self._quick_save(self.body_edit))
        # Ctrl+R for rerun (send again)
        ctrl_r_shortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        ctrl_r_shortcut.activated.connect(self._send_request_with_feedback)
        # Tab/Shift+Tab for focus navigation (optional, Qt default)

    def _trigger_send_if_focused(self):
        # Only trigger SEND if focus is on url_input or body_edit
        focus_widget = self.focusWidget()
        if focus_widget in [self.url_input, self.body_edit]:
            self._send_request_with_feedback()

    def _setup_request_controls(self):
        req_controls = QHBoxLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
        self.method_box.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Request URL")
        self.url_input.setMinimumWidth(320)
        self.send_btn = QPushButton("  Send")
        self.send_btn.setIcon(QIcon.fromTheme("mail-send") or QIcon(":/icons/send.png"))
        self.send_btn.setMinimumHeight(38)
        self.send_btn.clicked.connect(self._send_request_with_feedback)
        self.send_btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    # Eliminada conexión a menú contextual sin lógica real
        req_controls.addWidget(self.method_box)
        req_controls.addWidget(self.url_input, 1)
        req_controls.addWidget(self.send_btn)
        self._main_layout.addLayout(req_controls)

    def _setup_template_box(self):
        template_controls = QHBoxLayout()
        self.template_box = QComboBox()
        self.template_box.addItems([
            "External: httpbin.org GET",  # Primera opción, funciona con cualquier web
            "REST: Create User", "REST: Login", "GraphQL: Query", "SOAP: Envelope", "Form: Login", "Custom: API Key",
            "Pentest: SQL Injection", "Pentest: XSS", "Pentest: Command Injection", "Pentest: SSRF", "Pentest: XXE",
            "Test: Large Payload", "Test: Invalid JSON", "Test: Slowloris", "Test: Fuzz Headers", "Test: Fuzz Body",
            "Programmer: File Upload", "Programmer: OAuth2 Token", "Programmer: Multipart Form", "Programmer: Custom Headers",
            "Programmer: PATCH Example", "Programmer: PUT Example", "Programmer: DELETE Example",
            "External: Google.com GET",
            "External: httpbin.org POST JSON",
            "External: Shodan.io Host Search",
            "External: HaveIBeenPwned Email Check",
            "External: HackerTarget DNS Lookup"
        ])
        self.template_box.currentIndexChanged.connect(self.apply_template)
        template_controls.addWidget(QLabel("Template:"))
        template_controls.addWidget(self.template_box)
        self._main_layout.addLayout(template_controls)

    def _setup_auth_controls(self):
        auth_layout = QHBoxLayout()
        self.auth_type = QComboBox()
        self.auth_type.addItems(["None", "Bearer Token", "Basic Auth"])
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("Token or username:password")
        auth_layout.addWidget(QLabel("Auth:"))
        auth_layout.addWidget(self.auth_type)
        auth_layout.addWidget(self.auth_input)
        self._main_layout.addLayout(auth_layout)

    def _setup_env_controls(self):
        self.env_vars = {"API_URL": "https://api.example.com", "TOKEN": "abcdef123456"}
        self.env_preview_btn = QPushButton("Preview Environment Variables")
        self.env_preview_btn.setToolTip("Show and edit environment variables used in requests.")
        self.env_preview_btn.clicked.connect(self.show_env_preview)
        self._main_layout.addWidget(self.env_preview_btn)

    def _setup_body_edit(self):
        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText("Request body (JSON, form, etc.)")
        self._main_layout.addWidget(QLabel("Body:"))
        self._main_layout.addWidget(self.body_edit)
        self._add_context_menu(self.body_edit, format_json=True, format_xml=True, quick_save=True)
        self._body_suggestions = [
            'username', 'password', 'token', 'email', 'search', 'comment', 'X-Api-Key', 'cmd', 'url',
            'Content-Type', 'Authorization', 'Bearer', 'Basic', 'admin', 'user', 'id', 'name', 'value',
            'form-data', 'application/json', 'application/xml', 'application/x-www-form-urlencoded',
        ]
        self._body_suggestions += [f'{{{{{k}}}}}' for k in self.env_vars.keys()]
    # Eliminadas conexiones a sugerencias y tooltips sin lógica real
        self._body_popup = None

    def _setup_script_edits(self):
        self.pre_script_edit = QTextEdit()
        self.pre_script_edit.setPlaceholderText("Pre-request script (Python)")
        self.post_script_edit = QTextEdit()
        self.post_script_edit.setPlaceholderText("Post-response script (Python)")
        self._main_layout.addWidget(QLabel("Pre-request Script:"))
        self._main_layout.addWidget(self.pre_script_edit)
        self._main_layout.addWidget(QLabel("Post-response Script:"))
        self._main_layout.addWidget(self.post_script_edit)

    def _setup_response_tabs(self):
        self.response_tabs = QTabWidget()
        self.response_request = QTextEdit(); self.response_request.setReadOnly(True)
        self.response_pretty = QTextEdit(); self.response_pretty.setReadOnly(True)
        self.response_raw = QTextEdit(); self.response_raw.setReadOnly(True)
        self.response_headers = QTextEdit(); self.response_headers.setReadOnly(True)
        self.response_cookies = QTextEdit(); self.response_cookies.setReadOnly(True)
        self.response_preview = QWebEngineView(); self._preview_plain_text = ""
        self.response_time_chart = QWebEngineView()
        self.response_tabs.addTab(self.response_request, "Request")
        self.response_tabs.addTab(self.response_pretty, "Pretty")
        self.response_tabs.addTab(self.response_raw, "Raw")
        self.response_tabs.addTab(self.response_headers, "Headers")
        self.response_tabs.addTab(self.response_cookies, "Cookies")
        self.response_tabs.addTab(self.response_preview, "Preview")
        self.response_tabs.addTab(self.response_time_chart, "Time Chart")
        self._main_layout.addWidget(self.response_tabs)

    def _setup_info_and_log(self):
        self.response_info = QLabel()
        self._main_layout.addWidget(self.response_info)
        self.terminal_log = QPlainTextEdit(); self.terminal_log.setReadOnly(True)
        self.terminal_log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.terminal_log.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.terminal_log.setMinimumHeight(120)
        self.terminal_log.setMaximumHeight(220)
        self.terminal_log.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._main_layout.addWidget(QLabel("Terminal / Log:"))
        self._main_layout.addWidget(self.terminal_log)

    def _setup_progress_bar(self):
        self.response_progress = QProgressBar()
        self._main_layout.addWidget(self.response_progress)

    # --- Logic methods ---
    def _send_request_with_feedback(self):
        # Collect request data and run pre-request script
        import re
        pre_code = self.pre_script_edit.toPlainText().strip()
        if pre_code:
            try:
                local_vars = {
                    'method': self.method_box.currentText(),
                    'url': self.url_input.text(),
                    'body': self.body_edit.toPlainText(),
                    'headers': {},
                    'env_vars': self.env_vars
                }
                exec(pre_code, {}, local_vars)
                self.method_box.setCurrentText(local_vars.get('method', self.method_box.currentText()))
                self.url_input.setText(local_vars.get('url', self.url_input.text()))
                self.body_edit.setText(local_vars.get('body', self.body_edit.toPlainText()))
                self.env_vars = local_vars.get('env_vars', self.env_vars)
            except Exception as e:
                self.terminal_log.appendPlainText(f"[PRE-SCRIPT ERROR] {e}")
        method = self.method_box.currentText()
        url = self.url_input.text().strip()
        body = self.body_edit.toPlainText().strip()
        # Validate URL
        if not re.match(r'^https?://[\w\.-]+(:\d+)?(/.*)?$', url):
            self.terminal_log.appendPlainText("[SECURITY] Invalid or unsafe URL.")
            return
        # Validate body (basic check for dangerous content)
        if any(x in body.lower() for x in ["<script>", "os.system", "subprocess", "eval", "exec"]):
            self.terminal_log.appendPlainText("[SECURITY] Dangerous content detected in body.")
            return
        headers = {}
        if self.auth_type.currentText() == "Bearer Token" and self.auth_input.text():
            headers["Authorization"] = f"Bearer {self.auth_input.text()}"
        elif self.auth_type.currentText() == "Basic Auth" and self.auth_input.text():
            headers["Authorization"] = f"Basic {self.auth_input.text()}"
        for k, v in self.env_vars.items():
            url = url.replace(f'{{{{{k}}}}}', str(v))
            body = body.replace(f'{{{{{k}}}}}', str(v))
        self.response_progress.setVisible(True)
        self.response_progress.setValue(0)
        self.terminal_log.appendPlainText(f"[SEND] {method} {url}")
        self._thread = QThread()
        self._worker = RequestWorker(method, url, headers, body)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_request_finished)
        self._worker.error.connect(self._on_request_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_request_finished(self, result):
        self.response_progress.setValue(100)
        status = result['status']
        # Color simple para status
        if 200 <= status < 300:
            color = 'green'
        elif 300 <= status < 400:
            color = 'goldenrod'
        elif 400 <= status < 500:
            color = 'orange'
        else:
            color = 'red'
        # Mostrar status coloreado en el info bar
        self.response_info.setText(f'<span style="color:{color};font-weight:bold;">Status: {status}</span> | Time: {result["elapsed"]:.2f}s | Size: {len(result["content"])} bytes')
        # Add status code explanation
        status_explanations_en = {
            200: "OK: The request was successful.",
            201: "Created: Resource created successfully.",
            204: "No Content: No content in response.",
            400: "Bad Request: Malformed request.",
            401: "Unauthorized: Not authorized.",
            403: "Forbidden: Access forbidden.",
            404: "Not Found: Resource not found.",
            405: "Method Not Allowed: Method not allowed.",
            409: "Conflict: Data conflict.",
            422: "Unprocessable Entity: Unprocessable entity.",
            429: "Too Many Requests: Too many requests.",
            500: "Internal Server Error: Internal server error.",
            502: "Bad Gateway: Bad gateway.",
            503: "Service Unavailable: Service unavailable."
        }
        explanation = status_explanations_en.get(status, "")
        self.terminal_log.appendPlainText(
            f"[RESPONSE] Status: {status} | Time: {result['elapsed']:.2f}s | Size: {len(result['content'])} bytes"
            + (f"\n[STATUS EXPLANATION] {explanation}" if explanation else "")
        )
        # TODO: Update response tabs and info bar

    def _on_request_error(self, error):
        self.response_progress.setValue(0)
        self.terminal_log.appendPlainText(f"[REQUEST ERROR] {error}")

    def apply_template(self):
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
        template = self.template_box.currentText()
        if template == "External: httpbin.org GET":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://httpbin.org/get")
            self.body_edit.setText("")
        elif template == "REST: Create User":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/users")
            self.body_edit.setText('{"username": "new_user", "password": "pass123"}')
        elif template == "External: Google.com GET":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://www.google.com")
            self.body_edit.setText("")
    # --- Revisión de pestañas ---
    # Las siguientes pestañas tienen lógica funcional real:
    # - Request (envío de peticiones)
    # - History (requiere backend, revisar si responde)
    # - Test Runner (requiere scripts, revisar si ejecuta)
    # - Mock Server (requiere backend, revisar endpoint)
    # - Flow Designer (si no tiene lógica, ocultar o comentar)
    # - Environments (gestión de variables, revisar si guarda/carga)
    # - Auth (funcional, pero revisar si conecta con backend)
    # - Response Visualizer (depende de respuesta, revisar)
    # - Scheduler/Monitor (si no tiene lógica, ocultar)
    # - Plugins/Scripting (si no ejecuta scripts, ocultar)
    # - Gemini (si no tiene lógica, ocultar)
    # - Cloud Sync (requiere backend, revisar endpoint)
    # - CodeGen (si no genera código, ocultar)
    # - Accessibility/i18n (si no cambia idioma/contraste, ocultar)
    # - User Management (si no gestiona usuarios, ocultar)
    # - Visualization (si no muestra gráficas, ocultar)
    # - Workspace Collaboration (si no sincroniza, ocultar)
        elif template == "External: httpbin.org POST JSON":
            self.method_box.setCurrentText("POST")
            self.url_input.setText("https://httpbin.org/post")
            self.body_edit.setText('{"test": "value"}')
        elif template == "External: Shodan.io Host Search":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://api.shodan.io/shodan/host/search?key=YOUR_API_KEY&query=apache")
            self.body_edit.setText("")
        elif template == "External: HaveIBeenPwned Email Check":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com")
            self.body_edit.setText("")
        elif template == "External: HackerTarget DNS Lookup":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://api.hackertarget.com/dnslookup/?q=example.com")
            self.body_edit.setText("")
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
        elif template == "Pentest: SQL Injection":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/search")
            self.body_edit.setText('{"search": "admin\' OR \'1\'=\'1"}')
        elif template == "Pentest: XSS":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/comment")
            self.body_edit.setText('{"comment": "<script>alert(1)</script>"}')
        elif template == "Pentest: Command Injection":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/cmd")
            self.body_edit.setText('{"cmd": "cat /etc/passwd"}')
        elif template == "Pentest: SSRF":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/ssrf")
            self.body_edit.setText('{"url": "http://127.0.0.1:80"}')
        elif template == "Pentest: XXE":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/xxe")
            self.body_edit.setText('<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>')
        elif template == "Test: Large Payload":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/upload")
            self.body_edit.setText('{"data": "%s"}' % ("A"*10000))
        elif template == "Test: Invalid JSON":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/json")
            self.body_edit.setText('{"invalid": }')
        elif template == "Test: Slowloris":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/slow")
            self.body_edit.setText('{"data": "test"}')
        elif template == "Test: Fuzz Headers":
            self.method_box.setCurrentText("GET")
            self.url_input.setText(f"{base_url}/fuzz")
            self.body_edit.setText('')
        elif template == "Test: Fuzz Body":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/fuzz")
            self.body_edit.setText('{"fuzz": "!@#$%^&*()_+"}')
        elif template == "Programmer: File Upload":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/upload")
            self.body_edit.setText('---boundary\nContent-Disposition: form-data; name="file"; filename="test.txt"\nContent-Type: text/plain\n\nHello World\n---boundary--')
        elif template == "Programmer: OAuth2 Token":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/oauth/token")
            self.body_edit.setText('grant_type=client_credentials&client_id=abc&client_secret=xyz')
        elif template == "Programmer: Multipart Form":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/form")
            self.body_edit.setText('field1=value1&field2=value2')
        elif template == "Programmer: Custom Headers":
            self.method_box.setCurrentText("GET")
            self.url_input.setText(f"{base_url}/headers")
            self.body_edit.setText('')
        elif template == "Programmer: PATCH Example":
            self.method_box.setCurrentText("PATCH")
            self.url_input.setText(f"{base_url}/update")
            self.body_edit.setText('{"field": "new_value"}')
        elif template == "Programmer: PUT Example":
            self.method_box.setCurrentText("PUT")
            self.url_input.setText(f"{base_url}/replace")
            self.body_edit.setText('{"field": "replace_value"}')
        elif template == "Programmer: DELETE Example":
            self.method_box.setCurrentText("DELETE")
            self.url_input.setText(f"{base_url}/delete")
            self.body_edit.setText('')
        else:
            self.body_edit.clear()
        self.body_edit.setFocus()
        if template == "REST: Create User":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/users")
            self.body_edit.setText('{"username": "new_user", "password": "pass123"}')
        elif template == "External: Google.com GET":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://www.google.com")
            self.body_edit.setText("")
        elif template == "External: httpbin.org GET":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://httpbin.org/get")
            self.body_edit.setText("")
        elif template == "External: httpbin.org POST JSON":
            self.method_box.setCurrentText("POST")
            self.url_input.setText("https://httpbin.org/post")
            self.body_edit.setText('{"test": "value"}')
        elif template == "External: Shodan.io Host Search":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://api.shodan.io/shodan/host/search?key=YOUR_API_KEY&query=apache")
            self.body_edit.setText("")
        elif template == "External: HaveIBeenPwned Email Check":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com")
            self.body_edit.setText("")
        elif template == "External: HackerTarget DNS Lookup":
            self.method_box.setCurrentText("GET")
            self.url_input.setText("https://api.hackertarget.com/dnslookup/?q=example.com")
            self.body_edit.setText("")
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
        elif template == "Pentest: SQL Injection":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/search")
            self.body_edit.setText('{"search": "admin\' OR \'1\'=\'1"}')
        elif template == "Pentest: XSS":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/comment")
            self.body_edit.setText('{"comment": "<script>alert(1)</script>"}')
        elif template == "Pentest: Command Injection":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/cmd")
            self.body_edit.setText('{"cmd": "cat /etc/passwd"}')
        elif template == "Pentest: SSRF":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/ssrf")
            self.body_edit.setText('{"url": "http://127.0.0.1:80"}')
        elif template == "Pentest: XXE":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/xxe")
            self.body_edit.setText('<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>')
        elif template == "Test: Large Payload":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/upload")
            self.body_edit.setText('{"data": "%s"}' % ("A"*10000))
        elif template == "Test: Invalid JSON":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/json")
            self.body_edit.setText('{"invalid": }')
        elif template == "Test: Slowloris":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/slow")
            self.body_edit.setText('{"data": "test"}')
        elif template == "Test: Fuzz Headers":
            self.method_box.setCurrentText("GET")
            self.url_input.setText(f"{base_url}/fuzz")
            self.body_edit.setText('')
        elif template == "Test: Fuzz Body":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/fuzz")
            self.body_edit.setText('{"fuzz": "!@#$%^&*()_+"}')
        elif template == "Programmer: File Upload":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/upload")
            self.body_edit.setText('---boundary\nContent-Disposition: form-data; name="file"; filename="test.txt"\nContent-Type: text/plain\n\nHello World\n---boundary--')
        elif template == "Programmer: OAuth2 Token":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/oauth/token")
            self.body_edit.setText('grant_type=client_credentials&client_id=abc&client_secret=xyz')
        elif template == "Programmer: Multipart Form":
            self.method_box.setCurrentText("POST")
            self.url_input.setText(f"{base_url}/form")
            self.body_edit.setText('field1=value1&field2=value2')
        elif template == "Programmer: Custom Headers":
            self.method_box.setCurrentText("GET")
            self.url_input.setText(f"{base_url}/headers")
            self.body_edit.setText('')
        elif template == "Programmer: PATCH Example":
            self.method_box.setCurrentText("PATCH")
            self.url_input.setText(f"{base_url}/update")
            self.body_edit.setText('{"field": "new_value"}')
        elif template == "Programmer: PUT Example":
            self.method_box.setCurrentText("PUT")
            self.url_input.setText(f"{base_url}/replace")
            self.body_edit.setText('{"field": "replace_value"}')
        elif template == "Programmer: DELETE Example":
            self.method_box.setCurrentText("DELETE")
            self.url_input.setText(f"{base_url}/delete")
            self.body_edit.setText('')
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
        except Exception as e:
            self.terminal_log.appendPlainText(f"[Format JSON Error] {e}")

    def _format_xml(self, widget):
        try:
            import xml.dom.minidom
            text = widget.toPlainText()
            dom = xml.dom.minidom.parseString(text)
            pretty = dom.toprettyxml()
            widget.setText(pretty)
        except Exception as e:
            self.terminal_log.appendPlainText(f"[Format XML Error] {e}")

    def _quick_save(self, widget):
        import os
        text = widget.toPlainText() if hasattr(widget, 'toPlainText') else widget.text()
        fname, _ = QFileDialog.getSaveFileName(self, "Save Content", "", "Text Files (*.txt)")
        if fname:
            # Security: prevent path traversal
            if os.path.isabs(fname) and not fname.startswith(os.getcwd()):
                self.terminal_log.appendPlainText("[SECURITY] Invalid file path.")
                return
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)

    # Métodos eliminados por no tener lógica real implementada
