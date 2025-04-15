import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock, mock_open
import logging

from docs2llm.main import (
    setup_logging,
    is_documentation_file,
    markdown_to_text,
    find_documentation_files,
    process_documentation_files,
    extract_documentation,
    clone_repository,
    get_directory_size,
)


@pytest.fixture
def temp_dir():
    """Creates a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as td:
        yield td


class TestSetupLogging:
    """Tests for the setup_logging function."""

    @patch("docs2llm.main.RichHandler")
    @patch("logging.getLogger")
    def test_setup_logging_basic(self, mock_get_logger, mock_rich_handler):
        """Test basic logging setup."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logging(verbose=False)

        # Verify logger was configured properly
        mock_get_logger.assert_called_once()
        mock_logger.setLevel.assert_called_once_with(logging.INFO)
        mock_logger.addHandler.assert_called()

    @patch("docs2llm.main.RichHandler")
    @patch("logging.getLogger")
    def test_setup_logging_verbose(self, mock_get_logger, mock_rich_handler):
        """Test verbose logging setup."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logging(verbose=True)

        # Verify logger was configured with DEBUG level
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

    @patch("docs2llm.main.RichHandler")
    @patch("logging.FileHandler")
    @patch("logging.getLogger")
    def test_setup_logging_with_file(
        self, mock_get_logger, mock_file_handler, mock_rich_handler
    ):
        """Test logging setup with file output."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        log_file = "test.log"
        setup_logging(verbose=False, log_file=log_file)

        # Verify file handler was created
        mock_file_handler.assert_called_once_with(log_file, mode="w")
        assert (
            mock_logger.addHandler.call_count >= 2
        )  # At least console and file handlers


class TestIsDocumentationFile:
    """Tests for the is_documentation_file function."""

    def test_identifies_markdown_files(self):
        """Test that markdown files are identified as documentation."""
        assert is_documentation_file("readme.md") is True
        assert is_documentation_file("docs/guide.md") is True
        assert is_documentation_file("some/path/with/DOCUMENTATION.md") is True

    def test_identifies_other_doc_files(self):
        """Test that other documentation file types are identified."""
        assert is_documentation_file("README.rst") is True
        assert is_documentation_file("GUIDE.txt") is True
        assert is_documentation_file("README") is True
        assert is_documentation_file("docs/TUTORIAL") is True

    def test_rejects_binary_files(self):
        """Test that binary files are not identified as documentation."""
        assert is_documentation_file("image.jpg") is False
        assert is_documentation_file("image.png") is False
        assert is_documentation_file("archive.zip") is False
        assert is_documentation_file("program.exe") is False

    def test_rejects_git_files(self):
        """Test that git files are not identified as documentation."""
        assert is_documentation_file(".git/config") is False


class TestMarkdownToText:
    """Tests for the markdown_to_text function."""

    def test_converts_basic_markdown(self):
        """Test basic markdown conversion."""
        markdown_content = "# Title\n\nThis is a paragraph."
        result = markdown_to_text(markdown_content)
        assert "Title" in result
        assert "This is a paragraph." in result

    def test_preserves_code_blocks(self):
        """Test that code blocks are preserved."""
        markdown_content = "```python\ndef test():\n    pass\n```"
        result = markdown_to_text(markdown_content)
        assert "```" in result
        assert "def test():" in result

    @patch("markdown.markdown")
    def test_handles_markdown_conversion_error(self, mock_markdown):
        """Test handling of markdown conversion errors."""
        mock_markdown.side_effect = Exception("Markdown error")
        markdown_content = "# Problem content"
        result = markdown_to_text(markdown_content)
        # Should return original content on error
        assert result == markdown_content


class TestCloneRepository:
    """Tests for the clone_repository function."""

    @patch("subprocess.Popen")
    @patch("docs2llm.main.get_directory_size")
    def test_clone_with_full_url(self, mock_get_size, mock_popen):
        """Test cloning with a full URL."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = ("output", "")
        mock_popen.return_value = process_mock
        mock_get_size.return_value = 1024 * 1024  # 1MB

        # Call the function
        success, repo_name = clone_repository(
            "https://github.com/owner/repo.git", "/tmp/repo"
        )

        # Verify
        assert success is True
        assert repo_name == "owner/repo"
        mock_popen.assert_called_once()
        assert "git" in mock_popen.call_args[0][0]
        assert "clone" in mock_popen.call_args[0][0]

    @patch("subprocess.Popen")
    @patch("docs2llm.main.get_directory_size")
    def test_clone_with_owner_repo_format(self, mock_get_size, mock_popen):
        """Test cloning with owner/repo format."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = ("output", "")
        mock_popen.return_value = process_mock
        mock_get_size.return_value = 1024 * 1024  # 1MB

        # Call the function
        success, repo_name = clone_repository("owner/repo", "/tmp/repo")

        # Verify
        assert success is True
        assert repo_name == "owner/repo"
        mock_popen.assert_called_once()
        assert "https://github.com/owner/repo.git" in mock_popen.call_args[0][0]

    @patch("subprocess.Popen")
    def test_clone_with_branch(self, mock_popen):
        """Test cloning a specific branch."""
        # Setup mock
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = ("output", "")
        mock_popen.return_value = process_mock

        # Call the function
        clone_repository("owner/repo", "/tmp/repo", branch="develop")

        # Verify branch was specified
        cmd = mock_popen.call_args[0][0]
        assert "--branch" in cmd
        assert "develop" in cmd

    @patch("subprocess.Popen")
    def test_clone_failure(self, mock_popen):
        """Test handling of clone failure."""
        # Setup mock to simulate failure
        process_mock = MagicMock()
        process_mock.returncode = 1
        process_mock.communicate.return_value = ("", "error message")
        mock_popen.return_value = process_mock

        # Call the function
        success, repo_name = clone_repository("owner/repo", "/tmp/repo")

        # Verify
        assert success is False
        assert repo_name is None


