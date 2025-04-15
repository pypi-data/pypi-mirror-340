import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress
import glob
import os
import threading
from queue import Queue

from file_prompt_cli.gcp.uploader import GCSUploader
from file_prompt_cli.gcp.pubsub_client import PubSubClient
from file_prompt_cli.gcp.result_listener import ResultListener

# Initialize Typer app
app = typer.Typer(
    name="file-prompt",
    help="Dispatch files to GCP Pub/Sub and listen for results",
    add_completion=False
)

# Initialize console for rich output
console = Console()

def validate_file_paths(file_paths: List[str]) -> List[Path]:
    """Validate and convert file paths to Path objects."""
    valid_paths = []
    for path in file_paths:
        path_obj = Path(path)
        if not path_obj.exists():
            console.print(f"[red]Error: File not found: {path}[/red]")
            continue
        valid_paths.append(path_obj)
    return valid_paths

def dispatch_job_thread(
    files: List[Path],
    prompt: str,
    project_id: str,
    bucket_name: str,
    topic_name: str,
    progress_queue: Queue
):
    """Thread function for dispatching jobs."""
    try:
        # Initialize components
        uploader = GCSUploader(bucket_name)
        pubsub_client = PubSubClient(project_id, topic_name)
        
        # Process files
        for file_path in files:
            try:
                # Upload file to GCS
                gcs_path = uploader.upload_file(file_path)
                
                # Dispatch job
                job_id = pubsub_client.publish_job(
                    file_path=gcs_path,
                    prompt=prompt
                )
                
                progress_queue.put(("dispatched", file_path))
                
            except Exception as e:
                progress_queue.put(("error", f"Error dispatching {file_path}: {str(e)}"))
                continue
        
        progress_queue.put(("done", None))
        
    except Exception as e:
        progress_queue.put(("error", f"Dispatch thread error: {str(e)}"))

def listen_thread(
    project_id: str,
    subscription_name: str,
    timeout: int,
    verbose: bool,
    progress_queue: Queue
):
    """Thread function for listening to results."""
    try:
        # Initialize result listener
        listener = ResultListener(
            project_id=project_id,
            subscription_name=subscription_name,
            timeout=timeout,
            verbose=verbose
        )
        
        for result in listener.listen():
            progress_queue.put(("result", result))
            
    except Exception as e:
        progress_queue.put(("error", f"Listening thread error: {str(e)}"))

@app.command()
def process(
    files: List[str] = typer.Argument(..., help="File paths or glob patterns to process"),
    prompt: str = typer.Option(..., "--prompt", "-p", help="Prompt to use for processing"),
    project_id: str = typer.Option(..., "--project-id", help="GCP project ID"),
    bucket_name: str = typer.Option(..., "--bucket", help="GCS bucket name"),
    topic_name: str = typer.Option(..., "--topic", help="Pub/Sub topic name"),
    subscription_name: str = typer.Option(..., "--subscription", help="Pub/Sub subscription name"),
    timeout: int = typer.Option(300, "--timeout", "-t", help="Timeout in seconds for processing each file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Dispatch files to GCP Pub/Sub and listen for results."""
    try:
        # Expand glob patterns and validate files
        expanded_files = []
        for pattern in files:
            expanded_files.extend(glob.glob(pattern))
        
        if not expanded_files:
            console.print("[red]Error: No valid files found[/red]")
            raise typer.Exit(1)
        
        valid_files = validate_file_paths(expanded_files)
        if not valid_files:
            console.print("[red]Error: No valid files to process[/red]")
            raise typer.Exit(1)
        
        # Create a queue for thread communication
        progress_queue = Queue()
        
        # Start dispatch thread
        dispatch_thread = threading.Thread(
            target=dispatch_job_thread,
            args=(valid_files, prompt, project_id, bucket_name, topic_name, progress_queue)
        )
        dispatch_thread.start()
        
        # Start listening thread
        listen_thread = threading.Thread(
            target=listen_thread,
            args=(project_id, subscription_name, timeout, verbose, progress_queue)
        )
        listen_thread.start()
        
        # Track progress
        files_dispatched = 0
        results_received = 0
        total_files = len(valid_files)
        
        with Progress() as progress:
            dispatch_task = progress.add_task("[cyan]Dispatching jobs...", total=total_files)
            result_task = progress.add_task("[cyan]Waiting for results...", total=total_files)
            
            while True:
                try:
                    # Get updates from the queue
                    update_type, data = progress_queue.get(timeout=1)
                    
                    if update_type == "dispatched":
                        files_dispatched += 1
                        progress.update(dispatch_task, advance=1)
                        console.print(f"[green]Dispatched: {data}[/green]")
                        
                    elif update_type == "result":
                        results_received += 1
                        progress.update(result_task, advance=1)
                        console.print(f"[green]Received result: {data}[/green]")
                        
                    elif update_type == "error":
                        console.print(f"[red]{data}[/red]")
                        
                    elif update_type == "done":
                        if files_dispatched == total_files:
                            break
                            
                except Queue.Empty:
                    # Check if threads are still alive
                    if not dispatch_thread.is_alive() and not listen_thread.is_alive():
                        break
                    continue
        
        # Wait for threads to finish
        dispatch_thread.join()
        listen_thread.join()
        
        console.print(f"\n[green]Dispatched {files_dispatched} jobs and received {results_received} results[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 