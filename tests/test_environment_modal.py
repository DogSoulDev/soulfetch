from frontend.views.environment_modal import EnvironmentModal
from PySide6.QtWidgets import QApplication
import pytest

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_environment_modal_fields(app):
    modal = EnvironmentModal()
    modal.name_input.setText("dev")
    modal.vars_input.setText("API_KEY=123;SECRET=xyz")
    assert modal.name_input.text() == "dev"
    assert modal.vars_input.text() == "API_KEY=123;SECRET=xyz"
