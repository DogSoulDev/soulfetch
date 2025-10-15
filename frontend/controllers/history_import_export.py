import json
from ..models.history_model import HistoryModel

class HistoryImportExport:
    @staticmethod
    def export_history(history, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([h.__dict__ for h in history], f, indent=2)

    @staticmethod
    def import_history(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [HistoryModel(**h) for h in data]
