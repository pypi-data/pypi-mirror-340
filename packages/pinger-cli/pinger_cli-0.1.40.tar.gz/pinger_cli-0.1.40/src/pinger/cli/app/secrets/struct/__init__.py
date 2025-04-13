import typer
from pinger.app import app

secrets_app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


@secrets_app.command("edit")
def edit(env):
    """
    edit secrets with your $EDITOR
    """
    app().edit(env)
