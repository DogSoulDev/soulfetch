import pytest
from frontend.views.main_view import MainView
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_main_view_init(app):
    view = MainView()
    assert view is not None
    assert hasattr(view, 'setLayout')
    assert view.layout() is not None
