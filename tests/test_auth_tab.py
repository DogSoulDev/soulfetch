import pytest
from frontend.views.auth_tab import AuthTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_auth_tab_init(app):
    tab = AuthTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
