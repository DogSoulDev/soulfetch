import pytest
from frontend.views.flow_designer_tab import FlowDesignerTab
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_flow_designer_tab_init(app):
    tab = FlowDesignerTab()
    assert tab is not None
    assert hasattr(tab, 'setLayout')
    assert tab.layout() is not None
