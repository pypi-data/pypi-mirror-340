#!/usr/bin/env python3
import sys
import click
from docs2llm.main import extract_documentation, console


@click.command()
@click.argument("path", required=False)
@click.option(
    "--git", help="GitHub repository URL (e.g., https://github.com/owner/repo.git)"
)
@click.option("--output", default="llm_context.txt", help="Output file name")
@click.option(
    "--max-depth", type=int, default=3, help="Maximum directory depth to search"
)
@click.option("--branch", help="Specific branch to clone (only used with --git)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--log-file", help="Log to this file in addition to console")
def main(path, git, output, max_depth, branch, verbose, log_file):
    """Generate LLM context from documentation in a directory or GitHub repository.

    PATH: Local directory path containing documentation files

    You can either provide a local path or use --git with a GitHub repository URL.
    Example: --git https://github.com/owner/repo.git
    """
    if not path and not git:
        console.print(
            "[bold red]Error: Either a local path or --git option must be provided.[/bold red]"
        )
        sys.exit(1)

    if path and git:
        console.print(
            "[bold red]Error: Cannot specify both a local path and --git. Choose one input source.[/bold red]"
        )
        sys.exit(1)

    success = extract_documentation(
        local_path=path,
        git_repo=git,
        output_file=output,
        max_depth=max_depth,
        branch=branch,
        verbose=verbose,
        log_file=log_file,
    )

    # Exit without any success/failure message
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
