from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox

class VisualizationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Advanced Visualization"))
        self.visualize_btn = QPushButton("Visualize Data")
        self.visualize_btn.clicked.connect(self.visualize_data)
        layout.addWidget(self.visualize_btn)
        self.data_edit = QTextEdit()
        layout.addWidget(self.data_edit)
        self.setLayout(layout)
    def visualize_data(self):
        import requests
        self.data_edit.clear()
        try:
            resp = requests.get("http://localhost:8000/visualization/data", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Format and display aggregated data
            text = (
                f"Collections: {data.get('collections', 0)}\n"
                f"History Entries: {data.get('history_count', 0)}\n"
                f"Request Method Counts:\n"
            )
            for method, count in data.get('method_counts', {}).items():
                text += f"  {method}: {count}\n"
            self.data_edit.setText(text)
            QMessageBox.information(self, "Visualization", "Data visualization updated.")
        except Exception as e:
            self.data_edit.setText("")
            QMessageBox.critical(self, "Visualization Error", f"Failed to visualize data: {e}")
