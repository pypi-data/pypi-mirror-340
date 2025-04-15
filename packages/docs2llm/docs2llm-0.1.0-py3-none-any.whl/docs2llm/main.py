#!/usr/bin/env python3
import os
import sys
import re
import logging
import tempfile
from os.path import exists, isdir
import subprocess
import time
import markdown
from bs4 import BeautifulSoup
from rich.console import Console
from rich.logging import RichHandler


# Create a Rich console
console = Console()


def setup_logging(verbose=False, log_file=None, use_rich=True):
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear any existing handlers (important for module reuse)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler, using Rich if available
    if use_rich:
        console_handler = RichHandler(
            console=console, rich_tracebacks=True, show_time=False, show_path=False
        )
        root_logger.addHandler(console_handler)
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)
        logging.info(f"Logging to file: {log_file}")

    # Log initial message
    logging.debug("Logging initialized in DEBUG mode")
    logging.info("Documentation Extractor started")


def is_documentation_file(file_path):
    """Check if a file is likely to be documentation based on its name and extension."""
    file_name = os.path.basename(file_path)

    doc_patterns = [
        r"\.md$",
        r"\.rst$",
        r"\.txt$",
        r"README",
        r"GUIDE",
        r"TUTORIAL",
        r"DOCUMENTATION",
        r"DOCS",
        r"MANUAL",
    ]

    # Skip binary files and certain non-documentation files
    skip_patterns = [
        r"\.jpg$",
        r"\.jpeg$",
        r"\.png$",
        r"\.gif$",
        r"\.pdf$",
        r"\.exe$",
        r"\.dll$",
        r"\.so$",
        r"\.dylib$",
        r"\.jar$",
        r"\.zip$",
        r"\.tar$",
        r"\.gz$",
        r"\.git",  # Skip .git directories
    ]

    for pattern in skip_patterns:
        if re.search(pattern, file_name, re.IGNORECASE):
            return False

    for pattern in doc_patterns:
        if re.search(pattern, file_name, re.IGNORECASE):
            return True
    return False


def markdown_to_text(markdown_content):
    """Convert markdown to plain text while preserving structure."""
    try:
        # Convert markdown to HTML
        html = markdown.markdown(markdown_content, extensions=["tables", "fenced_code"])

        # Use BeautifulSoup to extract text from HTML
        soup = BeautifulSoup(html, "html.parser")

        # Preserve code blocks
        for pre in soup.find_all("pre"):
            code_text = pre.get_text()
            pre.replace_with(f"\n```\n{code_text}\n```\n")

        # Extract text
        text = soup.get_text()

        # Clean up the text
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text
    except Exception as e:
        logging.error(f"Error converting markdown to text: {e}")
        return markdown_content  # Return original content if conversion fails


def clone_repository(repo_path, temp_dir, branch=None):
    """Clone a GitHub repository to a local directory.

    Args:
        repo_path: GitHub repository URL or owner/repo format
        temp_dir: Directory to clone the repository into
        branch: Specific branch to clone (default: main branch)
    """
    # Check if the repo_path is a full URL or just owner/repo
    if repo_path.startswith(("http://", "https://")):
        clone_url = repo_path
        # Extract owner/repo from URL for display purposes
        if "github.com" in repo_path:
            # Handle URLs like https://github.com/owner/repo.git
            parts = repo_path.split("github.com/")
            if len(parts) > 1:
                owner_repo = parts[1].replace(".git", "")
            else:
                owner_repo = repo_path  # Fallback
        else:
            owner_repo = repo_path  # Non-GitHub URL
    else:
        # Traditional owner/repo format (for backward compatibility)
        clone_url = f"https://github.com/{repo_path}.git"
        owner_repo = repo_path

    logging.info(f"Cloning repository {clone_url} to temporary directory")

    start_time = time.time()

    try:
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([clone_url, temp_dir])

        with console.status(f"[bold blue]Cloning {owner_repo}...", spinner="dots"):
            # Execute git clone command
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Capture output for logging
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logging.error(f"Git clone failed: {stderr}")
                raise Exception(f"Failed to clone repository: {stderr}")

        end_time = time.time()
        logging.info(
            f"Clone completed successfully in {end_time - start_time:.2f} seconds"
        )

        # Log repository size information
        repo_size = get_directory_size(temp_dir)
        logging.info(f"Repository size: {repo_size / 1024 / 1024:.2f} MB")

        return True, owner_repo

    except Exception as e:
        logging.error(f"Error during clone: {str(e)}")
        return False, None


