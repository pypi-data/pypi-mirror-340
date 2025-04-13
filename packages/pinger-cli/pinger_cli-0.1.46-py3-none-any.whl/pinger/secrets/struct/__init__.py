import subprocess
import typer
import yaml
import boto3
from pathlib import Path
from typing import Dict
from pinger.config import config


class Secrets:
    """
    Uploads decrypted secrets from SOPS-managed files into AWS SSM Parameter Store.
    """

    @classmethod
    def encrypt(cls, env: str):
        path = Path(f"{config().envs}/{env}/secrets.yaml").resolve()
        ssm_prefix = f"/{config().name}/{env}"

        typer.secho(
            f"[SECRETS] Loading encrypted secrets from: {path}", fg=typer.colors.CYAN
        )

        if not path.exists():
            typer.secho(
                f"✘ Secrets file not found: {path}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1)

        try:
            # Decrypt secrets using SOPS
            decrypted = subprocess.check_output(f"sops -d {path}", shell=True)
            secrets: Dict = yaml.safe_load(decrypted)
        except Exception as e:
            typer.secho(
                f"✘ Failed to decrypt secrets: {e}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1)

        ssm = boto3.Session(profile_name=env).client(
            "ssm", region_name=config().cd.region
        )

        typer.secho(
            f"[SECRETS] Uploading to Parameter Store with prefix: {ssm_prefix}\n",
            fg=typer.colors.BLUE,
        )

        for key, value in secrets.items():
            param_name = f"{ssm_prefix}/{key}"
            try:
                ssm.put_parameter(
                    Name=param_name,
                    Value=str(value),
                    Type="SecureString",
                    Overwrite=True,
                )
                typer.secho(f"✔ Uploaded secret: {param_name}", fg=typer.colors.GREEN)
            except Exception as e:
                typer.secho(
                    f"✘ Failed to upload {param_name}: {e}",
                    fg=typer.colors.RED,
                    err=True,
                )

        typer.secho(
            f"\n[SECRETS] Done uploading secrets for environment: {env}",
            fg=typer.colors.GREEN,
            bold=True,
        )
