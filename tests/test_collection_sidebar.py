import pytest
from frontend.views.collection_sidebar import CollectionSidebar
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_collection_sidebar_init(app):
    sidebar = CollectionSidebar()
    assert sidebar is not None
    assert hasattr(sidebar, 'setLayout')
    assert sidebar.layout() is not None
