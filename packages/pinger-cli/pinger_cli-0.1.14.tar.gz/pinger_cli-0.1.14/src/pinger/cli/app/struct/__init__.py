import typer
from pinger.app import app

app_sub = typer.Typer(no_args_is_help=True)


@app_sub.command("start")
def start():
    """
    Start local Docker Compose for development.
    """
    app().start()


@app_sub.command("restart")
def restart():
    """
    Restart local Docker Compose containers.
    """
    app().restart()


@app_sub.command("shell")
def shell():
    """
    Drop into a bash shell in the 'main' container, creating and starting it if necessary.
    """
    app().shell()


@app_sub.command("ci")
def ci():
    """
    build the application artifact

    Example:
        pinger app ci
    """
    app().ci()


@app_sub.command("cd")
def cd(
    env: str = typer.Argument(..., help="Name of the AWS profile/environment."),
    region: str = typer.Argument(..., help="AWS region for the ECS cluster."),
):
    """
    Deploy the latest ECS task definition in the environment's service.
    """
    app().cd(env, region)


@app_sub.command("scale")
def scale(
    env: str = typer.Argument(..., help="Name of the AWS profile/environment."),
    cluster: str = typer.Argument(..., help="ECS cluster name."),
    service: str = typer.Argument(..., help="ECS service name."),
    count: int = typer.Argument(..., help="Desired number of tasks."),
    region: str = typer.Argument(..., help="AWS region for the ECS cluster."),
):
    """
    Scale an ECS service to the specified number of tasks, then wait for stability.
    """
    app().scale(env, cluster, service, count, region)
