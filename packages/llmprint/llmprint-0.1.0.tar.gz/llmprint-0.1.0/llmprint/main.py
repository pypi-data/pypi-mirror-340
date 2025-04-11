import argparse
import io
import os
from pathlib import Path

import pyperclip

# Common .gitignore-style patterns
GITIGNORE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "env/",
    "venv/",
    ".venv/",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    ".ipynb_checkpoints",
    ".tox/",
    ".nox/",
    ".coverage",
    ".cache",
    "build/",
    "dist/",
    "*.egg-info/",
    "*.egg",
    "node_modules/",
    "npm-debug.log",
    "yarn-debug.log",
    "yarn-error.log",
    "yarn.lock",
    "package-lock.json",
    "*.class",
    "*.jar",
    "*.war",
    "*.ear",
    "*.iml",
    "*.ipr",
    "*.iws",
    ".gradle/",
    "target/",
    ".idea/",
    ".project",
    "*.o",
    "*.out",
    "*.obj",
    "*.exe",
    "*.dll",
    "*.so",
    "*.dylib",
    "Debug/",
    "Release/",
    "*.log",
    "*.tmp",
    "*.swp",
    "*.sublime-workspace",
    "*.bak",
    "*.orig",
    "*.rej",
    "*~",
    ".DS_Store",
    ".AppleDouble",
    "._*",
    "Thumbs.db",
    "ehthumbs.db",
    "Desktop.ini",
    "$RECYCLE.BIN/",
    ".git",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".gitkeep",
    ".vscode/",
    ".vs/",
    "*.code-workspace",
    ".env",
    ".pytest_cache/",
    ".mypy_cache/",
    "coverage.xml",
    "*.sqlite3",
    "*.db",
    "*.lock",
    "tmp/",
    "cache/",
    ".svn/",
]


def should_ignore(path: Path, exclude_patterns: list) -> bool:
    for pattern in GITIGNORE_PATTERNS + exclude_patterns:
        try:
            if path.is_file():
                if pattern.endswith("/"):
                    continue
                if (
                    path.match(pattern)
                    or path.match("*/" + pattern)
                    or path.match("**/" + pattern)
                    or path.name == pattern
                ):
                    return True
            else:
                if (
                    path.match(pattern)
                    or path.match("*/" + pattern)
                    or path.match("**/" + pattern)
                    or path.name == pattern
                    or any(part == pattern.rstrip("/") for part in path.parts)
                ):
                    return True
        except Exception:
            continue
    return False


def print_tree_structure(base_path, exclude_patterns, prefix="", output_buffer=None, quiet=False):
    if should_ignore(base_path, exclude_patterns):
        return

    entries = sorted(base_path.iterdir(), key=lambda e: (e.is_file(), e.name))
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        content = f"{prefix}{connector}{entry.name}\n"
        if output_buffer is not None:
            output_buffer.write(content)
        if not quiet:
            print(content, end="")
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree_structure(entry, exclude_patterns, prefix + extension, output_buffer, quiet)


def print_file_contents(base_path, include_dirs, exclude_patterns, output_buffer=None, quiet=False):
    if not include_dirs:
        for root, dirs, files in os.walk(base_path):
            current_path = Path(root)
            dirs[:] = [d for d in dirs if not should_ignore(current_path / d, exclude_patterns)]
            for file in files:
                file_path = current_path / file
                if not should_ignore(file_path, exclude_patterns):
                    _print_file_content(file_path, base_path, output_buffer, quiet)
        return

    for include_path in include_dirs:
        path = base_path / include_path
        if path.is_file():
            if not should_ignore(path, exclude_patterns):  # Fixed: Use should_ignore consistently
                _print_file_content(path, base_path, output_buffer, quiet)
            continue
        if path.is_dir():
            for root, dirs, files in os.walk(path):
                current_path = Path(root)
                dirs[:] = [d for d in dirs if not should_ignore(current_path / d, exclude_patterns)]
                for file in files:
                    file_path = current_path / file
                    if not should_ignore(file_path, exclude_patterns):
                        _print_file_content(file_path, base_path, output_buffer, quiet)


