import os
import tempfile
import pytest
from click.testing import CliRunner
from unittest.mock import patch
from docs2llm.cli import main


@pytest.fixture
def runner():
    """Provides a Click test runner for CLI testing."""
    return CliRunner()


@pytest.fixture
def temp_dir():
    """Creates a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as td:
        yield td


def test_cli_help(runner):
    """Test the CLI help functionality."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Generate LLM context from documentation" in result.output
    assert "--git" in result.output
    assert "--output" in result.output
    assert "--max-depth" in result.output


def test_cli_missing_inputs(runner):
    """Test that the CLI shows an error when no inputs are provided."""
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    assert (
        "Error: Either a local path or --git option must be provided" in result.output
    )


def test_cli_conflicting_inputs(runner):
    """Test that the CLI shows an error when both local path and git repo are provided."""
    result = runner.invoke(
        main, ["local/path", "--git", "https://github.com/owner/repo.git"]
    )
    assert result.exit_code == 1
    assert "Error: Cannot specify both a local path and --git" in result.output


@patch("docs2llm.cli.extract_documentation")
def test_cli_local_path(mock_extract, runner, temp_dir):
    """Test CLI with local path input."""
    # Configure the mock to return True (success)
    mock_extract.return_value = True

    # Create a test directory
    test_dir = os.path.join(temp_dir, "test_docs")
    os.makedirs(test_dir)

    # Execute the CLI command
    result = runner.invoke(main, [test_dir, "--output", "test_output.txt"])

    # Verify CLI behavior
    assert result.exit_code == 0

    # Verify extract_documentation was called with correct arguments
    mock_extract.assert_called_once_with(
        local_path=test_dir,
        git_repo=None,
        output_file="test_output.txt",
        max_depth=3,
        branch=None,
        verbose=False,
        log_file=None,
    )


@patch("docs2llm.cli.extract_documentation")
def test_cli_git_repo(mock_extract, runner):
    """Test CLI with git repository input."""
    # Configure the mock to return True (success)
    mock_extract.return_value = True

    # Test URL
    test_repo = "https://github.com/owner/repo.git"

    # Execute the CLI command
    result = runner.invoke(
        main,
        [
            "--git",
            test_repo,
            "--output",
            "git_output.txt",
            "--branch",
            "main",
            "--verbose",
        ],
    )

    # Verify CLI behavior
    assert result.exit_code == 0

    # Verify extract_documentation was called with correct arguments
    mock_extract.assert_called_once_with(
        local_path=None,
        git_repo=test_repo,
        output_file="git_output.txt",
        max_depth=3,
        branch="main",
        verbose=True,
        log_file=None,
    )


@patch("docs2llm.cli.extract_documentation")
def test_cli_with_all_options(mock_extract, runner):
    """Test CLI with all available options."""
    # Configure the mock to return True (success)
    mock_extract.return_value = True

    # Execute the CLI command with all options
    result = runner.invoke(
        main,
        [
            "--git",
            "https://github.com/owner/repo.git",
            "--output",
            "full_options.txt",
            "--max-depth",
            "5",
            "--branch",
            "develop",
            "--verbose",
            "--log-file",
            "test.log",
        ],
    )

    # Verify CLI behavior
    assert result.exit_code == 0

    # Verify extract_documentation was called with correct arguments
    mock_extract.assert_called_once_with(
        local_path=None,
        git_repo="https://github.com/owner/repo.git",
        output_file="full_options.txt",
        max_depth=5,
        branch="develop",
        verbose=True,
        log_file="test.log",
    )


@patch("docs2llm.cli.extract_documentation")
def test_cli_failure_case(mock_extract, runner):
    """Test CLI when extraction fails."""
    # Configure the mock to return False (failure)
    mock_extract.return_value = False

    # Execute the CLI command
    result = runner.invoke(main, ["nonexistent/path"])

    # Verify CLI returns error code
    assert result.exit_code == 1
