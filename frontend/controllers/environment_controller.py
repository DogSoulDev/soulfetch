from .api_client import APIClient

class EnvironmentController:
    def __init__(self):
        self.environments = APIClient.get_environments()

    def add_environment(self, env):
        result = APIClient.create_environment(env)
        if result:
            self.environments.append(result)
        return result

    def get_environments(self):
        self.environments = APIClient.get_environments()
        return self.environments
