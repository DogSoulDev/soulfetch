from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QDialog, QTextEdit, QHBoxLayout
from PySide6.QtCore import Signal

class HistoryTab(QWidget):
    request_rerun = Signal(dict)
    def __init__(self, history_items=None):
        super().__init__()
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Request History"))
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.history_items = history_items or []
        self.list_widget.itemClicked.connect(self.show_details)
        if history_items:
            self.load_history(history_items)
        self.current_env_vars = None
        self.current_auth_config = None

    def load_history(self, items):
        self.list_widget.clear()
        self.history_items = items
        for idx, item in enumerate(items):
            self.list_widget.addItem(f"{item['method']} {item['url']} - {item['status']}")

    def show_details(self, item):
        idx = self.list_widget.row(item)
        entry = self.history_items[idx]
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Details: {entry['method']} {entry['url']}")
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel(f"Method: {entry['method']}"))
        vlayout.addWidget(QLabel(f"URL: {entry['url']}"))
        vlayout.addWidget(QLabel(f"Status: {entry['status']}"))
        resp_edit = QTextEdit()
        resp_edit.setReadOnly(True)
        resp_edit.setText(entry.get('response', ''))
        vlayout.addWidget(QLabel("Response:"))
        vlayout.addWidget(resp_edit)
        btn_layout = QHBoxLayout()
        rerun_btn = QPushButton("Re-run Request")
        rerun_btn.clicked.connect(lambda: self.rerun_request(entry, dialog))
        btn_layout.addWidget(rerun_btn)
        vlayout.addLayout(btn_layout)
        dialog.setLayout(vlayout)
        dialog.exec_()

    def rerun_request(self, entry, dialog):
        # Emitir también el entorno y auth actual si están disponibles
        payload = dict(entry)
        if hasattr(self, 'current_env_vars'):
            payload['env_vars'] = self.current_env_vars
        if hasattr(self, 'current_auth_config'):
            payload['auth_config'] = self.current_auth_config
        self.request_rerun.emit(payload)
        dialog.accept()

    def set_env_vars(self, env_vars):
        self.current_env_vars = env_vars

    def set_auth_config(self, auth_config):
        self.current_auth_config = auth_config
