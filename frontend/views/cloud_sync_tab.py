from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class CloudSyncTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Cloud Sync"))
        self.sync_btn = QPushButton("Sync Now")
        self.sync_btn.clicked.connect(self.sync_now)
        layout.addWidget(self.sync_btn)
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        self.setLayout(layout)
    def sync_now(self):
        import requests
        self.status_label.setText("Syncing...")
        try:
            # Download data from cloud
            resp = requests.get("http://localhost:8000/cloud/sync", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Upload current data to cloud (simulate bi-directional sync)
            up_resp = requests.post("http://localhost:8000/cloud/sync", json=data, timeout=10)
            up_resp.raise_for_status()
            self.status_label.setText("Sync complete.")
            QMessageBox.information(self, "Cloud Sync", "Data synced with cloud.")
        except Exception as e:
            self.status_label.setText("Sync failed.")
            QMessageBox.critical(self, "Cloud Sync Error", f"Sync failed: {e}")
