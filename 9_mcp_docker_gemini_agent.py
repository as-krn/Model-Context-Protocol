from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from google import genai
import asyncio

# Connect to the MCP server running in Docker on localhost:1923
# For HTTP transport, we need to create a StreamableHttpTransport
transport = StreamableHttpTransport("http://localhost:1923")
mcp_client = Client(transport)
gemini_client = genai.Client()

async def create_gemini_agent():
    """  
    Creates and returns a Gemini chat agent with access to MCP tools.

    Returns:
        chat (genai.aio.chats.Chat): The Gemini chat object configured with MCP tools.
    """  
    async with mcp_client:
        # Save the existing prompts as samples
        system_instruction = (
            "You are an assistant with access to MCP tools. Use them to answer user queries. "
            "The tools: " + str(await mcp_client.list_tools())
        )

        chat = gemini_client.aio.chats.create(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],
                system_instruction=system_instruction
            ),
        )
        return chat

async def main():
    """
    Main function to interact with the Gemini agent in a loop.
    """
    chat = await create_gemini_agent()
    print("Gemini agent is ready. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        response = await chat.send_message(user_input)
        print("Gemini: " + response.text)


if __name__ == "__main__":
    asyncio.run(main())

    sample_prompts = [
        "list the available tools in the mcp server you can access",
        "prepare a report based on 3 latest papers published at arXiv website about the RAG and MCP security risks. Provide the detailed citations and URLs."
    ]