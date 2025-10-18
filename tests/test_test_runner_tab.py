import pytest
from frontend.views.test_runner_tab import _TestRunnerTab as TestRunnerTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_test_runner_tab_init(app):
    tab = TestRunnerTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
