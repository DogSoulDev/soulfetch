from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QHBoxLayout, QListWidget, QLineEdit
from PySide6.QtCore import Qt

class _TestRunnerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("API Test Runner"))
        self.test_list = QListWidget()
        layout.addWidget(self.test_list)
        self.test_code_edit = QTextEdit()
        self.test_code_edit.setPlaceholderText("Write Python test/assertions here. Example: assert response.status == 200")
        layout.addWidget(self.test_code_edit)
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Test")
        self.run_btn.clicked.connect(self.run_test)
        btn_layout.addWidget(self.run_btn)
        self.import_btn = QPushButton("Import Tests")
        self.import_btn.clicked.connect(self.import_tests)
        btn_layout.addWidget(self.import_btn)
        self.export_btn = QPushButton("Export Tests")
        self.export_btn.clicked.connect(self.export_tests)
        btn_layout.addWidget(self.export_btn)
        self.run_on_response_btn = QPushButton("Run on Last Response")
        self.run_on_response_btn.clicked.connect(self.run_on_last_response)
        btn_layout.addWidget(self.run_on_response_btn)
        layout.addLayout(btn_layout)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        self.setLayout(layout)
        self.tests = []
        self.last_response = None
        # Plantillas útiles para ciberseguridad y programación
        self.add_test("Status 200", "assert response.status == 200")
        self.add_test("JSON válido", "import json\njson.loads(response.body)")
        self.add_test("SQL Injection detectado", "assert 'syntax error' not in response.body.lower()")
        self.add_test("XSS detectado", "assert '<script>' not in response.body.lower()")
        self.add_test("Tiempo de respuesta < 2s", "assert getattr(response, 'elapsed', 1) < 2")
        self.add_test("Cabecera personalizada", "assert 'X-Api-Key' in response.body")
        self.add_test("Autenticación Bearer", "assert 'Bearer' in response.body or response.status == 401")
    def import_tests(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        fname, _ = QFileDialog.getOpenFileName(self, "Import Tests", "", "JSON Files (*.json)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                tests = json.load(f)
            self.test_list.clear()
            self.tests = []
            for t in tests:
                self.add_test(t['name'], t['code'])
            QMessageBox.information(self, "Import", f"Imported {len(tests)} tests.")

    def export_tests(self):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        fname, _ = QFileDialog.getSaveFileName(self, "Export Tests", "tests.json", "JSON Files (*.json)")
        if fname:
            tests = [{'name': n, 'code': c} for n, c in self.tests]
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(tests, f, indent=2)
            QMessageBox.information(self, "Export", f"Exported {len(tests)} tests.")

    def run_on_last_response(self):
        if self.last_response:
            self.run_test_on_response(self.last_response)
        else:
            self.result_label.setText("No response available.")

    def set_last_response(self, response_obj):
        self.last_response = response_obj

    def add_test(self, name, code):
        self.tests.append((name, code))
        self.test_list.addItem(name)

    def run_test(self):
        code = self.test_code_edit.toPlainText()
        result = self.execute_test(code)
        self.result_label.setText(result)

    def execute_test(self, code):
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            # Provide a mock response object for assertions
            class Response:
                def __init__(self):
                    self.status = 200
                    self.body = '{"success":true}'
            response = Response()
            exec(code, {"response": response})
            output = mystdout.getvalue() or "Test passed."
        except AssertionError as e:
            output = f"Assertion failed: {e}"
        except Exception as e:
            output = f"Error: {e}"
        finally:
            sys.stdout = old_stdout
        return output

    def run_test_on_response(self, response_obj):
        code = self.test_code_edit.toPlainText()
        result = self.execute_test_on_response(code, response_obj)
        self.result_label.setText(result)

    def execute_test_on_response(self, code, response_obj):
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            exec(code, {"response": response_obj})
            output = mystdout.getvalue() or "Test passed."
        except AssertionError as e:
            output = f"Assertion failed: {e}"
        except Exception as e:
            output = f"Error: {e}"
        finally:
            sys.stdout = old_stdout
        return output


__all__ = ["TestRunnerTab"]
TestRunnerTab = _TestRunnerTab
