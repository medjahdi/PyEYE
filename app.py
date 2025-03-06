import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.style import Style

# Initialize Rich console
console = Console()

def fetch_url(url):
    """Fetch URL content with error handling and content type check"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if any(x in content_type for x in ['text', 'javascript', 'css']):
                return response.text
            console.print(f"[yellow]Skipping non-text content at {url}[/yellow]")
            return None
        console.print(f"[red]Failed to fetch {url}: Status code {response.status_code}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error fetching {url}: {str(e)}[/red]")
        return None

def extract_resource_urls(main_url, html):
    """Extract resource URLs from HTML content"""
    soup = BeautifulSoup(html, 'html.parser')
    tags = {'script': 'src', 'link': 'href', 'img': 'src'}
    resource_urls = set()

    for tag, attr in tags.items():
        for element in soup.find_all(tag, **{attr: True}):
            url = element.get(attr)
            absolute_url = urljoin(main_url, url)
            resource_urls.add(absolute_url)
    
    return resource_urls

def is_valid_path(path):
    """Validate path using criteria from original JavaScript code"""
    if not (path.startswith('/') or path.startswith('./') or path.startswith('../')):
        return False
    if ' ' in path:
        return False
    if re.search(r'[^\x20-\x7E]', path):
        return False
    if len(path) < 1 or len(path) >= 200:
        return False
    return True

def extract_paths(content):
    """Extract valid paths from text content using regex"""
    pattern = re.compile(r'''['"]((?:/|\.\./|\./)[^'"]*)['"]''')
    matches = pattern.findall(content)
    return [path for path in matches if is_valid_path(path)]

def main():
    parser = argparse.ArgumentParser(description='Extract endpoints from a website')
    parser.add_argument('url', help='Target website URL')
    parser.add_argument('-o', '--output', default='endpoints.txt',
                       help='Output file name (default: endpoints.txt)')
    args = parser.parse_args()

    main_url = args.url
    output_file = args.output

    # Display a fancy header with project name and copyright
    console.print(Panel.fit(
        Text("PyEYE - Python Endpoint Extractor\n", style="bold blue") +
        Text("Copyright © @medjahdi\n", style="bold yellow") +
        Text("For educational purposes only", style="bold green"),
        title="Welcome to PyEYE",
        border_style="bold magenta"
    ))
    console.print(f"[bold]Target URL:[/bold] [cyan]{main_url}[/cyan]")
    console.print(f"[bold]Output File:[/bold] [cyan]{output_file}[/cyan]")
    console.print()

    # Fetch main page
    with console.status("[bold green]Fetching main page...[/bold green]", spinner="dots"):
        main_html = fetch_url(main_url)
    if not main_html:
        console.print("[red]Failed to fetch main URL. Exiting...[/red]")
        return

    # Extract resource URLs
    with console.status("[bold green]Extracting resource URLs...[/bold green]", spinner="dots"):
        resource_urls = extract_resource_urls(main_url, main_html)
    console.print(f"[green]Found {len(resource_urls)} resource URLs to process[/green]")

    # Collect all paths
    all_paths = set()
    
    # Process main page content
    with console.status("[bold green]Processing main page content...[/bold green]", spinner="dots"):
        main_paths = extract_paths(main_html)
        all_paths.update(main_paths)
    console.print(f"[green]Found {len(main_paths)} paths in main HTML[/green]")

    # Process each resource URL
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing resource URLs...", total=len(resource_urls))
        for url in resource_urls:
            progress.update(task, advance=1, description=f"[cyan]Processing: {url}[/cyan]")
            content = fetch_url(url)
            if content:
                paths = extract_paths(content)
                all_paths.update(paths)
                progress.console.print(f"[yellow]Found {len(paths)} paths in {url}[/yellow]")

    # Save results
    sorted_paths = sorted(all_paths)
    with open(output_file, 'w') as f:
        f.write('\n'.join(sorted_paths))
    
    # Display results in a table
    table = Table(title="Extracted Endpoints", show_header=True, header_style="bold magenta")
    table.add_column("Endpoint", style="cyan")
    for path in sorted_paths:
        table.add_row(path)
    
    console.print()
    console.print(Panel.fit(table))
    console.print(f"[bold green]Saved {len(sorted_paths)} unique endpoints to {output_file}[/bold green]")

if __name__ == '__main__':
    main()