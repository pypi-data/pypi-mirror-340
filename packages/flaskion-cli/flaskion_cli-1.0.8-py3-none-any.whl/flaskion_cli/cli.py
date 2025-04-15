import click
import os
import shutil
import subprocess
from jinja2 import Environment, FileSystemLoader

@click.group()
def cli():
    pass

@cli.command()
@click.argument("project_name")
def new(project_name):
    """
        🏗️ Create a new Flaskion project.

        This will:
        • Copy the default Flaskion template into a new folder
        • Initialise a Git repository
        • Create a virtual environment
        • Install dependencies via requirements.txt

        Example:
            flaskion new myapp
    """
    template_path = os.path.join(os.path.dirname(__file__), "flaskion_template")
    project_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_path):
        click.echo(f"❌ Project '{project_name}' already exists.")
        return

    shutil.copytree(template_path, project_path)
    subprocess.run(["git", "init"], cwd=project_path)
    subprocess.run(["python3", "-m", "venv", "venv"], cwd=project_path)
    subprocess.run(
        [os.path.join(project_path, "venv", "bin", "pip"), "install", "-r", "requirements.txt"],
        cwd=project_path,
    )

    click.echo(f"✅ Flaskion project '{project_name}' created!\n")
    click.echo(f"🚀 cd {project_name}\n   source venv/bin/activate\n   flask run")


@cli.command()
@click.argument("name")
def make_model(name):
    """
        🧱 Generate a new SQLAlchemy model.

        This will create:
        • A model file in app/models/
        • A basic model class with an auto-incrementing ID

        Example:
            flaskion make:model user
    """
    model_name = name.capitalize()
    table_name = name.lower() + "s"

    template_dir = os.path.join(os.path.dirname(__file__), "cli_templates")
    output_dir = os.path.join(os.getcwd(), "app", "models")
    output_file = os.path.join(output_dir, f"{name.lower()}.py")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("model_template.py.jinja")
    rendered = template.render(model_name=model_name, table_name=table_name)

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(rendered)

    click.echo(f"✅ Created model: {output_file}")


@cli.command()
@click.argument("name")
def make_controller(name):
    """
        🧭 Generate a new controller class.

        This creates:
        • A controller in app/controllers/
        • With static methods: index, create, show, update, delete
        • Using Flask's render_template flow

        Example:
            flaskion make:controller UserController
    """
    controller_name = name if name.endswith("Controller") else f"{name.capitalize()}Controller"
    resource_name = name.lower().replace("controller", "")
    resource_name_plural = resource_name + "s"

    template_dir = os.path.join(os.path.dirname(__file__), "cli_templates")
    output_dir = os.path.join(os.getcwd(), "app", "controllers")
    output_file = os.path.join(output_dir, f"{resource_name}_controller.py")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("controller_template.py.jinja")
    rendered = template.render(
        controller_name=controller_name,
        resource_name=resource_name,
        resource_name_plural=resource_name_plural
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(rendered)

    click.echo(f"✅ Created controller: {output_file}")


@cli.command()
@click.argument("name")
def make_schema(name):
    """
        🧬 Generate a new Marshmallow schema.

        This creates:
        • A schema in app/schemas/
        • Based on the SQLAlchemy model of the same name

        Example:
            flaskion make:schema user
    """
    model_name = name.capitalize()
    model_name_lower = name.lower()

    template_dir = os.path.join(os.path.dirname(__file__), "cli_templates")
    output_dir = os.path.join(os.getcwd(), "app", "schemas")
    output_file = os.path.join(output_dir, f"{model_name_lower}_schema.py")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("schema_template.py.jinja")
    rendered = template.render(
        model_name=model_name,
        model_name_lower=model_name_lower
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(rendered)

    click.echo(f"✅ Created schema: {output_file}")


@cli.command(name="new:mvc")
@click.argument("name")
@click.option("--api", is_flag=True, help="Generate API routes instead of web routes")
def new_mvc(name, api):
    """
    📦 Generate a new MVC resource with:
    
    - SQLAlchemy model
    - Class-based controller with index/create/show/update/delete
    - Marshmallow schema
    - Route definitions (appended to web_routes.py or api_routes.py)

    Example:
        flaskion new:mvc user
        flaskion new:mvc product --api
    """
    model_name = name.capitalize()
    resource_name = name.lower()
    resource_name_plural = resource_name + "s"
    controller_name = f"{model_name}Controller"

    template_dir = os.path.join(os.path.dirname(__file__), "cli_templates")
    env = Environment(loader=FileSystemLoader(template_dir))

    # Paths
    model_file = os.path.join("app", "models", f"{resource_name}.py")
    controller_file = os.path.join("app", "controllers", f"{resource_name}_controller.py")
    schema_file = os.path.join("app", "schemas", f"{resource_name}_schema.py")
    route_file = os.path.join("app", "routes", "api_routes.py" if api else "web_routes.py")

    # --- Generate Model ---
    model_template = env.get_template("model_template.py.jinja")
    with open(model_file, "w") as f:
        f.write(model_template.render(model_name=model_name, table_name=resource_name_plural))
    click.echo(f"✅ Created model: {model_file}")

    # --- Generate Controller ---
    controller_template = env.get_template("controller_template.py.jinja")
    with open(controller_file, "w") as f:
        f.write(controller_template.render(
            controller_name=controller_name,
            resource_name=resource_name,
            resource_name_plural=resource_name_plural
        ))
    click.echo(f"✅ Created controller: {controller_file}")

    # --- Generate Schema ---
    schema_template = env.get_template("schema_template.py.jinja")
    with open(schema_file, "w") as f:
        f.write(schema_template.render(model_name=model_name, model_name_lower=resource_name))
    click.echo(f"✅ Created schema: {schema_file}")

    # --- Append Routes ---
    route_template = env.get_template("api_route_template.py.jinja" if api else "web_route_template.py.jinja")
    route_code = route_template.render(
        controller_name=controller_name,
        resource_name=resource_name,
        resource_name_plural=resource_name_plural
    )

    os.makedirs(os.path.dirname(route_file), exist_ok=True)

    if not os.path.exists(route_file):
        with open(route_file, "w") as f:
            f.write("from flask import Blueprint\n\n")
            f.write(f"{'api' if api else 'web'}_routes = Blueprint('{resource_name}_routes', __name__)\n\n")

    # Add import if not already there
    with open(route_file, "r+") as f:
        contents = f.read()
        import_line = f"from app.controllers.{resource_name}_controller import {controller_name}"
        if import_line not in contents:
            f.seek(0, 0)
            f.write(import_line + "\n" + contents)

    # Append routes
    with open(route_file, "a") as f:
        f.write("\n" + route_code.strip() + "\n")
    click.echo(f"✅ Updated routes in: {route_file}")

if __name__ == "__main__":
    cli()