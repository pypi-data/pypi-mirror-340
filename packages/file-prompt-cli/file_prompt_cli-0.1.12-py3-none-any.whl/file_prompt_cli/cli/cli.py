import typer
from pathlib import Path
from typing import List, Optional, Set
from rich.console import Console
from rich.progress import Progress
from dotenv import load_dotenv, find_dotenv
import time
import glob
import os
import json
from google.cloud import storage
from google.cloud import pubsub_v1

# Load environment variables from .env file
load_dotenv()

from file_prompt_cli.core.dispatcher import JobDispatcher
from file_prompt_cli.gcp.uploader import GCSUploader
from file_prompt_cli.gcp.result_listener import ResultListener
from file_prompt_cli.config import Config

app = typer.Typer(
    name="file-prompt",
    help="Process files through LLMs using GCP and Gemini API",
    add_completion=False
)
console = Console()

def expand_file_patterns(patterns: List[str]) -> List[Path]:
    """Expand file patterns into a list of Path objects."""
    expanded_files = set()
    
    for pattern in patterns:
        # Handle both relative and absolute paths
        if os.path.isabs(pattern):
            matches = glob.glob(pattern, recursive=True)
        else:
            matches = glob.glob(pattern, recursive=True)
            # Convert to absolute paths
            matches = [os.path.abspath(match) for match in matches]
        
        # Filter out directories and add to set
        for match in matches:
            if os.path.isfile(match):
                expanded_files.add(Path(match))
    
    return sorted(list(expanded_files))

@app.command()
def process_files(
    files: List[str] = typer.Option(..., "--files", help="File paths or glob patterns (can be multiple)"),
    prompt: str = typer.Option(..., "--prompt", help="The prompt to process files with"),
    mode: str = typer.Option("auto", "--mode", help="Processing mode (text/image/auto)"),
    output_format: str = typer.Option("text", "--output-format", help="Output format (json/text/markdown)")
):
    """Process files through LLM with the given prompt.
    
    Files can be specified as:
    - Individual file paths: --files file1.txt --files file2.pdf
    - Wildcard patterns: --files "*.txt" --files "docs/*.pdf"
    - Multiple patterns: --files "*.txt" "*.pdf"
    """
    try:
        # Validate configuration
        Config.validate()
        
        # Expand file patterns
        file_paths = expand_file_patterns(files)
        
        if not file_paths:
            console.print("[bold red]No matching files found![/bold red]")
            raise typer.Exit(1)
            
        console.print(f"[bold green]Found {len(file_paths)} files to process[/bold green]")
        
        # Initialize components
        uploader = GCSUploader(Config.GCS_BUCKET_NAME)
        dispatcher = JobDispatcher()
        listener = ResultListener()

        # Track number of files processed and results received
        files_processed = 0
        results_received = 0

        with Progress() as progress:
            # Process and upload files
            task = progress.add_task("[cyan]Processing files...", total=len(file_paths))
            
            for file_path in file_paths:
                try:
                    # Upload to GCS
                    gcs_path = uploader.upload_file(file_path)
                    
                    # Create job with GCS path
                    dispatcher.create_job(
                        file_path=gcs_path,
                        prompt=prompt,
                        mode=mode
                    )
                    
                    files_processed += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    console.print(f"[bold red]Error processing {file_path}:[/bold red] {str(e)}")
                    continue
        
        if files_processed == 0:
            console.print("[bold red]No files were successfully processed![/bold red]")
            raise typer.Exit(1)
            
        # Listen for results
        console.print(f"\n[bold green]Waiting for results for {files_processed} files...[/bold green]")
        
        # Set a timeout for waiting (5 minutes)
        timeout = time.time() + 300  # 5 minutes from now
        all_results_received = False
        
        while not all_results_received and time.time() < timeout:
            try:
                for result in listener.listen():
                    # Process the result
                    if result.get('status') == 'error':
                        console.print(f"[bold red]Error processing result:[/bold red] {result.get('error', 'Unknown error')}")
                    else:
                        console.print(f"[bold green]Successfully processed result[/bold green]")
                    
                    results_received += 1
                    
                    # Check if we've received all results
                    if results_received >= files_processed:
                        all_results_received = True
                        break
                        
            except Exception as e:
                console.print(f"[bold red]Error receiving results:[/bold red] {str(e)}")
                break
        
        if all_results_received:
            console.print("\n[bold green]All results processed successfully![/bold green]")
        else:
            if time.time() >= timeout:
                console.print("\n[bold yellow]Timeout reached while waiting for results[/bold yellow]")
            console.print(f"\n[bold yellow]Processed {results_received} out of {files_processed} results[/bold yellow]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def load_env(
    env_file: str = typer.Option(
        None,
        "--env-file",
        "-e",
        help="Path to .env file to load. If not specified, looks for .env in current directory."
    ),
    override: bool = typer.Option(
        False,
        "--override",
        help="Override existing environment variables with values from the new .env file"
    )
):
    """Load environment variables from a specified .env file."""
    try:
        if env_file:
            env_path = Path(env_file)
            if not env_path.exists():
                console.print(f"[red]Error: .env file not found at {env_file}[/red]")
                raise typer.Exit(1)
        else:
            # Try to find .env file in current directory
            env_path = find_dotenv()
            if not env_path:
                console.print("[yellow]Warning: No .env file found in current directory[/yellow]")
                return

        # Load the environment variables
        load_dotenv(env_path, override=override)
        
        # Validate the loaded configuration
        try:
            Config.validate()
            console.print("[green]Successfully loaded and validated environment variables[/green]")
            console.print(f"[cyan]Loaded from: {env_path}[/cyan]")
        except ValueError as e:
            console.print(f"[red]Configuration validation failed: {str(e)}[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Error loading environment variables: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 