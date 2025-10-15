from frontend.views.history_tab import HistoryTab
from PySide6.QtWidgets import QApplication
import pytest

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_history_tab_load(app):
    items = [
        {"method": "GET", "url": "https://httpbin.org/get", "status": 200},
        {"method": "POST", "url": "https://httpbin.org/post", "status": 201}
    ]
    tab = HistoryTab()
    tab.load_history(items)
    assert tab.list_widget.count() == 2
    assert tab.list_widget.item(0).text().startswith("GET https://httpbin.org/get")
