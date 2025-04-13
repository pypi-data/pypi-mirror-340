from typer.testing import CliRunner
from pyrtk.main import app
from pathlib import Path

runner = CliRunner()

def test_create_api_project():
    project_name = "testapi"

    with runner.isolated_filesystem():
        result = runner.invoke(app, ["create", project_name, "--type", "api"])
        project_path = Path(project_name)

        assert result.exit_code == 0
        assert f"Project '{project_name}' created successfully" in result.stdout
        assert project_path.exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "main.py").exists()
        assert (project_path / "app" / "routers").exists()

def test_create_ms_project():
    project_name = "testms"

    with runner.isolated_filesystem():
        result = runner.invoke(app, ["create", project_name, "--type", "ms"])
        project_path = Path(project_name)

        assert result.exit_code == 0
        assert f"Project '{project_name}' created successfully" in result.stdout
        assert project_path.exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "main.py").exists()
        assert (project_path / "app" / "core").exists()
        assert (project_path / "app" / "models").exists()
        assert (project_path / "app" / "routers").exists()