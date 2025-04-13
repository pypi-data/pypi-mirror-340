import typer

# import yaml
# from pathlib import Path
# from pinger.config import config
from pinger.app import app

env_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@env_app.command("deployable")
def deployable():
    """
    list deployable environments
    """
    app().list_deployable_environments()
