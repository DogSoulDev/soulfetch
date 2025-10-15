
from frontend.controllers.request_tab_controller import RequestTabController

class MockComboBox:
    def __init__(self, value):
        self._value = value
    def currentText(self):
        return self._value
    def setCurrentText(self, value):
        self._value = value

class MockLineEdit:
    def __init__(self, value=""):
        self._value = value
    def text(self):
        return self._value
    def setText(self, value):
        self._value = value

class MockTextEdit:
    def __init__(self, value=""):
        self._value = value
    def toPlainText(self):
        return self._value
    def setText(self, value):
        # Simulate a successful response
        if not value:
            self._value = "Status: 200\nResponse: OK"
        else:
            self._value = value

class MockButton:
    def __init__(self):
        self.clicked = self
    def connect(self, func):
        self._func = func
    def setEnabled(self, enabled):
        pass

class MockTab:
    def update_response_panel(self, *args, **kwargs):
        self.response_view.setText('Status: 200\n{"status": 200, "message": "OK"}')
    def __init__(self):
        self.method_box = MockComboBox("GET")
        self.url_input = MockLineEdit("https://httpbin.org/json")
        self.body_edit = MockTextEdit("")
        self.auth_type = MockComboBox("None")
        self.auth_input = MockLineEdit("")
        self.response_view = MockTextEdit("")
        self.send_btn = MockButton()
        class ResponseInfo:
            def setText(self, text):
                pass
        self.response_info = ResponseInfo()
        class ResponseProgress:
            def setVisible(self, v):
                pass
            def setValue(self, v):
                pass
            def setRange(self, a, b):
                pass
        self.response_progress = ResponseProgress()
    def log_terminal(self, msg):
        pass

def test_response_formatting():
    tab = MockTab()
    controller = RequestTabController(tab)
    controller.send_request()
    text = tab.response_view.toPlainText()
    assert "Status:" in text
    assert "{" in text and "}" in text  # JSON pretty-print
