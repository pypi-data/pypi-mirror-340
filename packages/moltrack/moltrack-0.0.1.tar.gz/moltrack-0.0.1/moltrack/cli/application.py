"""Command line application."""

import typer

import moltrack

app = typer.Typer()


@app.command()
def about() -> None:
    """Display the package's tagline."""
    typer.echo(moltrack.__doc__)


@app.command()
def version() -> None:
    """Display the package's version."""
    typer.echo(moltrack.__version__)
