import asyncio
from fastmcp import Client

client = Client("4_mcp_server.py")

# Example of calling a tool defined in the server
# fetch_arxiv_papers(topic: str, number_of_papers: int = 3)
# get_arxiv_abstract(arxiv_id: str)

async def call_tool_fetch(topic: str, number_of_papers: int):
    async with client:
        result = await client.call_tool("fetch_arxiv_papers",
            {"topic": topic,
             "number_of_papers": number_of_papers})
        
        print(result.structured_content)

asyncio.run(call_tool_fetch("MCP", 3))


#https://gofastmcp.com/clients/resources
#https://gofastmcp.com/servers/resources