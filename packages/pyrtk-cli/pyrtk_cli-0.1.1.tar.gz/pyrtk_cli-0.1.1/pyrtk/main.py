import typer
from pyrtk.cli import create, run

app = typer.Typer(
    help="PyRTK - Python REST Toolkit CLI"
)

# Registrar comandos
app.add_typer(create.app, name="create")
app.add_typer(run.app, name="run")

def main() -> None:
    """CLI entrypoint."""
    app()

if __name__ == "__main__":
    main()