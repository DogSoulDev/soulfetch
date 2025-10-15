from frontend.models.history_model import HistoryModel

def test_history_model_init():
    hist = HistoryModel(method="GET", url="https://example.com", status=200, response="OK")
    assert hist.method == "GET"
    assert hist.url == "https://example.com"
    assert hist.status == 200
    assert hist.response == "OK"
