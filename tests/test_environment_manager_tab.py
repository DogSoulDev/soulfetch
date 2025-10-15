import pytest
from frontend.views.environment_manager_tab import EnvironmentManagerTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_environment_manager_tab_init(app):
    tab = EnvironmentManagerTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
