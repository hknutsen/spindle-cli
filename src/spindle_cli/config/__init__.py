import typer

from .list import app as list_app

app = typer.Typer(name="config", help="Configure spindle.")
app.add_typer(list_app)
