import re
from configparser import ConfigParser
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


@app.command(name="set", help="Set the value of a configuration key.")
def set(
    ctx: typer.Context,
    key_value: Annotated[
        str,
        typer.Argument(
            help="Configuration key-value pair to set in format 'SECTION.NAME=VALUE'."
        ),
    ],
):
    m = re.fullmatch(r"([a-z]+)\.([a-z]+)=(.+)", key_value)
    if not m:
        raise typer.BadParameter(
            "Key-value pair must be in format 'SECTION.NAME=VALUE'.",
            param_hint="'key_value'",
        )
    section, name, value = m.groups()

    config: ConfigParser = ctx.obj["config"]
    if section not in config:
        raise typer.BadParameter(
            f"Section '{section}' not found in configuration.", param_hint="'key_value'"
        )
    if name not in config[section]:
        raise typer.BadParameter(
            f"Configuration value with name '{name}' not found in section '{section}'.",
            param_hint="'key_value'",
        )
    config[section][name] = value

    config_file: Path = ctx.obj["config_file"]
    with config_file.open("w") as f:
        config.write(f, space_around_delimiters=False)
