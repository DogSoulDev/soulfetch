class HistoryModel:
    def __init__(self, method, url, status, response):
        self.method = method
        self.url = url
        self.status = status
        self.response = response
