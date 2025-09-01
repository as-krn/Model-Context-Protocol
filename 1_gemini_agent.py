from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown

client = genai.Client()

chat = client.chats.create(
    model="gemini-2.5-flash",
)

user_prompt = """What are the latest 3 papers from arXiv based on the topic MCP?
Please provide the title, authors, publication date, and a link to the PDF."""
response = chat.send_message(user_prompt)
# Use Rich to render Markdown for better terminal display
console = Console()
md = Markdown(response.text)
console.print(md)