def get_directory_size(path):
    """Calculate the total size of a directory in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp) and os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size


def find_documentation_files(repo_dir, max_depth=3):
    """Find all documentation files in the repository."""
    doc_files = []

    logging.info(f"Searching for documentation files (max depth: {max_depth})")

    # Skip .git directory
    with console.status("[bold blue]Scanning repository...", spinner="dots") as status:
        # Walk the directory tree
        for root, dirs, files in os.walk(repo_dir):
            # Remove .git directory from traversal
            if ".git" in dirs:
                dirs.remove(".git")

            # Check if we've reached max depth
            rel_path = os.path.relpath(root, repo_dir)
            current_depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1

            if current_depth > max_depth:
                logging.debug(f"Skipping {rel_path} (exceeds max depth)")
                # Clear dirs to prevent further traversal down this path
                dirs.clear()
                continue

            # Log current directory being processed
            if current_depth > 0:
                logging.debug(
                    f"Scanning directory: {rel_path} (depth {current_depth}/{max_depth})"
                )
                status.update(f"[bold blue]Scanning: {rel_path}")

            # Special attention to 'docs' directories
            if os.path.basename(root).lower() == "docs":
                logging.info(f"Found docs directory: {rel_path}")
                status.update(f"[bold green]Found docs directory: {rel_path}")

            # Process each file in directory
            for file in files:
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, repo_dir)

                if is_documentation_file(file_path):
                    logging.debug(f"Found documentation file: {rel_file_path}")
                    doc_files.append(rel_file_path)

        status.update("[bold green]Scanning complete")

    logging.info(f"Found {len(doc_files)} documentation files")
    return doc_files


def process_documentation_files(repo_dir, doc_files):
    """Process all found documentation files into a single text document."""
    docs_text = []

    # Sort files to prioritize READMEs and key documentation
    sorted_files = sorted(
        doc_files,
        key=lambda x: (
            0
            if "readme" in x.lower()
            else 1
            if "docs" in x.lower() or "/docs/" in x.lower()
            else 2
        ),
    )

    logging.info(f"Processing {len(doc_files)} documentation files")

    with console.status(
        "[bold blue]Processing documentation files...", spinner="dots"
    ) as status:
        file_count = 0

        for file_path in sorted_files:
            full_path = os.path.join(repo_dir, file_path)
            try:
                file_count += 1
                status.update(
                    f"[cyan]Processing: {file_path} ({file_count}/{len(doc_files)})"
                )
                logging.debug(f"Processing {file_path}...")

                # Read file content
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                # Convert content based on file type
                if file_path.lower().endswith(".md"):
                    logging.debug(f"Converting markdown to text for {file_path}")
                    text = markdown_to_text(content)
                else:
                    # For non-markdown files, just use the raw content
                    logging.debug(f"Using raw content for {file_path}")
                    text = content

                # Add file information and content to the docs_text
                docs_text.append(f"\n\n{'=' * 80}\n{file_path}\n{'=' * 80}\n\n")
                docs_text.append(text)

                logging.debug(
                    f"Successfully processed {file_path} ({len(text)} characters)"
                )

            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}", exc_info=True)

        status.update("[bold green]Processing complete")

    total_length = sum(len(text) for text in docs_text)
    logging.info(f"Total documentation size: {total_length} characters")
    return "\n".join(docs_text)


def extract_documentation(
    local_path=None,
    git_repo=None,
    output_file="llm_context.txt",
    max_depth=3,
    branch=None,
    verbose=False,
    log_file=None,
):
    """Extract documentation from a local directory or a GitHub repository.

    Args:
        local_path: Path to a local directory containing documentation
        git_repo: GitHub repository in the format 'owner/repo'
        output_file: Path to save the extracted documentation
        max_depth: Maximum directory depth to search
        branch: Specific branch to clone (only used with git_repo)
        verbose: Enable verbose logging
        log_file: Path to a file where logs will be written in addition to the console

    Returns:
        bool: True if the extraction was successful, False otherwise
    """
    # Setup logging
    setup_logging(verbose=verbose, log_file=log_file)

    # Determine if we're using a local path or git repo
    is_local = local_path is not None

    try:
        if is_local:
            # Using local directory
            if not exists(local_path):
                logging.error(f"Local path does not exist: {local_path}")
                return False

            if not isdir(local_path):
                logging.error(f"Path is not a directory: {local_path}")
                return False

            logging.info(f"Using local directory: {local_path}")

            # Process the local directory
            doc_files = find_documentation_files(local_path, max_depth)

            if not doc_files:
                logging.warning("No documentation files found in the directory.")
                return False

            # Process the documentation files
            docs_text = process_documentation_files(local_path, doc_files)

            # Create header for local directory
            dir_name = os.path.basename(os.path.abspath(local_path))
            header = f"""# Documentation from local directory: {local_path}
This file contains documentation extracted from the local directory {local_path}.
It is formatted for use as context with large language models.

## Directory Information
- Directory: {dir_name}
- Extraction Date: {time.strftime("%Y-%m-%d %H:%M:%S")}

## TABLE OF CONTENTS:
{chr(10).join([f"* {file}" for file in doc_files])}

"""
        else:
            # Using GitHub repository
            with tempfile.TemporaryDirectory() as temp_dir:
                logging.debug(f"Created temporary directory: {temp_dir}")

                # Clone the repository
                success, owner_repo = clone_repository(git_repo, temp_dir, branch)
                if not success:
                    logging.error("Repository cloning failed. Exiting.")
                    return False

                # Find documentation files
                doc_files = find_documentation_files(temp_dir, max_depth)

                if not doc_files:
                    logging.warning("No documentation files found in the repository.")
                    return False

                # Process the documentation files into a single text document
                docs_text = process_documentation_files(temp_dir, doc_files)

                # Add a header with repository information and table of contents
                header = f"""# Documentation for {owner_repo}
This file contains documentation extracted from the GitHub repository {owner_repo}.
It is formatted for use as context with large language models.

## Repository Information
- Repository: {owner_repo}
- Extraction Date: {time.strftime("%Y-%m-%d %H:%M:%S")}

## TABLE OF CONTENTS:
{chr(10).join([f"* {file}" for file in doc_files])}

"""

        # Write the result to a file
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(header + docs_text)
        except IOError as e:
            logging.error(f"Failed to write to file {output_file}: {e}")
            return False

        file_size_kb = os.path.getsize(output_file) / 1024

        console.print(f"[bold green]Documentation saved to [blue]{output_file}[/blue]")
        console.print(f"[bold green]Total size: [yellow]{file_size_kb:.1f}[/yellow] KB")

        if file_size_kb > 2000:
            console.print(
                f"[bold yellow]Warning: The output file is large ({file_size_kb:.1f} KB). "
                f"This may exceed context limits for some LLMs.[/bold yellow]"
            )

        return True

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return False
