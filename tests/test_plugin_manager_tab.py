import pytest
from frontend.views.plugin_manager_tab import PluginManagerTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_plugin_manager_tab_init(app):
    tab = PluginManagerTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
    assert hasattr(tab, 'plugin_list')
    assert hasattr(tab, 'output_edit')
