from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QInputDialog, QDialog, QLabel, QTextEdit,
    QAbstractItemView, QFrame, QSpacerItem, QSizePolicy, QListWidgetItem, QMenu, QMessageBox
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QAction, QIcon
import sqlite3
import os

class CollectionSidebar(QWidget):
    def handle_nav_click_tree(self, item, column=None):
        # Only respond to leaf (action) clicks, not parent section clicks
        if item.childCount() == 0:
            action = item.text(0)
            parent = item.parent().text(0) if item.parent() else ""
            print(f"Sidebar action selected: {action} (Section: {parent})")
            # Example: switch main tab if action matches a tab name
            if self.main_window and hasattr(self.main_window, 'tabs'):
                tab_map = {
                    "Collections": 0,
                    "History": 1,
                    "Environments": 5,
                    "Auth": 6,
                    "Mock Server": 3,
                    "Plugins/Scripting": 9,
                    "User Management": 10,
                    "Cloud Sync": 11,
                    "CodeGen": 12,
                    "Accessibility/i18n": 13,
                    "Visualization": 14,
                    "Workspace Collaboration": 15,
                    "API Docs": 16,
                }
                idx = tab_map.get(str(parent), None)
                if idx is not None:
                    self.main_window.tabs.setCurrentIndex(idx)
    collection_selected = Signal(dict)


    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QToolButton
        from PySide6.QtGui import QIcon
        nav_label = QLabel("<b style='font-size:18px;color:#ff9800;letter-spacing:2px;'>NAVIGATION</b>")
        nav_label.setStyleSheet("margin-bottom:8px;margin-top:8px;")
        # --- Responsive sidebar layout ---
        from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QToolButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
        from PySide6.QtGui import QIcon
        main_vbox = QVBoxLayout()
        main_vbox.setSpacing(0)
        main_vbox.setContentsMargins(8, 8, 8, 8)

        # Top bar: label + floating add button
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        nav_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        top_bar.addWidget(nav_label)
        self.add_btn = QToolButton()
        self.add_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_btn.setToolTip("New Collection")
        self.add_btn.setStyleSheet("background:#282c34;color:#ff9800;border-radius:16px;padding:8px;")
        self.add_btn.clicked.connect(self.add_collection)
        top_bar.addWidget(self.add_btn)
        top_bar.setAlignment(self.add_btn, Qt.AlignmentFlag.AlignRight)
        main_vbox.addLayout(top_bar)

        # Navigation tree fills all remaining space
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.nav_tree.setStyleSheet("font-size:16px;border-radius:12px;background:#23252b;color:#e0e0e0;selection-background-color:#44475a;selection-color:#ff9800;border:2px solid #44475a;")

        # Main sections and icons
        sections = [
            ("Collections", []),
            ("History", []),
            ("Environments", []),
            ("Auth", []),
            ("Mock Server", []),
            ("Plugins/Scripting", []),
            ("User Management", []),
            ("Cloud Sync", []),
            ("CodeGen", []),
            ("Accessibility/i18n", []),
            ("Visualization", []),
            ("Workspace Collaboration", []),
            ("API Docs", []),
        ]
        icon_map = {
            "Collections": "folder",
            "History": "clock",
            "Environments": "database",
            "Auth": "security-high",
            "Mock Server": "media-playback-start",
            "Plugins/Scripting": "applications-system",
            "User Management": "user-group",
            "Cloud Sync": "cloud",
            "CodeGen": "code-context",
            "Accessibility/i18n": "accessibility",
            "Visualization": "view-statistics",
            "Workspace Collaboration": "applications-office",
            "API Docs": "help-about",
        }
        # Collections section with children from DB
        collections_parent = QTreeWidgetItem(["Collections"])
        collections_parent.setExpanded(True)
        collections_parent.setIcon(0, QIcon.fromTheme("folder"))
        import sqlite3
        try:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            rows = c.execute('SELECT name FROM collections').fetchall()
            for row in rows:
                col_item = QTreeWidgetItem([row[0]])
                col_item.setIcon(0, QIcon.fromTheme("folder"))
                collections_parent.addChild(col_item)
            conn.close()
        except Exception as e:
            print(f"[SoulFetch] Error loading collections: {e}")
        self.nav_tree.addTopLevelItem(collections_parent)

        # Other sections
        for section, actions in sections[1:]:
            parent = QTreeWidgetItem([section])
            parent.setExpanded(False)
            if section in icon_map:
                parent.setIcon(0, QIcon.fromTheme(icon_map[section]))
            self.nav_tree.addTopLevelItem(parent)

        self.nav_tree.itemClicked.connect(self.handle_nav_click_tree)
        self.nav_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.nav_tree.customContextMenuRequested.connect(self.show_nav_context_menu)
        main_vbox.addWidget(self.nav_tree)

        self.setLayout(main_vbox)

        # Visual style
        self.setStyleSheet('''
            QTreeWidget {
                background: #23252b;
                color: #8be9fd;
                border-radius: 8px;
                font-size: 15px;
                padding: 6px 0 6px 0;
                font-weight: bold;
            }
            QToolButton {
                background: #282c34;
                color: #ff9800;
                border: 1px solid #44475a;
                border-radius: 16px;
                padding: 8px;
                font-size: 18px;
                margin-bottom: 8px;
            }
            QToolButton:hover {
                background: #343746;
                color: #ffb86c;
            }
        ''')
        # Auto-create DB and tables if missing
        db_path = 'soulfetch.db'
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS collections (name TEXT, requests TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS history (method TEXT, url TEXT, body TEXT, status TEXT, response TEXT)')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[SoulFetch] DB init error: {e}")

    def show_nav_context_menu(self, pos):
        sender = self.sender()
        if sender == self.nav_tree:
            item = self.nav_tree.itemAt(pos)
            menu = QMenu(self)
            if item:
                parent = item.parent()
                # Collections section: menu
                if parent and parent.text(0) == "Collections":
                    action_rename = QAction("Rename", self)
                    action_rename.triggered.connect(lambda: self.rename_collection(item))
                    menu.addAction(action_rename)
                    action_delete = QAction("Delete", self)
                    action_delete.triggered.connect(lambda: self.delete_collection(item))
                    menu.addAction(action_delete)
                    action_duplicate = QAction("Duplicate", self)
                    action_duplicate.triggered.connect(lambda: self.duplicate_collection(item))
                    menu.addAction(action_duplicate)
                    action_move = QAction("Move to...", self)
                    action_move.triggered.connect(lambda: self.move_collection(item))
                    menu.addAction(action_move)
                    action_export = QAction("Export", self)
                    action_export.triggered.connect(lambda: self.export_single_collection(item))
                    menu.addAction(action_export)
                # Section actions (History, Environments, etc.)
                elif parent is None and item.text(0) == "Collections":
                    action_new = QAction("New Collection", self)
                    action_new.triggered.connect(self.add_collection)
                    menu.addAction(action_new)
                elif parent is None and item.text(0) == "History":
                    action_export_yaml = QAction("Export History (YAML)", self)
                    action_export_yaml.triggered.connect(self.export_history_yaml)
                    menu.addAction(action_export_yaml)
                    action_export_csv = QAction("Export History (CSV)", self)
                    action_export_csv.triggered.connect(self.export_history_csv)
                    menu.addAction(action_export_csv)
                    action_clear = QAction("Clear History", self)
                    action_clear.triggered.connect(self.clear_history)
                    menu.addAction(action_clear)
                # Add more context actions for other nav items as needed
            menu.exec_(self.nav_tree.viewport().mapToGlobal(pos))
    def duplicate_collection(self, item):
        import sqlite3, json
        from PySide6.QtWidgets import QTreeWidgetItem
        name = item.text(0)
        new_name = name + " (Copy)"
        try:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            row = c.execute('SELECT requests FROM collections WHERE name=?', (name,)).fetchone()
            if row:
                c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (new_name, row[0]))
                conn.commit()
                # Add to sidebar
                copy_item = QTreeWidgetItem([new_name])
                copy_item.setIcon(0, item.icon(0))
                item.parent().addChild(copy_item)
            conn.close()
        except Exception as e:
            print(f"[SoulFetch] Error duplicating collection: {e}")

    def move_collection(self, item):
        # Only one group exists, so just show info for now
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Move Collection", "Grouping not implemented yet. All collections are in the same group.")

    def export_single_collection(self, item):
        import sqlite3, json
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        name = item.text(0)
        try:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            row = c.execute('SELECT requests FROM collections WHERE name=?', (name,)).fetchone()
            conn.close()
            if row:
                fname, _ = QFileDialog.getSaveFileName(self, "Export Collection", f"{name}.json", "JSON Files (*.json)")
                if fname:
                    with open(fname, 'w', encoding='utf-8') as f:
                        f.write(json.dumps({"name": name, "requests": json.loads(row[0])}, indent=2))
                    QMessageBox.information(self, "Export", f"Collection '{name}' exported to {fname}")
        except Exception as e:
            print(f"[SoulFetch] Error exporting collection: {e}")

    # Métodos stub para evitar errores si no existen (debes implementar la lógica real en tu proyecto)
    def show_collection(self, item):
        # Show collection details or select collection (stub)
        pass
    def quick_access(self, item):
        # Quick access to collection (stub)
        pass
    def handle_nav_click(self, item):
        # Switch main tab based on navigation item
        if self.main_window and hasattr(self.main_window, 'tabs'):
            tab_map = {
                "Collections": 0,
                "History": 1,
                "Test Runner": 2,
                "Mock Server": 3,
                "Flow Designer": 4,
                "Environments": 5,
                "Auth": 6,
                "Response Visualizer": 7,
                "Scheduler/Monitor": 8,
                "Plugins/Scripting": 9,
                "User Management": 10,
                "Cloud Sync": 11,
                "CodeGen": 12,
                "Accessibility/i18n": 13,
                "Visualization": 14,
                "Workspace Collaboration": 15,
                "API Docs": 16,
            }
            idx = tab_map.get(item.text(), None)
            if idx is not None:
                self.main_window.tabs.setCurrentIndex(idx)
    def add_collection(self):
        name, ok = QInputDialog.getText(self, "New Collection", "Collection name:")
        if ok and name:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (name, '[]'))
            conn.commit()
            conn.close()
            from PySide6.QtWidgets import QTreeWidgetItem
            for i in range(self.nav_tree.topLevelItemCount()):
                parent = self.nav_tree.topLevelItem(i)
                if parent and parent.text(0) == "Collections":
                    new_item = QTreeWidgetItem([name])
                    new_item.setIcon(0, QIcon.fromTheme("folder"))
                    parent.addChild(new_item)
                    parent.setExpanded(True)
                    break

    def import_collections(self):
        from PySide6.QtWidgets import QFileDialog
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections", "", "JSON Files (*.json)")
        if fname:
            with open(fname, 'r', encoding='utf-8') as f:
                import json
                data = json.load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            for col in data:
                c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (col['name'], json.dumps(col['requests'])))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")

    def export_collections(self):
        from PySide6.QtWidgets import QFileDialog
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections", "collections.json", "JSON Files (*.json)")
        if fname:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            rows = c.execute('SELECT name, requests FROM collections').fetchall()
            conn.close()
            import json
            data = [{'name': name, 'requests': json.loads(reqs)} for name, reqs in rows]
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def export_collections_yaml(self):
        from PySide6.QtWidgets import QFileDialog
        import yaml
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections (YAML)", "collections.yaml", "YAML Files (*.yaml)")
        if fname:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            rows = c.execute('SELECT name, requests FROM collections').fetchall()
            conn.close()
            import json
            data = [{'name': name, 'requests': json.loads(reqs)} for name, reqs in rows]
            with open(fname, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def import_collections_yaml(self):
        from PySide6.QtWidgets import QFileDialog
        import yaml
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections (YAML)", "", "YAML Files (*.yaml)")
        if fname:
            with open(fname, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            import json
            for col in data:
                c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (col['name'], json.dumps(col['requests'])))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")

    def export_collections_csv(self):
        from PySide6.QtWidgets import QFileDialog
        import csv
        fname, _ = QFileDialog.getSaveFileName(self, "Export Collections (CSV)", "collections.csv", "CSV Files (*.csv)")
        if fname:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            rows = c.execute('SELECT name, requests FROM collections').fetchall()
            conn.close()
            import json
            with open(fname, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["name", "requests"])
                for name, reqs in rows:
                    writer.writerow([name, reqs])
            QMessageBox.information(self, "Export", f"Collections exported to {fname}")

    def import_collections_csv(self):
        from PySide6.QtWidgets import QFileDialog
        import csv
        fname, _ = QFileDialog.getOpenFileName(self, "Import Collections (CSV)", "", "CSV Files (*.csv)")
        if fname:
            with open(fname, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                conn = sqlite3.connect('soulfetch.db')
                c = conn.cursor()
                for row in reader:
                    c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (row['name'], row['requests']))
                conn.commit()
                conn.close()
            QMessageBox.information(self, "Import", f"Collections imported from {fname}")

    def export_api_docs(self):
        QMessageBox.information(self, "Export", "API Docs export not implemented.")
    def export_api_docs_html(self):
        QMessageBox.information(self, "Export", "API Docs HTML export not implemented.")
    def export_api_docs_openapi(self):
        QMessageBox.information(self, "Export", "API Docs OpenAPI export not implemented.")

    def export_history_yaml(self):
        from PySide6.QtWidgets import QFileDialog
        import yaml
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        rows = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        history = [dict(zip(['method', 'url', 'body', 'status', 'response'], row)) for row in rows]
        fname, _ = QFileDialog.getSaveFileName(self, "Export History (YAML)", "history.yaml", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                yaml.dump(history, f, allow_unicode=True, sort_keys=False)
            QMessageBox.information(self, "Export", f"History exported to {fname}")

    def import_history_yaml(self):
        from PySide6.QtWidgets import QFileDialog
        import yaml
        fname, _ = QFileDialog.getOpenFileName(self, "Import History (YAML)", "", "YAML Files (*.yaml)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                history = yaml.safe_load(f)
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('DELETE FROM history')
            for entry in history:
                c.execute('INSERT INTO history (method, url, body, status, response) VALUES (?, ?, ?, ?, ?)',
                          (entry['method'], entry['url'], entry.get('body',''), entry['status'], entry.get('response','')))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Import", f"History imported from {fname}")

    def export_history_csv(self):
        from PySide6.QtWidgets import QFileDialog
        import csv
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
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
        from PySide6.QtWidgets import QFileDialog
        import csv
        fname, _ = QFileDialog.getOpenFileName(self, "Import History (CSV)", "", "CSV Files (*.csv)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                conn = sqlite3.connect('soulfetch.db')
                c = conn.cursor()
                c.execute('DELETE FROM history')
                for row in reader:
                    c.execute('INSERT INTO history (method, url, body, status, response) VALUES (?, ?, ?, ?, ?)',
                              (row['method'], row['url'], row['body'], row['status'], row['response']))
                conn.commit()
                conn.close()
            QMessageBox.information(self, "Import", f"History imported from {fname}")

    def clear_history(self):
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('DELETE FROM history')
        conn.commit()
        conn.close()
        QMessageBox.information(self, "History", "History cleared.")

    def rename_collection(self, item):
        old_name = item.text()
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        import sqlite3
        new_name, ok = QInputDialog.getText(self, "Rename Collection", "New name:", text=old_name)
        if ok and new_name and new_name != old_name:
            try:
                conn = sqlite3.connect('soulfetch.db')
                c = conn.cursor()
                c.execute('UPDATE collections SET name=? WHERE name=?', (new_name, old_name))
                conn.commit()
                conn.close()
                item.setText(new_name)
                QMessageBox.information(self, "Rename", f"Collection renamed to '{new_name}'")
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", str(e))

    def delete_collection(self, item):
        name = item.text(0)
        reply = QMessageBox.question(self, "Delete Collection", f"Delete collection '{name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('soulfetch.db')
            c = conn.cursor()
            c.execute('DELETE FROM collections WHERE name=?', (name,))
            conn.commit()
            conn.close()
            # Remove from nav_tree
            parent = item.parent()
            if parent:
                parent.removeChild(item)
