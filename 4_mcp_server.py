import os
import urllib.request
from fastmcp import FastMCP
import xml.etree.ElementTree as ET
import re

mcp = FastMCP("Arxiv Mcp Server")

@mcp.tool
def fetch_arxiv_papers(topic: str, number_of_papers: int = 3) -> list:
    """  
    Retrieves the latest papers from arXiv matching a given topic.

    This tool searches arXiv for papers based on the provided topic, fetches the most recent ones sorted by submission date in descending order, and returns a list of dictionaries containing details for each paper. Each dictionary includes the arXiv ID, title, authors, publication date, and

    Args:
        topic (str): The search topic or keyword (e.g., "mcp", "machine learning").
        number_of_papers (int, optional): The number of latest papers to retrieve. Defaults to 3.

    Returns:
        list: A list of dictionaries, each representing a paper with keys:
            - 'arxiv_id' (str): The arXiv identifier of the paper.
            - 'title' (str): The title of the paper.
            - 'authors' (list of str): List of author names.
            - 'published' (str): Publication date in ISO format.
            - 'pdf_link' (str): URL to the PDF of the paper.


    Example:
        fetch_arxiv_papers("quantum computing", 2)
        # Returns: [{'arxiv_id': '...', 'title': '...', 'authors': [...], 'published': '...', 'pdf_link': '...'}, ...]
    """

    search_query = f"all:({topic})"
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={number_of_papers}&sortBy=submittedDate&sortOrder=descending"
    print(f"******* FUNCTION CALLED: Fetching papers from arXiv with URL: {url} *******")
    with urllib.request.urlopen(url) as resp:
        raw = resp.read()

    root = ET.fromstring(raw)

    papers = []
    for entry in root.findall(".//{*}entry"):
        full_id = entry.findtext("{*}id")
        arxiv_id = full_id.split("/")[-1] if full_id else None
        title = entry.findtext("{*}title")
        published = entry.findtext("{*}published")
        authors = [a.findtext("{*}name") for a in entry.findall("{*}author")]
        pdf_link = next((l.get("href") for l in entry.findall("{*}link") if l.get("type") == "application/pdf"), None)
        
        papers.append({
            'arxiv_id': arxiv_id,
            'title': title,
            'authors': authors,
            'published': published,
            'pdf_link': pdf_link
        })

    return papers

@mcp.tool
def get_arxiv_abstract(arxiv_id: str) -> str | None:
    """
    Fetches and returns the abstract of a specific arXiv paper.

    This tool retrieves the abstract (summary) of an arXiv paper using its unique arXiv ID. It queries the arXiv API and extracts the summary text if available.

    Args:
        arxiv_id (str): The arXiv ID (e.g., "2301.12345"). Must be a valid arXiv identifier.

    Returns:
        str: The abstract text of the paper, or None if the paper is not found or an error occurs.

    Example:
        get_arxiv_abstract("2301.12345")
        # Returns: "This paper discusses..."
    """
    
    url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    print(f"******* FUNCTION CALLED: Fetching paper abstract from arXiv with URL: {url} *******")
    try:
        with urllib.request.urlopen(url) as resp:
            raw = resp.read()

        root = ET.fromstring(raw)
        entry = root.find(".//{*}entry")
        if entry is not None:
            return entry.findtext('{*}summary')
        else:
            return None
    except Exception as e:
        print(f"Error fetching abstract: {e}")
        return None

@mcp.tool    
def save_md_to_file(text: str, filename: str) -> None:
    """  
    Saves the given Markdown-formatted text to a .md file in the ./reports folder.

    This tool writes the provided text to a file with a .md extension in the ./reports directory.  
    The folder is created if it doesn't exist. The filename is automatically sanitized  
    to replace special characters (e.g., colons, slashes) with hyphens to ensure compatibility across systems.  
    Use a descriptive filename based on the content, such as the paper title, for easy identification.

    Args:
        text (str): The Markdown-formatted text to save.
        filename (str): The desired name of the file (e.g., "Model Context Protocols in Adaptive Transport").  
        Special characters will be replaced with hyphens, and '.md' will be appended if not present.

    Returns:
    None

    Example:
        papers = fetch_arxiv_papers("MCP", 3)
        abstracts = [get_arxiv_abstract(paper['arxiv_id']) for paper in papers]
        md_content = "# Latest MCP Papers\n\n"
        for i, paper in enumerate(papers):
            md_content += f"## {paper['title']}\nAuthors: {', '.join(paper['authors'])}\nPublished: {paper['published']}\n"
        save_md_to_file(md_content, "mcp_papers_summary.md")
    """
    print(f"******* FUNCTION CALLED: Saving Markdown to file: {filename} *******")

    # Create reports folder if it doesn't exist
    os.makedirs("./reports", exist_ok=True)

    # Sanitize filename to avoid issues with special characters
    filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
    if not filename.endswith('.md'):
        filename += '.md'

    # Set path to ./reports
    filepath = os.path.join('./reports', filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"File saved successfully: {filepath}")
    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    mcp.run()

# USE COMMANDS:
# "fastmcp run 4_mcp_server.py:mcp" or just "python 4_mcp_server.py"
# This command starts the MCP server defined in the file `4_mcp_server.py` with the instance `mcp`. 
# It allows the server to register its tools and make them accessible for external clients.

# "npx @modelcontextprotocol/inspector"
# This command connects to the MCP server and lists all available tools with their metadata.
# It allows interactive testing and debugging of the server's tools.