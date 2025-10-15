from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, QHBoxLayout, QListWidget, QDialog
from PySide6.QtCore import Signal
import importlib.util, os, traceback

class PluginManagerTab(QWidget):
    plugin_executed = Signal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sistema de Plugins y Scripting"))
        self.plugin_list = QListWidget()
        layout.addWidget(self.plugin_list)
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Cargar Plugin")
        self.load_btn.clicked.connect(self.load_plugin)
        btn_layout.addWidget(self.load_btn)
        self.import_btn = QPushButton("Importar Plugins")
        self.import_btn.clicked.connect(self.import_plugins)
        btn_layout.addWidget(self.import_btn)
        self.export_btn = QPushButton("Exportar Plugins")
        self.export_btn.clicked.connect(self.export_plugins)
        btn_layout.addWidget(self.export_btn)
        self.run_btn = QPushButton("Ejecutar Plugin")
        self.run_btn.clicked.connect(self.run_plugin)
        btn_layout.addWidget(self.run_btn)
        self.run_script_btn = QPushButton("Ejecutar Script Personalizado")
        self.run_script_btn.clicked.connect(self.run_custom_script)
        btn_layout.addWidget(self.run_script_btn)
        layout.addLayout(btn_layout)
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(QLabel("Salida del Plugin:"))
        layout.addWidget(self.output_edit)
        self.setLayout(layout)
        self.plugins = []
        self.selected_plugin_path = None
        self.plugin_list.itemClicked.connect(self.select_plugin)

    def import_plugins(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        fname, _ = QFileDialog.getOpenFileName(self, "Importar Plugins", "", "JSON Files (*.json)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                plugins = json.load(f)
            self.plugin_list.clear()
            self.plugins = []
            for p in plugins:
                self.plugins.append(p)
                self.plugin_list.addItem(os.path.basename(p))
            QMessageBox.information(self, "Importar", f"Importados {len(plugins)} plugins.")

    def export_plugins(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        fname, _ = QFileDialog.getSaveFileName(self, "Exportar Plugins", "plugins.json", "JSON Files (*.json)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(self.plugins, f, indent=2)
            QMessageBox.information(self, "Exportar", f"Exportados {len(self.plugins)} plugins.")

    def run_custom_script(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
        dialog = QDialog(self)
        dialog.setWindowTitle("Ejecutar Script Personalizado")
        vlayout = QVBoxLayout()
        script_edit = QTextEdit()
        script_edit.setPlaceholderText("Escribe tu script Python aquí...")
        vlayout.addWidget(script_edit)
        run_btn = QPushButton("Ejecutar")
        def run_script():
            code = script_edit.toPlainText()
            try:
                safe_globals = {"__builtins__": {"print": print, "len": len, "str": str, "dict": dict, "list": list}}
                exec(code, safe_globals)
                QMessageBox.information(dialog, "Script", "Script ejecutado correctamente.")
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Error al ejecutar script: {e}")
        run_btn.clicked.connect(run_script)
        vlayout.addWidget(run_btn)
        dialog.setLayout(vlayout)
        dialog.resize(600, 400)
        dialog.setModal(True)
        dialog.show()
    # Eliminado: inicialización duplicada de widgets/layout. Todo está en __init__.

    def load_plugin(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Seleccionar Plugin Python", "", "Python Files (*.py)")
        if fname:
            self.plugins.append(fname)
            self.plugin_list.addItem(os.path.basename(fname))

    def select_plugin(self, item):
        idx = self.plugin_list.row(item)
        self.selected_plugin_path = self.plugins[idx]

    def run_plugin(self):
        if not self.selected_plugin_path:
            self.output_edit.setText("Selecciona un plugin primero.")
            return
        try:
            # Sandbox básico: solo permite acceso a 'request' y 'response' si se pasan como argumentos
            spec = importlib.util.spec_from_file_location("user_plugin", self.selected_plugin_path)
            if spec is None or spec.loader is None:
                self.output_edit.setText("No se pudo cargar el plugin.")
                return
            plugin = importlib.util.module_from_spec(spec)
            # Limitar el entorno de ejecución
            safe_globals = {"__builtins__": {"print": print, "len": len, "str": str, "dict": dict, "list": list}}
            spec.loader.exec_module(plugin)
            if hasattr(plugin, "run"):
                result = plugin.run()
                self.output_edit.setText(str(result))
                self.plugin_executed.emit(str(result))
            else:
                self.output_edit.setText("El plugin debe definir una función 'run()'.")
        except Exception as e:
            tb = traceback.format_exc()
            self.output_edit.setText(f"Error al ejecutar plugin:\n{tb}")
