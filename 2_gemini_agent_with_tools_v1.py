import urllib.request
import xml.etree.ElementTree as ET
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
import os
import re

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
    

client = genai.Client()
config = types.GenerateContentConfig(
    tools=[fetch_arxiv_papers, get_arxiv_abstract]
)
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=config,
)
print("Gemini agent is ready.")
print("----------------------------------------------------------------------------------------")
user_prompt = """What are the latest 3 papers from arXiv based on the topic MCP?
Please provide the id, title, authors, publication date, and a link to the PDF."""
print("User prompt:", user_prompt)
response = chat.send_message(user_prompt)
# Use Rich to render Markdown for better terminal display
console = Console()
md = Markdown(response.text)
console.print(md)

print("----------------------------------------------------------------------------------------")
user_prompt = """Summarize the first paper's abstract."""
print("User prompt:", user_prompt)
response = chat.send_message(user_prompt)
# Use Rich to render Markdown for better terminal display
md = Markdown(response.text)
console.print(md)