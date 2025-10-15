from backend.domain.models import Request, Environment, History, Collection

def test_request_entity():
    req = Request(method="GET", url="https://example.com", headers={}, body="")
    assert req.method == "GET"
    assert req.url == "https://example.com"
    assert req.body == ""
    assert isinstance(req.headers, dict)

def test_environment_entity():
    env = Environment(name="dev", variables={"API_KEY": "123"})
    assert env.name == "dev"
    assert env.variables["API_KEY"] == "123"

def test_history_entity():
    hist = History(method="GET", url="https://example.com", status=200, response="OK")
    assert hist.method == "GET"
    assert hist.url == "https://example.com"
    assert hist.status == 200
    assert hist.response == "OK"

def test_collection_entity():
    col = Collection(name="Test Collection", requests=[])
    assert col.name == "Test Collection"
    assert isinstance(col.requests, list)
