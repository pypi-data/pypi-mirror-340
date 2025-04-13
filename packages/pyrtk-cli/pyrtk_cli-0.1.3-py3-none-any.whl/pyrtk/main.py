import typer
from pyrtk.cli.create import create
from pyrtk.cli.run import run
from pyrtk.cli.generate import generate
# from pyrtk.cli.docs import docs

app = typer.Typer(
    help="PyRTK - Python REST Toolkit CLI"
)

# Comandos simples registrados (sin subgrupos)
app.command()(create)
app.command()(run)
app.command()(generate)

def main() -> None:
    """CLI entrypoint."""
    app()

if __name__ == "__main__":
    main()