from frontend.models.environment_model import EnvironmentModel

def test_environment_model_init():
    env = EnvironmentModel(name="dev", variables={"API_KEY": "123"})
    assert env.name == "dev"
    assert env.variables["API_KEY"] == "123"
