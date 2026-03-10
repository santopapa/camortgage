from typer.testing import CliRunner
from camortgage.cli import app

runner = CliRunner()


def test_rates_help():
    result = runner.invoke(app, ["rates", "--help"])
    assert result.exit_code == 0
    assert "refresh" in result.output.lower()


def test_qualify_help():
    result = runner.invoke(app, ["qualify", "--help"])
    assert result.exit_code == 0
    assert "income" in result.output.lower()


def test_compare_help():
    result = runner.invoke(app, ["compare", "--help"])
    assert result.exit_code == 0
    assert "income" in result.output.lower()
