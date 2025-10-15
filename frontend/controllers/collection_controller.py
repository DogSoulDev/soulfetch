import json
from ..models.collection_model import CollectionModel

class CollectionController:
    def __init__(self):
        self.collections = []

    def add_collection(self, collection):
        self.collections.append(collection)

    def export_collections(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([c.__dict__ for c in self.collections], f, indent=2)

    def import_collections(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.collections = [CollectionModel(**c) for c in data]
