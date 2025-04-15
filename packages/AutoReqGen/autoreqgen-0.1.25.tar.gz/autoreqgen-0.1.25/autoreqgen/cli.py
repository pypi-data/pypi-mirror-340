import typer
import json
import subprocess
import platform
import sys
from pathlib import Path

from autoreqgen import scanner, requirements, formatter, docgen, utils

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = typer.Typer(help="🚀 AutoReqGen – Smarter Python dependency and tooling assistant.",
                  add_completion=True,
                  pretty_exceptions_show_locals=False)


@app.command()
def scan(
    path: Path = typer.Argument(..., help="Path to your Python project"),
    all: bool = typer.Option(False, "--all", help="Include local and standard library modules"),
    as_json: bool = typer.Option(False, "--as-json", help="Output results in JSON format")
):
    """Scan the project and list all imported packages."""
    utils.print_banner()
    imports = scanner.extract_all_imports(str(path)) if all else scanner.scan_project_for_imports(str(path))
    imports = sorted(imports)

    if as_json:
        typer.echo(json.dumps(imports, indent=2))
    else:
        for imp in imports:
            typer.echo(f"📦 {imp}")
        typer.echo(f"\n✅ Found {len(imports)} unique imports.")


@app.command()
def generate(
    path: Path = typer.Argument(..., help="Path to your Python project"),
    output: str = typer.Option("requirements.txt", help="Output file name"),
    with_versions: bool = typer.Option(True, help="Include version numbers in requirements.txt")
):
    """Generate requirements.txt with or without versions."""
    utils.print_banner()
    imports = scanner.scan_project_for_imports(str(path))
    requirements.generate_requirements(imports, output_file=output, with_versions=with_versions)


@app.command()
def format(
    tool: str = typer.Argument(..., help="Choose from: black, isort, autopep8"),
    path: Path = typer.Argument(".", help="Target path for formatting")
):
    """Format code using Black, isort, or autopep8."""
    utils.print_banner()
    if not utils.is_tool_installed(tool):
        typer.echo(f"❌ Error: `{tool}` is not installed.")
        raise typer.Exit(code=1)
    formatter.run_formatter(tool, str(path))


@app.command()
def docs(
    path: Path = typer.Argument(..., help="Path to your Python code"),
    output: str = typer.Option("DOCUMENTATION.md", help="Output Markdown file"),
    include_private: bool = typer.Option(False, "--include-private", help="Include private functions and classes")
):
    """Generate documentation from docstrings."""
    utils.print_banner()
    docgen.generate_docs(str(path), output_file=output, include_private=include_private)


@app.command()
def add(package: str, path: Path = Path("requirements.txt")):
    """Install a package and add it to requirements.txt (without version pinning)."""
    utils.print_banner()
    typer.echo(f"📦 Installing {package}...")
    result = subprocess.run(["pip", "install", package], capture_output=True, text=True)
    if result.returncode != 0:
        typer.echo(f"❌ Failed to install {package}:\n{result.stderr}")
        raise typer.Exit(code=1)

    if not path.exists():
        typer.echo(f"📄 Creating {path}...")
        path.touch()

    with open(path, "r") as f:
        lines = {line.strip().lower() for line in f if line.strip()}
    lines.add(package.lower())

    with open(path, "w") as f:
        for pkg in sorted(lines):
            f.write(pkg + "\n")

    typer.echo(f"✅ {package} added to {path} (sorted & deduplicated)")


@app.command()
def freeze(output: str = "requirements.txt"):
    """Freeze the current environment and write exact package versions to a file."""
    utils.print_banner()
    typer.echo(f"📄 Freezing environment to {output}...")
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    if result.returncode != 0:
        typer.echo(f"❌ Failed to freeze environment:\n{result.stderr}")
        raise typer.Exit(code=1)

    frozen = list(set(line.strip() for line in result.stdout.splitlines() if line.strip()))
    frozen_sorted = sorted(frozen, key=str.lower)
    with open(output, "w") as f:
        f.write("\n".join(frozen_sorted) + "\n")

    typer.echo(f"✅ Environment frozen, sorted, and saved to {output}")


@app.command()
def start():
    """Create a new virtual environment by selecting Python version and name."""
    utils.print_banner()

    if "google.colab" in sys.modules:
        typer.echo("⚠️  Virtual environment creation is not supported in Google Colab.")
        raise typer.Exit(code=1)

    env_name = typer.prompt("Enter a name for your virtual environment")
    command = "where python" if platform.system() == "Windows" else "which -a python"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    python_paths = [line.strip() for line in result.stdout.splitlines() if "python" in line.lower()]

    if not python_paths:
        typer.echo("❌ No Python executables found.")
        raise typer.Exit(code=1)

    typer.echo("\nAvailable Python versions:")
    for i, path in enumerate(python_paths):
        typer.echo(f"  [{i + 1}] {path}")

    choice = typer.prompt("Choose Python version (number)", type=int)
    selected_python = python_paths[choice - 1]

    typer.echo(f"\n🐍 Creating virtual environment `{env_name}` with {selected_python}...")
    result = subprocess.run([selected_python, "-m", "venv", env_name], capture_output=True, text=True)

    if result.returncode == 0:
        typer.echo(f"✅ Virtual environment `{env_name}` created successfully.")
        if platform.system() == "Windows":
            typer.echo(f"💡 Activate it with: .\\{env_name}\\Scripts\\activate")
        else:
            typer.echo(f"💡 Activate it with: source ./{env_name}/bin/activate")
    else:
        typer.echo(f"❌ Failed to create virtual environment:\n{result.stderr}")


@app.command()
def watch(
    path: Path = typer.Argument(".", help="Path to watch for changes"),
    requirements_file: Path = typer.Option("requirements.txt", help="Requirements file to update")
):
    """Watch for changes in Python files and auto-update requirements."""
    utils.print_banner()
    typer.echo(f"👀 Watching {path} for changes...")

    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        typer.echo("⚙️ Installing missing dependency: watchdog")
        subprocess.run(["pip", "install", "watchdog"])
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

    class ImportChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith(".py"):
                typer.echo(f"\n🔁 Change detected: {event.src_path}")
                imports = scanner.scan_project_for_imports(str(path))
                requirements.generate_requirements(imports, output_file=requirements_file, with_versions=True)
                typer.echo(f"✅ Updated {requirements_file}.")

    observer = Observer()
    observer.schedule(ImportChangeHandler(), str(path), recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        typer.echo("\n👋 Stopped watching.")
    observer.join()


if __name__ == "__main__":
    app()
