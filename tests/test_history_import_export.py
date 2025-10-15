from frontend.controllers.history_import_export import HistoryImportExport
from frontend.models.history_model import HistoryModel
import os
import tempfile

def test_import_export_history():
    history = [HistoryModel(method="GET", url="https://example.com", status=200, response="OK")]
    tmp = os.path.join(tempfile.gettempdir(), "history.json")
    HistoryImportExport.export_history(history, tmp)
    loaded = HistoryImportExport.import_history(tmp)
    assert len(loaded) == 1
    assert loaded[0].method == "GET"
    assert loaded[0].url == "https://example.com"
    assert loaded[0].status == 200
    assert loaded[0].response == "OK"
