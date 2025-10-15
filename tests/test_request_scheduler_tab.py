import pytest
from frontend.views.request_scheduler_tab import RequestSchedulerTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_request_scheduler_tab_init(app):
    tab = RequestSchedulerTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
