from configparser import ConfigParser
from pathlib import Path

import typer

from .config import app as config_app

app = typer.Typer(
    help="A command-line interface for syncing your music library to multiple audio formats.",
    no_args_is_help=True,
)
app.add_typer(config_app)


@app.callback()
def main(ctx: typer.Context) -> None:
    home = Path.home()
    spindle_dir = home / ".spindle"
    spindle_dir.mkdir(exist_ok=True)

    config_file = spindle_dir / "config.ini"
    config = ConfigParser()
    if config_file.is_file():
        # Read config from existing file
        config.read(config_file)
    else:
        # Create config file
        config["flac"] = {"dir": str(home / "Music/FLAC")}
        config["ogg"] = {
            "dir": str(home / "Music/Ogg Vorbis"),
            "quality": "6",
            "resample": "44100",
        }
        config["opus"] = {
            "dir": str(home / "Music/Ogg Opus"),
            "bitrate": "128",
            "vbr": "true",
        }
        with open(config_file, "w") as f:
            config.write(f, space_around_delimiters=False)

    ctx.ensure_object(dict)
    ctx.obj["config_file"] = config_file
    ctx.obj["config"] = config


if __name__ == "__main__":
    app()
