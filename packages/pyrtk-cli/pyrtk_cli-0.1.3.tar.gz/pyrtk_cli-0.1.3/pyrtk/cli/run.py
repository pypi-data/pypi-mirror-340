# pyrtk/cli/run.py
import typer
from pyrtk.internal import run_logic

app = typer.Typer(help="Run your PyRTK project with Uvicorn.")

@app.command()
def run():
    """
    Start the FastAPI server.
    """
    run_logic.run()