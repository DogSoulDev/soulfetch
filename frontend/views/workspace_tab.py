from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox
from PySide6.QtCore import QTimer
import threading

class WorkspaceTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Workspace Collaboration"))
        self.workspace_list = QListWidget()
        layout.addWidget(self.workspace_list)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Workspace name")
        layout.addWidget(self.name_input)
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Owner username")
        layout.addWidget(self.owner_input)
        self.create_btn = QPushButton("Create Workspace")
        self.create_btn.clicked.connect(self.create_workspace)
        layout.addWidget(self.create_btn)
        self.connect_btn = QPushButton("Connect to Workspace")
        self.connect_btn.clicked.connect(self.connect_workspace)
        layout.addWidget(self.connect_btn)
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.refresh_workspaces()

    def refresh_workspaces(self):
        import requests
        self.workspace_list.clear()
        try:
            # For demo, fetch all workspaces (could be paginated)
            resp = requests.get("http://localhost:8000/workspace/demo", timeout=10)
            if resp.status_code == 200:
                ws = resp.json()
                self.workspace_list.addItem(f"{ws['name']} (Owner: {ws['owner']})")
        except Exception as e:
            # Provide visible feedback instead of silently passing
            self.status_label.setText(f"Failed to refresh workspaces: {e}")
            print(f"[WorkspaceTab] refresh_workspaces error: {e}")

    def create_workspace(self):
        import requests
        name = self.name_input.text().strip()
        owner = self.owner_input.text().strip()
        if name and owner:
            try:
                resp = requests.post("http://localhost:8000/workspace", json={"name": name, "owner": owner}, timeout=10)
                resp.raise_for_status()
                self.refresh_workspaces()
                QMessageBox.information(self, "Workspace", f"Workspace '{name}' created.")
            except Exception as e:
                QMessageBox.critical(self, "Workspace Error", f"Failed to create workspace: {e}")

    def connect_workspace(self):
        from PySide6.QtCore import QUrl
        import websocket
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Workspace", "Enter workspace name to connect.")
            return
        def ws_thread():
            try:
                ws = websocket.WebSocket()
                ws.connect(f"ws://localhost:8000/ws/workspace/{name}")
                self.status_label.setText(f"Connected to workspace '{name}'")
                while True:
                    msg = ws.recv()
                    self.status_label.setText(f"Message: {msg}")
            except Exception as e:
                self.status_label.setText(f"Connection error: {e}")
        threading.Thread(target=ws_thread, daemon=True).start()
