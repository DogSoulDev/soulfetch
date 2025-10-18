from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox

class UserManagerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("User Management"))
        self.user_list = QListWidget()
        layout.addWidget(self.user_list)
        self.add_user_btn = QPushButton("Add User")
        self.add_user_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_btn)
        self.remove_user_btn = QPushButton("Remove Selected User")
        self.remove_user_btn.clicked.connect(self.remove_user)
        layout.addWidget(self.remove_user_btn)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        self.setLayout(layout)
        self.refresh_users()

    def refresh_users(self):
        import requests
        self.user_list.clear()
        try:
            resp = requests.get("http://localhost:8000/users", timeout=10)
            resp.raise_for_status()
            users = resp.json().get("users", [])
            for username in users:
                self.user_list.addItem(username)
        except Exception as e:
            msg = str(e)
            if 'Failed to connect' in msg or 'Connection refused' in msg:
                QMessageBox.critical(self, "User Error", "Backend unavailable. Please start the SoulFetch backend server.")
            else:
                QMessageBox.critical(self, "User Error", f"Failed to load users: {msg}")
    def add_user(self):
        import requests
        username = self.username_input.text().strip()
        if username:
            try:
                resp = requests.post("http://localhost:8000/users", json={"username": username}, timeout=10)
                resp.raise_for_status()
                self.username_input.clear()
                self.refresh_users()
                QMessageBox.information(self, "User Added", f"User '{username}' added.")
            except Exception as e:
                msg = str(e)
                if 'Failed to connect' in msg or 'Connection refused' in msg:
                    QMessageBox.critical(self, "User Error", "Backend unavailable. Please start the SoulFetch backend server.")
                else:
                    QMessageBox.critical(self, "User Error", f"Failed to add user: {msg}")
    def remove_user(self):
        import requests
        selected = self.user_list.currentItem()
        if selected:
            username = selected.text()
            try:
                resp = requests.delete(f"http://localhost:8000/users/{username}", timeout=10)
                resp.raise_for_status()
                self.refresh_users()
                QMessageBox.information(self, "User Removed", f"User '{username}' removed.")
            except Exception as e:
                msg = str(e)
                if 'Failed to connect' in msg or 'Connection refused' in msg:
                    QMessageBox.critical(self, "User Error", "Backend unavailable. Please start the SoulFetch backend server.")
                else:
                    QMessageBox.critical(self, "User Error", f"Failed to remove user: {msg}")
