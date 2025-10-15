from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
import json, csv

class ResponseVisualizerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Visualizador de respuestas (JSON/CSV)"))
        self.data_edit = QTextEdit()
        self.data_edit.setPlaceholderText("Pega aquí datos JSON o CSV...")
        layout.addWidget(self.data_edit)
        self.load_btn = QPushButton("Cargar archivo")
        self.load_btn.clicked.connect(self.load_file)
        layout.addWidget(self.load_btn)
        self.visualize_btn = QPushButton("Visualizar")
        self.visualize_btn.clicked.connect(self.visualize)
        layout.addWidget(self.visualize_btn)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Cargar datos", "", "JSON/CSV Files (*.json *.csv)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                self.data_edit.setText(f.read())

    def visualize(self):
        text = self.data_edit.toPlainText().strip()
        html = ""
        try:
            if text.startswith("{") or text.startswith("["):
                data = json.loads(text)
                html = self.generate_chart_html(data)
            else:
                reader = csv.reader(text.splitlines())
                rows = list(reader)
                html = self.generate_chart_html(rows)
        except Exception as e:
            html = f"<h3>Error al procesar datos: {e}</h3>"
        self.webview.setHtml(html if html is not None else "")

    def generate_chart_html(self, data):
        labels = []
        values = []
        if isinstance(data, dict):
            labels = list(data.keys())
            values = [float(data[k]) if str(data[k]).replace('.','',1).isdigit() else 0 for k in labels]
        elif isinstance(data, list):
            if all(isinstance(x, dict) for x in data):
                keys = list(data[0].keys())
                labels = [str(d[keys[0]]) for d in data]
                values = [float(d[keys[1]]) if str(d[keys[1]]).replace('.','',1).isdigit() else 0 for d in data]
            else:
                labels = data[0]
                values = [float(x[1]) if len(x)>1 and str(x[1]).replace('.','',1).isdigit() else 0 for x in data[1:]]
        html = """
        <html><head><style>
        .bar { display: inline-block; width: 40px; margin: 2px; background: #4e8cff; vertical-align: bottom; }
        .bar-label { writing-mode: vertical-lr; font-size: 10px; color: #222; }
        </style></head><body>
        <h3>Gráfico de barras</h3>
        <div style='height:200px;'>"""
        max_val = max(values) if values else 1
        for idx in range(len(values)):
            v = values[idx]
            label = labels[idx] if idx < len(labels) else ""
            html += f"<div class='bar' style='height:{int((v/max_val)*180)}px;' title='{label}'></div>"
        html += "</div><div>"
        for label in labels:
            html += f"<span class='bar-label'>{label}</span>"
        html += "</div></body></html>"
        return html
