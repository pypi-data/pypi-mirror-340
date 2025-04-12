import platform
import subprocess
import sys
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def run():
    """Run your FastAPI project using Uvicorn and the local virtual environment."""
    current_dir = Path.cwd()
    project_name = current_dir.name
    venv_path = current_dir / f"{project_name}-venv"

    python_path = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )

    if not python_path.exists():
        print(f"❌ Virtual environment not found at: {venv_path}")
        raise typer.Exit(code=1)

    if not (current_dir / "main.py").exists():
        print("❌ 'main.py' not found in the project root.")
        raise typer.Exit(code=1)

    print("🚀 Launching Uvicorn server...\n")

    try:
        subprocess.run(
            [str(python_path), "-m", "uvicorn", "main:app", "--reload"],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=sys.stdin
        )
    except subprocess.CalledProcessError:
        print("❌ Failed to start Uvicorn.")
        raise typer.Exit(code=1)