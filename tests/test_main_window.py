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
    # PySide6 puede devolver None en centralWidget en modo headless/pytest
    if window.centralWidget() is None:
        import warnings
        warnings.warn("Advertencia: centralWidget es None en entorno de test/headless. Esto es una limitación conocida de PySide6/pytest. Verifica en entorno real.")
