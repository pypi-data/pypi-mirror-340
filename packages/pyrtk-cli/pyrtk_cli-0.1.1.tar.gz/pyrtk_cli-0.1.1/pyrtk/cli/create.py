import typer
from pyrtk.scaffold.api import create_api_structure
from pyrtk.scaffold.ms import create_ms_structure

app = typer.Typer(help="Create a new FastAPI API or Microservice project.")

@app.command()
def project(
    name: str = typer.Argument(..., help="Name of the new project"),
    type: str = typer.Option(..., "--type", "-t", help="Project type: 'api' or 'ms'")
):
    """
    Scaffold a new FastAPI project with the specified structure.
    """
    type = type.lower()

    if type not in ["api", "ms"]:
        typer.echo("❌ Invalid project type. Use --type api or --type ms")
        raise typer.Exit(code=1)

    typer.echo(f"🔨 Creating {type.upper()} project: {name}...")

    try:
        if type == "api":
            create_api_structure(name)
        elif type == "ms":
            create_ms_structure(name)

        typer.echo(f"✅ Project '{name}' created successfully.")
    
    except FileExistsError:
        typer.echo(f"⚠️  The folder '{name}' already exists.")
        raise typer.Exit(code=1)