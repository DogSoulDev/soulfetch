class RequestModel:
    def __init__(self, method="GET", url="", body="", headers=None):
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers or {}
