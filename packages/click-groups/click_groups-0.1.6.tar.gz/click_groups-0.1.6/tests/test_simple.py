import click
import pytest
from click.testing import CliRunner


import click
from click_groups import GroupedGroup


@pytest.fixture(scope="function")
def runner():
    return CliRunner()


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
    click.echo("Sub-command 1.")


@cli.command(help_group="Group 3")
def command_4():
    """Run a command."""


@cli.command()
def command_5():
    """Run a command."""


@cli.group()
def command_6():
    """Run a command."""


TEST_HELP = """Usage: cli [OPTIONS] COMMAND [ARGS]...

  Run commands.

Options:
  --help  Show this message and exit.

Group 1:
  command-high-priority (h,high)  Run a command.
  command-medium-priority (m,medium)
                                  Run a command.
  command-low-priority            Run a command.

Group 3:
  command-4  Run a command.

Commands:
  command-5  Run a command.
  command-3  Group command.
  command-6  Run a command.
"""

TEST_MEDIUM_PRIORITY = "Medium priority command.\n"
TEST_HIGH_PRIORITY = "High priority command.\n"
TEST_GROUP_PRIORITY = "Sub-command 1.\n"


def test_help(runner):
    result = runner.invoke(cli)
    assert result.output == TEST_HELP


@pytest.mark.parametrize("alias", ["command-high-priority", "high", "h"])
def test_high_priority(runner, alias):
    result = runner.invoke(cli, [alias])
    assert result.output == TEST_HIGH_PRIORITY


@pytest.mark.parametrize("alias", ["command-medium-priority", "medium", "m"])
def test_medium_priority(runner, alias):
    result = runner.invoke(cli, [alias])
    assert result.output == TEST_MEDIUM_PRIORITY


@pytest.mark.parametrize("alias", ["subcommand-1", "sub1"])
def test_group_priority(runner, alias):
    result = runner.invoke(cli, ["command-3", alias])
    assert result.output == TEST_GROUP_PRIORITY
