# src/pinger/cli/app/cd/struct/__init__.py

import typer

from pinger.app import app

cd_app = typer.Typer(no_args_is_help=True)


@cd_app.command("list")
def list():
    """
    list deployable environments for this application
    """
    envs = app().list_deployable_environments()
    if not envs:
        raise typer.Exit(code=0)

    for e in envs:
        print(f"- {e}")
