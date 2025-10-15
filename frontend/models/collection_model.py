class CollectionModel:
    def __init__(self, name, requests=None):
        self.name = name
        self.requests = requests or []
