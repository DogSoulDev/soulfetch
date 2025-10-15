class EnvironmentModel:
    def __init__(self, name, variables=None):
        self.name = name
        self.variables = variables or {}
