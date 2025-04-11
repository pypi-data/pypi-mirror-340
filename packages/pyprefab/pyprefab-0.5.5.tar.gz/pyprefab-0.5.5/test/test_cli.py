"""Test the pyprefab cli."""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from pyprefab.cli import app  # type: ignore


@pytest.mark.parametrize(
    'cli_inputs, expected_dirs',
    [
        (['--name', 'pytest_package', '--author', 'Py Test'], ['.github', 'src', 'test']),
        (['--name', 'pytest_package', '--author', 'Py Test', '--docs'], ['.github', 'docs', 'src', 'test']),
    ],
)
def test_pyprefab_cli(tmp_path, cli_inputs, expected_dirs):
    runner = CliRunner()
    package_dir = tmp_path / 'test_cli'

    result = runner.invoke(
        app,
        cli_inputs + ['--dir', package_dir],
        input='""\n',
    )
    assert result.exit_code == 0
    assert package_dir.exists()

    # package directory populated with template output contains expected folders
    dir_count = 0
    dir_names = []
    for child in package_dir.iterdir():
        if child.is_dir():
            dir_names.append(child.name)
            dir_count += 1
    assert dir_count == len(expected_dirs)
    assert set(dir_names) == set(expected_dirs)


def test_invalid_package_name(tmp_path):
    """Package name must be a valid Python identifier."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest-package', '--author', 'Py Test', '--dir', tmp_path],
        input='This is a test package\n',
    )
    assert result.exit_code != 0


def test_error_cleanup(tmp_path):
    """Error when creating a package should trigger cleanup."""
    package_dir = tmp_path / 'test_error'
    with patch('pyprefab.cli.render_templates', side_effect=Exception('Test exception')):
        runner = CliRunner()
        result = runner.invoke(
            app,
            ['--name', 'pytest_package', '--description', '', '--dir', package_dir],
            input='Py Test\n',
        )
    assert result.exit_code != 0
    # pyprefab should remove package directory if an error occurs
    assert package_dir.exists() is False


def test_error_existing_data(tmp_path):
    """If there are existing files in package directory, pyprefab should fail."""

    package_dir = tmp_path / 'test_existing_data'
    package_dir.mkdir()
    (package_dir / 'existing_file.txt').touch()

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_package', '--author', 'Py Test', '--description', 'new package', '--dir', package_dir],
        input='y\n',
    )
    assert result.exit_code != 0


def test_existing_data_exception(tmp_path):
    """If existing files in package directory are on the exception list, pyprefab should create the package."""

    package_dir = tmp_path / 'test_existing_data'
    (package_dir / '.git').mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_package', '--author', 'Py Test', '--description', 'new package', '--dir', package_dir],
        input='y\n',
    )
    assert result.exit_code == 0


def test_existing_data_exception_and_no_exception(tmp_path):
    """If there's a mix of allowed and not allowed existing files in the package directory, pyprefab should fail."""

    package_dir = tmp_path / 'test_existing_data'
    (package_dir / '.git').mkdir(parents=True, exist_ok=True)
    (package_dir / 'logs').mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_package', '--author', 'Py Test', '--description', 'new package', '--dir', package_dir],
        input='y\n',
    )
    assert result.exit_code != 0
