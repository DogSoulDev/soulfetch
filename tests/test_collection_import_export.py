from frontend.controllers.collection_controller import CollectionController
from frontend.models.collection_model import CollectionModel
import os
import tempfile

def test_import_export_collections():
    controller = CollectionController()
    c1 = CollectionModel(name="Test", requests=[])
    controller.add_collection(c1)
    tmp = os.path.join(tempfile.gettempdir(), "collections.json")
    controller.export_collections(tmp)
    controller.collections = []
    controller.import_collections(tmp)
    assert len(controller.collections) == 1
    assert controller.collections[0].name == "Test"
