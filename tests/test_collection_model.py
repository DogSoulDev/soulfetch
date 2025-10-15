from frontend.models.collection_model import CollectionModel

def test_collection_model_init():
    col = CollectionModel(name="Test Collection", requests=[])
    assert col.name == "Test Collection"
    assert isinstance(col.requests, list)