class TestFindDocumentationFiles:
    """Tests for the find_documentation_files function."""

    def test_find_docs_in_empty_directory(self, temp_dir):
        """Test finding docs in an empty directory."""
        result = find_documentation_files(temp_dir)
        assert len(result) == 0

    def test_find_docs_with_markdown_files(self, temp_dir):
        """Test finding markdown files."""
        # Create test files
        readme_path = os.path.join(temp_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write("# Test README")

        result = find_documentation_files(temp_dir)
        assert len(result) == 1
        assert "README.md" in result[0]

    def test_respects_max_depth(self, temp_dir):
        """Test that max_depth is respected."""
        # Create a deep directory structure
        deep_dir = os.path.join(temp_dir, "level1", "level2", "level3", "level4")
        os.makedirs(deep_dir)

        # Create files at different depths
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write("# Root README")

        with open(os.path.join(temp_dir, "level1", "guide.md"), "w") as f:
            f.write("# Level 1 Guide")

        with open(os.path.join(deep_dir, "deep.md"), "w") as f:
            f.write("# Deep documentation")

        # Find with max_depth=2
        result = find_documentation_files(temp_dir, max_depth=2)

        # Should include files at depth 0 and 1, but not at depth 4
        assert any("README.md" in file for file in result)
        assert any("level1/guide.md" in file for file in result)
        assert not any("deep.md" in file for file in result)

    def test_skips_git_directory(self, temp_dir):
        """Test that .git directory is skipped."""
        # Create .git directory with a file
        git_dir = os.path.join(temp_dir, ".git")
        os.makedirs(git_dir)
        with open(os.path.join(git_dir, "config"), "w") as f:
            f.write("[core]\n\trepositoryformatversion = 0")

        # Create a valid doc file
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write("# README")

        result = find_documentation_files(temp_dir)

        # Should find README.md but not .git/config
        assert len(result) == 1
        assert "README.md" in result[0]


class TestProcessDocumentationFiles:
    """Tests for the process_documentation_files function."""

    @patch("docs2llm.main.markdown_to_text")
    @patch("builtins.open", new_callable=mock_open, read_data="# Test content")
    def test_processes_markdown_files(self, mock_file, mock_markdown_to_text):
        """Test processing of markdown files."""
        mock_markdown_to_text.return_value = "Test content"

        result = process_documentation_files(
            "/tmp/repo", ["README.md", "docs/guide.md"]
        )

        # Verify files were opened and processed
        assert mock_file.call_count == 2
        assert mock_markdown_to_text.call_count == 2

        # Verify output formatting
        assert "README.md" in result
        assert "docs/guide.md" in result
        assert "Test content" in result

    @patch("builtins.open", side_effect=IOError("File not found"))
    @patch("logging.error")
    def test_handles_file_errors(self, mock_logging_error, mock_file):
        """Test handling of file read errors."""
        # In this case, we expect an empty string to be returned
        # but the function should not crash
        result = process_documentation_files("/tmp/repo", ["missing.md"])

        # Verify error was logged
        mock_logging_error.assert_called()
        assert isinstance(result, str)

    @patch("builtins.open", new_callable=mock_open, read_data="# File content")
    def test_sorts_readme_first(self, mock_file):
        """Test that README files are sorted first."""
        doc_files = ["some/random/doc.md", "README.md", "docs/guide.md"]

        result = process_documentation_files("/tmp/repo", doc_files)

        # Since our mocked files all return the same content,
        # we need to check that the file names are in the order we expect
        file_sections = result.split("=")
        # The first section is empty, so we start from the second
        assert len(file_sections) > 1
        # README should be processed before other files
        readme_index = -1
        other_file_index = -1

        for i, section in enumerate(file_sections):
            if "README.md" in section:
                readme_index = i
            if "random/doc.md" in section:
                other_file_index = i

        # If both files are found, README should come before other files
        if readme_index != -1 and other_file_index != -1:
            assert readme_index < other_file_index


class TestExtractDocumentation:
    """Tests for the extract_documentation function."""

    @patch("docs2llm.main.setup_logging")
    @patch("docs2llm.main.find_documentation_files")
    @patch("docs2llm.main.process_documentation_files")
    @patch("os.path.getsize")
    @patch(
        "docs2llm.main.exists", return_value=True
    )  # Patching the direct import from os.path
    @patch(
        "docs2llm.main.isdir", return_value=True
    )  # Patching the direct import from os.path
    @patch("builtins.open", new_callable=mock_open)
    def test_extract_from_local_path(
        self,
        mock_file,
        mock_isdir,
        mock_exists,
        mock_getsize,
        mock_process,
        mock_find,
        mock_setup_logging,
    ):
        """Test extraction from a local path."""
        # Setup mocks
        mock_find.return_value = ["README.md", "docs/guide.md"]
        mock_process.return_value = "Documentation content"
        mock_getsize.return_value = 1024  # 1KB

        # Call function
        result = extract_documentation(
            local_path="/tmp/local", output_file="output.txt"
        )

        # Verify
        assert result is True
        mock_setup_logging.assert_called_once()
        mock_find.assert_called_once_with("/tmp/local", 3)
        mock_process.assert_called_once()
        mock_file.assert_called()

    @patch("docs2llm.main.setup_logging")
    @patch("tempfile.TemporaryDirectory")
    @patch("docs2llm.main.clone_repository")
    @patch("docs2llm.main.find_documentation_files")
    @patch("docs2llm.main.process_documentation_files")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_extract_from_git_repo(
        self,
        mock_file,
        mock_getsize,
        mock_process,
        mock_find,
        mock_clone,
        mock_temp_dir,
        mock_setup_logging,
    ):
        """Test extraction from a git repository."""
        # Setup mocks
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/git_repo"
        mock_clone.return_value = (True, "owner/repo")
        mock_find.return_value = ["README.md", "docs/guide.md"]
        mock_process.return_value = "Documentation content"
        mock_getsize.return_value = 1024  # 1KB

        # Call function
        result = extract_documentation(git_repo="owner/repo", output_file="output.txt")

        # Verify
        assert result is True
        mock_setup_logging.assert_called_once()
        mock_clone.assert_called_once_with("owner/repo", "/tmp/git_repo", None)
        mock_find.assert_called_once_with("/tmp/git_repo", 3)
        mock_process.assert_called_once()
        mock_file.assert_called()

    @patch("docs2llm.main.setup_logging")
    @patch("os.path.exists")
    def test_nonexistent_local_path(self, mock_exists, mock_setup_logging):
        """Test handling of nonexistent local path."""
        mock_exists.return_value = False

        # Call function
        result = extract_documentation(
            local_path="/nonexistent/path", output_file="output.txt"
        )

        # Verify
        assert result is False

    @patch("docs2llm.main.setup_logging")
    @patch("tempfile.TemporaryDirectory")
    @patch("docs2llm.main.clone_repository")
    def test_clone_failure(self, mock_clone, mock_temp_dir, mock_setup_logging):
        """Test handling of git clone failure."""
        # Setup mocks
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/git_repo"
        mock_clone.return_value = (False, None)

        # Call function
        result = extract_documentation(git_repo="owner/repo", output_file="output.txt")

        # Verify
        assert result is False

    @patch("docs2llm.main.setup_logging")
    @patch("os.path.exists")
    @patch("os.path.isdir")
    @patch("docs2llm.main.find_documentation_files")
    def test_no_documentation_files(
        self, mock_find, mock_isdir, mock_exists, mock_setup_logging
    ):
        """Test handling when no documentation files are found."""
        # Setup mocks
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_find.return_value = []

        # Call function
        result = extract_documentation(
            local_path="/path/with/no/docs", output_file="output.txt"
        )

        # Verify
        assert result is False


def test_get_directory_size(temp_dir):
    """Test the get_directory_size function."""
    # Create test files
    with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
        f.write("a" * 100)  # 100 bytes

    with open(os.path.join(temp_dir, "file2.txt"), "w") as f:
        f.write("b" * 200)  # 200 bytes

    # Create subdirectory with file
    subdir = os.path.join(temp_dir, "subdir")
    os.makedirs(subdir)
    with open(os.path.join(subdir, "file3.txt"), "w") as f:
        f.write("c" * 300)  # 300 bytes

    # Get size
    size = get_directory_size(temp_dir)

    # Should be approximately 600 bytes (with small possible overhead)
    assert 600 <= size <= 650
