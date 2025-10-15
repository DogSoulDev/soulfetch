from frontend.controllers.history_controller import HistoryController
import pytest

def test_add_and_get_history():
    controller = HistoryController()
    item = {"id": 1, "method": "GET", "url": "https://httpbin.org/get", "status": 200, "response": "OK"}
    result = controller.add_history(item)
    assert result is not None
    history = controller.get_history()
    assert any(h["url"] == "https://httpbin.org/get" for h in history)
