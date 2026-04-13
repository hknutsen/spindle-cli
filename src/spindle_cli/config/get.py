import re
from configparser import ConfigParser
from typing import Annotated

import typer

app = typer.Typer()


@app.command(name="get", help="Get a configuration value.")
def get(
    ctx: typer.Context,
    key: Annotated[
        str,
        typer.Argument(
            help="Key of the configuration value to get in format 'SECTION.NAME'."
        ),
    ],
):
    m = re.fullmatch(r"([a-z]+)\.([a-z]+)", key)
    if not m:
        raise typer.BadParameter(
            "Key must be in format 'SECTION.NAME'.", param_hint="'key'"
        )
    section, name = m.groups()

    config: ConfigParser = ctx.obj["config"]
    if section not in config:
        raise typer.BadParameter(
            f"Section '{section}' not found in configuration.", param_hint="'key'"
        )

    items = config[section]
    if name not in items:
        raise typer.BadParameter(
            f"Configuration value with name '{name}' not found in section '{section}'.",
            param_hint="'key'",
        )

    value = items[name]
    print(value)
