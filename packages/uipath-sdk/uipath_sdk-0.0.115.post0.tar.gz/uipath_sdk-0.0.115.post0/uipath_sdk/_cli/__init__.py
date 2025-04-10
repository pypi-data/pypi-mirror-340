import importlib.metadata
import sys
import warnings

import click

from uipath_sdk._cli.cli_auth import auth as auth  # type: ignore
from uipath_sdk._cli.cli_deploy import deploy as deploy  # type: ignore
from uipath_sdk._cli.cli_init import init as init  # type: ignore
from uipath_sdk._cli.cli_new import new as new  # type: ignore
from uipath_sdk._cli.cli_pack import pack as pack  # type: ignore
from uipath_sdk._cli.cli_publish import publish as publish  # type: ignore
from uipath_sdk._cli.cli_run import run as run  # type: ignore

warnings.warn(
    "DEPRECATED: This package is no longer maintained. Please use 'uipath' instead.",
    DeprecationWarning,
    stacklevel=2,
)


@click.group(invoke_without_command=True)
@click.version_option(
    importlib.metadata.version("uipath-sdk"),
    prog_name="uipath",
    message="%(prog)s version %(version)s",
)
@click.option(
    "-lv",
    is_flag=True,
    help="Display the current version of uipath-langchain.",
)
@click.option(
    "-v",
    is_flag=True,
    help="Display the current version of uipath-sdk.",
)
def cli(lv: bool, v: bool) -> None:
    if lv:
        try:
            version = importlib.metadata.version("uipath-langchain")
            click.echo(f"uipath-langchain version {version}")
        except importlib.metadata.PackageNotFoundError:
            click.echo("uipath-langchain is not installed", err=True)
            sys.exit(1)
    if v:
        try:
            version = importlib.metadata.version("uipath-sdk")
            click.echo(f"uipath-sdk version {version}")
        except importlib.metadata.PackageNotFoundError:
            click.echo("uipath-sdk is not installed", err=True)
            sys.exit(1)


cli.add_command(new)
cli.add_command(init)
cli.add_command(pack)
cli.add_command(publish)
cli.add_command(run)
cli.add_command(deploy)
cli.add_command(auth)
