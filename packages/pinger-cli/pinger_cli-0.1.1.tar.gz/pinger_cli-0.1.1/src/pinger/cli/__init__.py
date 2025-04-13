import typer
from pinger.cli.app.struct import app_sub
from pinger.cli.infra.struct import infra_sub

this_cli = typer.Typer(no_args_is_help=True)


this_cli.add_typer(app_sub, name="app")
this_cli.add_typer(infra_sub, name="infra")


def main():
    this_cli()


if __name__ == "__main__":
    main()
