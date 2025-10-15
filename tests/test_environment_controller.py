from frontend.controllers.environment_controller import EnvironmentController
import pytest

def test_add_and_get_environment():
    controller = EnvironmentController()
    env = {"id": 1, "name": "testenv", "variables": {"API_KEY": "abc123"}}
    result = controller.add_environment(env)
    assert result is not None
    envs = controller.get_environments()
    assert any(e["name"] == "testenv" for e in envs)
