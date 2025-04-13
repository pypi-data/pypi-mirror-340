import typer
from pathlib import Path

app = typer.Typer()

BASE_DIRS = ["routers", "models", "schemas", "services"]

TEMPLATE = {
    "routers": """from fastapi import APIRouter

router = APIRouter()

@router.get("/{{name}}")
def get_{{name}}():
    return {"message": "{{name}} endpoint"}
""",

    "models": """# Pydantic or SQLAlchemy model placeholder for {{name}}

class {{Name|capitalize}}Model:
    pass
""",

    "schemas": """# Pydantic schema placeholder for {{name}}

class {{Name|capitalize}}Schema:
    pass
""",

    "services": """# Business logic for {{name}}

def get_all_{{name}}():
    return []
"""
}

def render_template(content: str, name: str) -> str:
    return content.replace("{{name}}", name).replace("{{Name|capitalize}}", name.capitalize())

@app.command()
def generate(name: str):
    """Generate CRUD structure for given name (router, model, schema, service)."""
    base_path = Path("app")

    for section in BASE_DIRS:
        section_dir = base_path / section / name
        section_dir.mkdir(parents=True, exist_ok=True)

        # create __init__.py
        (section_dir / "__init__.py").touch()

        # write the component file
        file_path = section_dir / f"{name}.py"
        content = render_template(TEMPLATE[section], name)
        file_path.write_text(content)

        try:
            relative = file_path.relative_to(Path.cwd())
        except ValueError:
            relative = file_path

        typer.echo(f"✅ Created: {relative}")

    # ✅ Add router to main.py
    main_path = Path("main.py")
    if main_path.exists():
        import_line = f"from app.routers.{name}.{name} import router as {name}_router\n"
        include_line = f"app.include_router({name}_router)\n"

        content = main_path.read_text()

        if import_line not in content:
            lines = content.splitlines()

            # Insert import after first block of imports
            import_index = next((i for i, line in enumerate(lines) if line.strip().startswith("from") or line.strip().startswith("import")), -1)
            lines.insert(import_index + 1, import_line.strip())

            # Insert include_router after apply_middlewares(app)
            inserted = False
            for i, line in enumerate(lines):
                if "apply_middlewares(app)" in line:
                    lines.insert(i + 1, include_line.strip())
                    inserted = True
                    break

            if not inserted:
                lines.append(include_line.strip())

            main_path.write_text("\n".join(lines))
            typer.echo(f"✅ Router '{name}' registered in main.py")
        else:
            typer.echo(f"⚠️  Router '{name}' already registered in main.py")