import typer

from .get import app as get_app
from .list import app as list_app

app = typer.Typer(name="config", help="Configure spindle.", no_args_is_help=True)
app.add_typer(get_app)
app.add_typer(list_app)
