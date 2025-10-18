import pytest
import os
from frontend.views.main_window import MainWindow
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.mark.skip(reason="Skipping GUI test to prevent hangs in all environments")
def test_main_window_init(app):
    pass
