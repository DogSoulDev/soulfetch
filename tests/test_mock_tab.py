import pytest
from frontend.views.mock_tab import MockTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_mock_tab_init(app):
    tab = MockTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