def _print_file_content(file_path: Path, base_path: Path, output_buffer=None, quiet=False) -> None:
    content = f"{file_path.relative_to(base_path)}\n"
    content += "-" * 40 + "\n"
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content += f.read()
    except Exception as e:
        content += f"Error reading file: {e}"
    content += "\n" + "=" * 40 + "\n"

    if output_buffer is not None:
        output_buffer.write(content)
    if not quiet:
        print(content, end="")


def main():
    parser = argparse.ArgumentParser(
        prog="llmprint",
        description=(
            "A CLI tool that prints directory structures and file contents in a clean, LLM-friendly format. "
            "Perfect for generating context when working with chatbots or code assistants. "
            "By default, it skips common development artifacts using .gitignore-style rules."
        ),
        epilog=(
            "Examples:\n"
            "  Print directory structure:    $ llmprint -s\n"
            "  Print specific directories:   $ llmprint -i src/ tests/\n"
            "  Exclude directories:          $ llmprint -i . -e node_modules dist\n"
            '  Exclude by pattern:           $ llmprint -s -e "*.md" "*.pyc"\n'
            "  Print tree structure:         $ llmprint\n"
            "  Print all files in current:   $ llmprint .\n"
            "  Copy to clipboard:            $ llmprint -s -c\n"
            "  Copy and also print:          $ llmprint -s -c -p\n"
            "\nFor more information, visit: https://github.com/rsh3khar/llmprint"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to process when no --include flag is specified. If empty, uses current directory.",
    )
    parser.add_argument(
        "-i",
        "--include",
        nargs="*",
        default=[],
        help="Specify paths to include in the output. Can be files or directories. Takes precedence over positional paths.",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="*",
        default=[],
        help="Paths to exclude from the output. Supports glob patterns (e.g., *.pyc, __pycache__).",
    )
    parser.add_argument(
        "-s",
        "--structure",
        action="store_true",
        help="Only print the directory structure as a tree, without file contents.",
    )
    parser.add_argument(
        "-c", "--copy", action="store_true", help="Copy the output to clipboard (suppresses stdout by default).",
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Print to stdout (when using --copy, output is suppressed by default).",
    )

    args = parser.parse_args()
    if not any(vars(args).values()):
        args.structure = True

    include_dirs = args.include if args.include else args.paths
    exclude_patterns = args.exclude
    base_path = Path.cwd()

    # Determine if we should be quiet (copy without print)
    quiet = args.copy and not args.print

    # Use StringIO to capture output if copying is requested
    output_buffer = io.StringIO() if args.copy else None

    if args.structure:
        if include_dirs:
            for path in include_dirs:
                target_path = base_path / path
                if target_path.exists():
                    content = f"{target_path.relative_to(base_path)}/\n"
                    if output_buffer:
                        output_buffer.write(content)
                    if not quiet:
                        print(content, end="")
                    print_tree_structure(target_path, exclude_patterns, output_buffer=output_buffer, quiet=quiet)
                else:
                    if not quiet:
                        print(f"Path not found: {path}")
        else:
            content = f"{base_path.name}/\n"
            if output_buffer:
                output_buffer.write(content)
            if not quiet:
                print(content, end="")
            print_tree_structure(base_path, exclude_patterns, output_buffer=output_buffer, quiet=quiet)
    else:
        print_file_contents(base_path, include_dirs, exclude_patterns, output_buffer, quiet)

    if args.copy:
        try:
            content = output_buffer.getvalue()
            pyperclip.copy(content)
            # Always show what was copied
            if args.structure:
                if include_dirs:
                    paths = ", ".join(str(p) for p in include_dirs)
                    print(f"\nCopied tree structure of: {paths}")
                else:
                    print(f"\nCopied tree structure of current directory")
            else:
                if include_dirs:
                    paths = ", ".join(str(p) for p in include_dirs)
                    print(f"\nCopied contents of: {paths}")
                else:
                    print(f"\nCopied contents of current directory")

            # Show size info
            lines = content.count("\n")
            chars = len(content)
            print(f"({lines:,} lines, {chars:,} characters copied to clipboard)")
        except Exception as e:
            print(f"\nFailed to copy to clipboard: {e}")  # Always show errors
        finally:
            output_buffer.close()


if __name__ == "__main__":
    main()
