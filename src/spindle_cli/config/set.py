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
    if "=" not in key_value:
        raise typer.BadParameter(
            "Key-value pair must be in format 'KEY=VALUE'.", param_hint="'key_value'"
        )
    key, value = key_value.split("=", maxsplit=1)

    if "." not in key:
        raise typer.BadParameter(
            "Key must be in format 'SECTION.NAME'.", param_hint="'key_value'"
        )
    section, name = key.split(".", maxsplit=1)

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
