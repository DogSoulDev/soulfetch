from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog
from PySide6.QtCore import QTimer, QThread, Signal, Slot
import requests, time

class RequestSchedulerTab(QWidget):
    alert_signal = Signal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Programar y Monitorear Solicitudes"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL del endpoint a monitorear")
        layout.addWidget(self.url_input)
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("Intervalo (segundos)")
        layout.addWidget(self.interval_input)
        self.start_btn = QPushButton("Iniciar Monitoreo")
        self.start_btn.clicked.connect(self.start_monitoring)
        layout.addWidget(self.start_btn)
        self.stop_btn = QPushButton("Detener Monitoreo")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        self.status_table = QTableWidget(0, 3)
        self.status_table.setHorizontalHeaderLabels(["Timestamp", "Status", "Response"])
        layout.addWidget(self.status_table)
        self.setLayout(layout)
        self.timer = None
        self.monitoring = False
        self.alert_signal.connect(self.show_alert)

    def start_monitoring(self):
        url = self.url_input.text().strip()
        try:
            interval = int(self.interval_input.text().strip())
        except ValueError:
            interval = 10
        if not url:
            self.show_alert("URL requerida")
            return
        self.monitoring = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.check_endpoint(url))
        self.timer.start(interval * 1000)
        self.check_endpoint(url)

    def stop_monitoring(self):
        self.monitoring = False
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def check_endpoint(self, url):
        import os
        base_url = os.getenv("SOULFETCH_API_URL", "")
        if base_url and url.startswith("/"):
            url = base_url + url
        try:
            resp = requests.get(url, timeout=5)
            status = resp.status_code
            body = resp.text[:100]
            if status >= 400:
                self.alert_signal.emit(f"Fallo detectado: {status}")
        except Exception as e:
            status = "Error"
            body = str(e)
            self.alert_signal.emit(f"Error: {body}")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        row = self.status_table.rowCount()
        self.status_table.insertRow(row)
        self.status_table.setItem(row, 0, QTableWidgetItem(timestamp))
        self.status_table.setItem(row, 1, QTableWidgetItem(str(status)))
        self.status_table.setItem(row, 2, QTableWidgetItem(body))

    def show_alert(self, msg):
        dialog = QDialog(self)
        dialog.setWindowTitle("Alerta de Monitoreo")
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel(msg))
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        vlayout.addWidget(ok_btn)
        dialog.setLayout(vlayout)
        dialog.exec_()
