import requests

class APIClient:
    import os
    BASE_URL = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")

    @staticmethod
    def execute_request(method, url, body, headers=None, params=None):
        try:
            payload = {
                "method": method,
                "url": url,
                "headers": headers or {},
                "params": params or {},
                "body": body
            }
            response = requests.post(f"{APIClient.BASE_URL}/execute", json=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_collections():
        try:
            response = requests.get(f"{APIClient.BASE_URL}/collections")
            return response.json()
        except Exception as e:
            return []

    @staticmethod
    def create_collection(collection):
        try:
            response = requests.post(f"{APIClient.BASE_URL}/collections", json=collection)
            return response.json()
        except Exception as e:
            return None

    @staticmethod
    def get_history():
        try:
            response = requests.get(f"{APIClient.BASE_URL}/history")
            return response.json()
        except Exception as e:
            return []

    @staticmethod
    def add_history(item):
        try:
            response = requests.post(f"{APIClient.BASE_URL}/history", json=item)
            return response.json()
        except Exception as e:
            return None

    @staticmethod
    def get_environments():
        try:
            response = requests.get(f"{APIClient.BASE_URL}/environments")
            return response.json()
        except Exception as e:
            return []

    @staticmethod
    def create_environment(env):
        try:
            response = requests.post(f"{APIClient.BASE_URL}/environments", json=env)
            return response.json()
        except Exception as e:
            return None
