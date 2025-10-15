from frontend.controllers.environment_import_export import EnvironmentImportExport
from frontend.models.environment_model import EnvironmentModel
import os
import tempfile

def test_import_export_environments():
    envs = [EnvironmentModel(name="dev", variables={"API_KEY": "123"})]
    tmp = os.path.join(tempfile.gettempdir(), "envs.json")
    EnvironmentImportExport.export_environments(envs, tmp)
    loaded = EnvironmentImportExport.import_environments(tmp)
    assert len(loaded) == 1
    assert loaded[0].name == "dev"
    assert loaded[0].variables["API_KEY"] == "123"
