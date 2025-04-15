"""
docs2llm - Extract documentation from GitHub repositories for use with LLMs.

This package provides functionality to extract documentation from GitHub repositories
and format it for use as context with large language models.
"""

from docs2llm.main import (
    extract_documentation,  # noqa: F401
    setup_logging,  # noqa: F401
    is_documentation_file,  # noqa: F401
    markdown_to_text,  # noqa: F401
    clone_repository,  # noqa: F401
    find_documentation_files,  # noqa: F401
    process_documentation_files,  # noqa: F401
)

__version__ = "0.1.0"
