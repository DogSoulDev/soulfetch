from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QInputDialog, QDialog, QLabel, QTextEdit
from PySide6.QtCore import Signal

class CollectionSidebar(QWidget):
    collection_selected = Signal(dict)

    def __init__(self, main_window=None):
        super().__init__()
        from PySide6.QtWidgets import QAbstractItemView
        from PySide6.QtCore import Qt
        self.main_window = main_window
        self.sidebar_layout = QVBoxLayout()
        self.collection_list = QListWidget()
        self.collection_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.collection_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.collection_list.addItem("Collections")
        self.collection_list.addItem("History")
        self.sidebar_layout.addWidget(self.collection_list)
        self.collection_list.itemClicked.connect(self.show_collection)
        self.collection_list.itemDoubleClicked.connect(self.quick_access)
        btn_layout = QHBoxLayout()
        self.new_collection_btn = QPushButton("New Collection")
        self.new_collection_btn.clicked.connect(self.add_collection)
        btn_layout.addWidget(self.new_collection_btn)
        self.export_btn = QPushButton("Export Collections")
        self.export_btn.clicked.connect(self.export_collections)
        btn_layout.addWidget(self.export_btn)
        self.import_btn = QPushButton("Import Collections")
        self.import_btn.clicked.connect(self.import_collections)
        btn_layout.addWidget(self.import_btn)
        self.doc_md_btn = QPushButton("Export API Docs (Markdown)")
        self.doc_md_btn.clicked.connect(self.export_api_docs)
        self.sidebar_layout.addWidget(self.doc_md_btn)

        self.doc_html_btn = QPushButton("Export API Docs (HTML)")
        self.doc_html_btn.clicked.connect(self.export_api_docs_html)
        self.sidebar_layout.addWidget(self.doc_html_btn)

        self.doc_openapi_btn = QPushButton("Export API Docs (OpenAPI)")
        self.doc_openapi_btn.clicked.connect(self.export_api_docs_openapi)
        self.sidebar_layout.addWidget(self.doc_openapi_btn)
        # Add YAML and CSV import/export buttons
        self.export_yaml_btn = QPushButton("Export Collections (YAML)")
        self.export_yaml_btn.clicked.connect(self.export_collections_yaml)
        btn_layout.addWidget(self.export_yaml_btn)
        self.import_yaml_btn = QPushButton("Import Collections (YAML)")
        self.import_yaml_btn.clicked.connect(self.import_collections_yaml)
        btn_layout.addWidget(self.import_yaml_btn)
        self.export_csv_btn = QPushButton("Export Collections (CSV)")
        self.export_csv_btn.clicked.connect(self.export_collections_csv)
        btn_layout.addWidget(self.export_csv_btn)
        self.import_csv_btn = QPushButton("Import Collections (CSV)")
        self.import_csv_btn.clicked.connect(self.import_collections_csv)
        btn_layout.addWidget(self.import_csv_btn)
        # Add YAML and CSV import/export buttons for history (inside __init__)
        self.export_history_yaml_btn = QPushButton("Export History (YAML)")
        self.export_history_yaml_btn.clicked.connect(self.export_history_yaml)
        btn_layout.addWidget(self.export_history_yaml_btn)
        self.import_history_yaml_btn = QPushButton("Import History (YAML)")
        self.import_history_yaml_btn.clicked.connect(self.import_history_yaml)
        btn_layout.addWidget(self.import_history_yaml_btn)
        self.export_history_csv_btn = QPushButton("Export History (CSV)")
        self.export_history_csv_btn.clicked.connect(self.export_history_csv)
        btn_layout.addWidget(self.export_history_csv_btn)
        self.import_history_csv_btn = QPushButton("Import History (CSV)")
        self.import_history_csv_btn.clicked.connect(self.import_history_csv)
        btn_layout.addWidget(self.import_history_csv_btn)
    def export_history_yaml(self):
        import sqlite3
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import yaml
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS history (method TEXT, url TEXT, body TEXT, status TEXT, response TEXT)')
        rows = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        history = [dict(zip(['method', 'url', 'body', 'status', 'response'], row)) for row in rows]
        fname, _ = QFileDialog.getSaveFileName(self, "Export History (YAML)", "history.yaml", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                yaml.dump(history, f, allow_unicode=True, sort_keys=False)
            QMessageBox.information(self, "Export", f"History exported to {fname}")

    def import_history_yaml(self):
        import sqlite3
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import yaml
        fname, _ = QFileDialog.getOpenFileName(self, "Import History (YAML)", "", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                history = yaml.safe_load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS history (method TEXT, url TEXT, body TEXT, status TEXT, response TEXT)')
            c.execute('DELETE FROM history')
            for entry in history:
                c.execute('INSERT INTO history (method, url, body, status, response) VALUES (?, ?, ?, ?, ?)',
                          (entry['method'], entry['url'], entry.get('body',''), entry['status'], entry.get('response','')))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"History imported from {fname}")

    def export_history_csv(self):
        import sqlite3, csv
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS history (method TEXT, url TEXT, body TEXT, status TEXT, response TEXT)')
        rows = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        fname, _ = QFileDialog.getSaveFileName(self, "Export History (CSV)", "history.csv", "CSV Files (*.csv)")
        if fname:
            with open(fname, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["method", "url", "body", "status", "response"])
                for row in rows:
                    writer.writerow(row)
            QMessageBox.information(self, "Export", f"History exported to {fname}")

    def import_history_csv(self):
        import sqlite3, csv
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        fname, _ = QFileDialog.getOpenFileName(self, "Import History (CSV)", "", "CSV Files (*.csv)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                history = list(reader)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS history (method TEXT, url TEXT, body TEXT, status TEXT, response TEXT)')
            c.execute('DELETE FROM history')
            for entry in history:
                c.execute('INSERT INTO history (method, url, body, status, response) VALUES (?, ?, ?, ?, ?)',
                          (entry['method'], entry['url'], entry.get('body',''), entry['status'], entry.get('response','')))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"History imported from {fname}")
    def export_collections_yaml(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import yaml
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        rows = c.execute('SELECT name, requests FROM collections').fetchall()
        conn.close()
        collections = []
        for name, requests in rows:
            collections.append({'name': name, 'requests': json.loads(requests)})
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections (YAML)", "collections.yaml", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                yaml.dump(collections, f, allow_unicode=True, sort_keys=False)
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def import_collections_yaml(self):
        import sqlite3
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import yaml
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections (YAML)", "", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                collections = yaml.safe_load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
            import json
            for col in collections:
                c.execute('INSERT OR REPLACE INTO collections (name, requests) VALUES (?, ?)', (col['name'], json.dumps(col['requests'])))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")
            self.collection_list.clear()
            self.collection_list.addItem("Collections")
            self.collection_list.addItem("History")
            for col in collections:
                self.collection_list.addItem(col['name'])

    def export_collections_csv(self):
        import sqlite3, json, csv
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        rows = c.execute('SELECT name, requests FROM collections').fetchall()
        conn.close()
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections (CSV)", "collections.csv", "CSV Files (*.csv)")
        if fname:
            with open(fname, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["name", "method", "url", "body", "status", "response"])
                for name, requests in rows:
                    reqs = json.loads(requests)
                    for req in reqs:
                        writer.writerow([name, req.get('method',''), req.get('url',''), req.get('body',''), req.get('status',''), req.get('response','')])
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def import_collections_csv(self):
        import sqlite3, csv, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections (CSV)", "", "CSV Files (*.csv)")
        if fname:
            collections = {}
            with open(fname, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row['name']
                    req = {
                        'method': row['method'],
                        'url': row['url'],
                        'body': row['body'],
                        'status': row['status'],
                        'response': row['response']
                    }
                    if name not in collections:
                        collections[name] = []
                    collections[name].append(req)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
            for name, reqs in collections.items():
                c.execute('INSERT OR REPLACE INTO collections (name, requests) VALUES (?, ?)', (name, json.dumps(reqs)))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")
            self.collection_list.clear()
            self.collection_list.addItem("Collections")
            self.collection_list.addItem("History")
            for name in collections:
                self.collection_list.addItem(name)

    # ...existing code...
    def export_api_docs_html(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        collections = c.execute('SELECT name, requests FROM collections').fetchall()
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        history = []
        if 'history' in tables:
            history = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        html = ["<html><head><title>API Documentation</title></head><body>", "<h1>API Documentation</h1>"]
        for name, requests in collections:
            html.append(f"<h2>Collection: {name}</h2>")
            try:
                reqs = json.loads(requests)
            except Exception:
                reqs = []
            for req in reqs:
                html.append(f"<h3>{req.get('method','')} {req.get('url','')}</h3>")
                html.append(f"<b>Body:</b> <pre>{req.get('body','')}</pre>")
                html.append(f"<b>Status:</b> <code>{req.get('status','')}</code>")
                html.append(f"<b>Response:</b> <pre>{req.get('response','')}</pre>")
        if history:
            html.append("<h2>History</h2>")
            for h in history:
                html.append(f"<h3>{h[0]} {h[1]}</h3>")
                html.append(f"<b>Body:</b> <pre>{h[2]}</pre>")
                html.append(f"<b>Status:</b> <code>{h[3]}</code>")
                html.append(f"<b>Response:</b> <pre>{h[4]}</pre>")
        html.append("</body></html>")
        fname, _ = QFileDialog.getSaveFileName(self, "Export API Docs (HTML)", "api_docs.html", "HTML Files (*.html)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write('\n'.join(html))
            QMessageBox.information(self, "Export", f"API documentation exported to {fname}")

    def export_api_docs_openapi(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        collections = c.execute('SELECT name, requests FROM collections').fetchall()
        conn.close()
        openapi = {
            "openapi": "3.0.0",
            "info": {"title": "SoulFetch API", "version": "1.0.0"},
            "paths": {}
        }
        for name, requests in collections:
            try:
                reqs = json.loads(requests)
            except Exception:
                reqs = []
            for req in reqs:
                url = req.get('url','')
                method = req.get('method','get').lower()
                if url not in openapi['paths']:
                    openapi['paths'][url] = {}
                openapi['paths'][url][method] = {
                    "summary": f"{method.upper()} {url}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "example": req.get('body','')
                            }
                        }
                    },
                    "responses": {
                        str(req.get('status','200')): {
                            "description": "Response",
                            "content": {
                                "application/json": {
                                    "example": req.get('response','')
                                }
                            }
                        }
                    }
                }
        fname, _ = QFileDialog.getSaveFileName(self, "Export API Docs (OpenAPI)", "api_openapi.json", "JSON Files (*.json)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(openapi, f, indent=2)
            QMessageBox.information(self, "Export", f"OpenAPI documentation exported to {fname}")

    def add_collection(self):
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "New Collection", "Collection name:")
        if ok and name:
            self.collection_list.addItem(name)
            # For demo, add a dummy request to the collection
            self.save_collection(name, [{
                "method": "GET",
                "url": "https://api.example.com/demo",
                "body": "",
                "status": "",
                "response": ""
            }])

    def quick_access(self, item):
        name = item.text()
        if name == "History" and self.main_window:
            for i in range(self.main_window.tabs.count()):
                if self.main_window.tabs.tabText(i) == "History":
                    self.main_window.tabs.setCurrentIndex(i)
                    self.main_window.show_toast("History tab focused.", success=True)
                    return
        elif name != "Collections":
            self.show_collection(item)
    def export_collections(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        rows = c.execute('SELECT name, requests FROM collections').fetchall()
        conn.close()
        collections = []
        for name, requests in rows:
            collections.append({'name': name, 'requests': json.loads(requests)})
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections", "collections.json", "JSON Files (*.json)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(collections, f, indent=2)
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def import_collections(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections", "", "JSON Files (*.json)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                collections = json.load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
            for col in collections:
                c.execute('INSERT OR REPLACE INTO collections (name, requests) VALUES (?, ?)', (col['name'], json.dumps(col['requests'])))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")
            self.collection_list.clear()
            self.collection_list.addItem("Collections")
            self.collection_list.addItem("History")
            for col in collections:
                self.collection_list.addItem(col['name'])
    def export_api_docs(self):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        # Get collections
        collections = c.execute('SELECT name, requests FROM collections').fetchall()
        # Get history if exists
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        history = []
        if 'history' in tables:
            history = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        md = ["# API Documentation\n"]
        # Collections section
        for name, requests in collections:
            md.append(f"## Collection: {name}\n")
            try:
                reqs = json.loads(requests)
            except Exception:
                reqs = []
            for req in reqs:
                md.append(f"### {req.get('method','')} {req.get('url','')}\n")
                md.append(f"**Body:** `{req.get('body','')}`\n")
                md.append(f"**Status:** `{req.get('status','')}`\n")
                md.append("**Response:**\n````\n" + str(req.get('response','')) + "\n````\n")
        # History section
        if history:
            md.append("## History\n")
            for h in history:
                md.append(f"### {h[0]} {h[1]}\n")
                md.append(f"**Body:** `{h[2]}`\n")
                md.append(f"**Status:** `{h[3]}`\n")
                md.append("**Response:**\n````\n" + str(h[4]) + "\n````\n")
        fname, _ = QFileDialog.getSaveFileName(self, "Export API Docs", "api_docs.md", "Markdown Files (*.md)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write('\n'.join(md))
            QMessageBox.information(self, "Export", f"API documentation exported to {fname}")

    def show_collection(self, item):
        name = item.text()
        if name in ["Collections", "History"]:
            return
        # Load collection requests from SQLite
        collections = self.load_collections()
        for col in collections:
            if col['name'] == name:
                dialog = QDialog(self)
                dialog.setWindowTitle(f"Collection: {name}")
                vlayout = QVBoxLayout()
                for req in col['requests']:
                    req_label = QLabel(f"{req['method']} {req['url']}")
                    vlayout.addWidget(req_label)
                    view_btn = QPushButton("Load Request")
                    view_btn.clicked.connect(lambda _, r=req: self.load_request(r, dialog))
                    vlayout.addWidget(view_btn)
                dialog.setLayout(vlayout)
                dialog.exec_()
                break

    def load_request(self, req, dialog):
        self.collection_selected.emit(req)
        dialog.accept()

    def save_collection(self, name, requests):
        import sqlite3
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
        import json
        c.execute('INSERT OR REPLACE INTO collections (name, requests) VALUES (?, ?)', (name, json.dumps(requests)))
        conn.commit()
        conn.close()

    def load_collections(self):
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
