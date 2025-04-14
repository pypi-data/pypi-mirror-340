import pytest
from typer.testing import CliRunner

from fspacker.cli import app


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_cli_build_valid_dir(runner, tmp_path):
    result = runner.invoke(app, ["b", str(tmp_path)])
    assert result.exit_code == 0


def test_cli_build_invalid_dirpath(runner):
    result = runner.invoke(app, ["b", "invalid_dir"])
    assert result.exit_code == 0


def test_cli_build_invalid_filepath(runner, tmp_path):
    result = runner.invoke(app, ["b", str(tmp_path), "invalid_filepath"])
    assert result.exit_code == 2


def test_version_command(runner, mocker):
    mocker.patch("fspacker.__version__", "1.0.0")
    mocker.patch("fspacker.__build_date__", "2024-01-01")

    result = runner.invoke(app, ["v"])
    assert "fspacker 1.0.0" in result.stdout
    assert "构建日期: 2024-01-01" in result.stdout
    assert result.exit_code == 0


def test_run_command(runner, mocker, dir_examples):
    result = runner.invoke(app, ["r", str(dir_examples / "ex00_simple")])
    assert result.exit_code == 1

    result = runner.invoke(app, ["b", str(dir_examples / "ex00_simple")])
    assert result.exit_code == 0

    result = runner.invoke(app, ["r", str(dir_examples / "ex00_simple")])
    assert result.exit_code == 0
