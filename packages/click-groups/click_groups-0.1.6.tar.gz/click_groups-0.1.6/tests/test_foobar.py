import click
import pytest
from click.testing import CliRunner

from click_groups import GroupedGroup, _click7


@pytest.fixture(scope="function")
def runner():
    return CliRunner()


@click.group(cls=GroupedGroup)
def cli():
    pass


@cli.command(aliases=["bar"])
def foo():
    click.echo("foo")


TEST_HELP = """Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  foo (bar)
"""


def test_help(runner):
    result = runner.invoke(cli)
    assert result.output == TEST_HELP


def test_foobar(runner):
    for cmd in ["foo", "bar"]:
        result = runner.invoke(cli, [cmd])
        assert result.output == "foo\n"


TEST_INVALID = """Usage: cli [OPTIONS] COMMAND [ARGS]...
{}
Error: No such command 'baz'.
""".format("Try 'cli --help' for help.\n" if _click7 else "")


def test_invalid(runner):
    result = runner.invoke(cli, ["baz"])
    assert result.output == TEST_INVALID
