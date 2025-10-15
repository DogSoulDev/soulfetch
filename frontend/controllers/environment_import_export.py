import json
from ..models.environment_model import EnvironmentModel

class EnvironmentImportExport:
    @staticmethod
    def export_environments(environments, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([e.__dict__ for e in environments], f, indent=2)

    @staticmethod
    def import_environments(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [EnvironmentModel(**e) for e in data]
