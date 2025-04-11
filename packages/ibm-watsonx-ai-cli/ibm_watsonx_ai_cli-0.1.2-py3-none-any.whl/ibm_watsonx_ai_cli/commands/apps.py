#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2025.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import typer

cli = typer.Typer(no_args_is_help=True)


@cli.command(help="List playground app samples.")
def list() -> None:
    raise NotImplementedError


@cli.command(
    help="Creates a demo playground app for the service. [OPTIONAL ARGS: name] if only one user do not need to pass name."
)
def new() -> None:
    raise NotImplementedError


@cli.command(
    help="Start the playground app. [OPTIONAL ARGS: name] if not provided, take from current dir."
)
def run() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    cli()
