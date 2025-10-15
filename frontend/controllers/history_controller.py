from .api_client import APIClient

class HistoryController:
    def __init__(self):
        self.history = APIClient.get_history()

    def add_history(self, item):
        result = APIClient.add_history(item)
        if result:
            self.history.append(result)
        return result

    def get_history(self):
        self.history = APIClient.get_history()
        return self.history
