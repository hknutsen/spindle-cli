from configparser import ConfigParser

import typer

app = typer.Typer()


@app.command(name="list", help="List configuration values.")
def list(ctx: typer.Context):
    config: ConfigParser = ctx.obj["config"]
    for section in config.sections():
        for name, value in config[section].items():
            print(f"{section}.{name}={value}")
