import typer
import os
import json
import csv
from time import sleep
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.align import Align
from extractor import extract_iocs_from_text
from utils import read_file
import pyfiglet

app = typer.Typer(help="🔥 AI IOC Hunter - Extract IOC indicators from files or directories.")
console = Console()

SUPPORTED_FORMATS = ["json", "csv", "txt"]

APP_NAME = "AI IOC Hunter"
VERSION = "v1.0"
SUBTITLE = "Extract IPs, Domains, URLs, Hashes, and Emails from files 🔥"

def print_banner():
    """Print CLI banner with ASCII app name and subtitle"""
    # Generate ASCII art for app name
    ascii_banner = pyfiglet.figlet_format(APP_NAME, font="slant")
    
    # Combine ASCII art with version and subtitle
    banner_text = f"[bold cyan]{ascii_banner}[/bold cyan][yellow]{VERSION}[/yellow]\n[italic]{SUBTITLE}[/italic]"
    
    # Create a panel
    panel = Panel(Align.center(banner_text), expand=True, border_style="green")
    console.print(panel)

    

def save_results(results, output_file, output_format):
    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
    elif output_format == "csv":
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "IOC_type", "IOC_value"])
            for file, iocs in results.items():
                for key, values in iocs.items():
                    for val in values:
                        writer.writerow([file, key, val])
    elif output_format == "txt":
        with open(output_file, "w", encoding="utf-8") as f:
            for file, iocs in results.items():
                f.write(f"File: {file}\n")
                for key, values in iocs.items():
                    f.write(f"{key}: {', '.join(values)}\n")
                f.write("\n")
    console.print(f"[green]Results saved to {output_file}[/green]")

def gather_files(path: str, recursive: bool = False):
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        if recursive:
            for root, _, filenames in os.walk(path):
                for name in filenames:
                    files.append(os.path.join(root, name))
        else:
            for name in os.listdir(path):
                file_path = os.path.join(path, name)
                if os.path.isfile(file_path):
                    files.append(file_path)
    return files

def tail_file(file_path):
    """Yield new lines in real-time (like tail -f)"""
    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                sleep(0.5)
                continue
            yield line.strip()

@app.command()
def scan(
    path: str = typer.Argument(..., help="Path to file or folder"),
    output: str = typer.Option("ioc_results.json", "--output", "-o", help="Output file name"),
    format: str = typer.Option("json", "--format", "-f", help="Output format", show_default=True),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursively scan folders"),
    tail: bool = typer.Option(False, "--tail", "-t", help="Tail a file (live monitoring)")
):
    """
    Scan file(s) and extract IOC indicators (IP, DOMAIN, URL, HASH, EMAIL).
    """
    print_banner()
    
    output = str(output)
    format = format.lower()
    if format not in SUPPORTED_FORMATS:
        console.print(f"[red]Unsupported format: {format}[/red]")
        raise typer.Exit(code=1)

    if tail:
        if not os.path.isfile(path):
            console.print(f"[red]Tail mode requires a file, not a folder: {path}[/red]")
            raise typer.Exit(code=1)
        console.print(f"[yellow]Tailing file: {path}[/yellow]")
        for line in tail_file(path):
            iocs = extract_iocs_from_text(line)
            if iocs:
                console.print(f"[blue]{line}[/blue]")
                console.print(f"[green]{iocs}[/green]")
        return

    files = gather_files(path, recursive)
    if not files:
        console.print(f"[red]No files found in path: {path}[/red]")
        raise typer.Exit(code=1)

    results = {}
    console.print(f"[cyan]Scanning {len(files)} file(s)...[/cyan]")

    for file_path in track(files, description="Processing files..."):
        try:
            text = read_file(file_path)
            iocs = extract_iocs_from_text(text)
            if iocs:
                results[os.path.basename(file_path)] = iocs
        except Exception as e:
            console.print(f"[red]Failed to process {file_path}: {e}[/red]")

    save_results(results, output, format)


if __name__ == "__main__":
    app()
