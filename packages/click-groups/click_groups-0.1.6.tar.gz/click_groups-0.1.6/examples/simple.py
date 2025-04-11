"""Simple app."""

import click
from click_groups import GroupedGroup


@click.group(cls=GroupedGroup)
def cli():
    """Run commands."""


@cli.command(help_group="Group 1", priority=10)
def command_low_priority():
    """Run a command."""
    click.echo("Low priority command.")


@cli.command(help_group="Group 1", aliases=["medium", "m"])
def command_medium_priority():
    """Run a command."""
    click.echo("Medium priority command.")


@cli.command(help_group="Group 1", priority=0, aliases=["high", "h"])
def command_high_priority():
    """Run a command."""
    click.echo("High priority command.")


@cli.group(help_group="Group 2")
def command_3():
    """Group command."""


@command_3.command(help_group="Group 2", aliases=["sub1"])
def subcommand_1():
    """Run a command."""


@cli.command(help_group="Group 3")
def command_4():
    """Run a command."""


@cli.command()
def command_5():
    """Run a command."""


@cli.group()
def command_6():
    """Run a command."""


if __name__ == "__main__":
    cli()
