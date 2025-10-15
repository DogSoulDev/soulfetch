import pytest
from frontend.views.main_window import MainWindow
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_main_window_init(app):
    window = MainWindow()
    assert window is not None
    assert hasattr(window, 'setCentralWidget')
    assert window.centralWidget() is not None
