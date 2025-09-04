import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from google import genai

app = FastAPI()

# CORS ayarları (frontend ile backend konuşabilsin diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # geliştirirken her yerden izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP & Gemini
transport = StreamableHttpTransport("http://localhost:1923")
mcp_client = Client(transport)
gemini_client = genai.Client()
chat = None

class UserMessage(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    """Uygulama açılırken Gemini agent oluştur."""
    global chat
    async with mcp_client:
        system_instruction = (
            "You are an assistant with access to MCP tools. Use them to answer user queries. "
            "The tools: " + str(await mcp_client.list_tools())
        )
        chat = gemini_client.aio.chats.create(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],
                system_instruction=system_instruction,
            ),
        )

@app.post("/chat")
async def chat_with_agent(msg: UserMessage):
    """Frontend'ten gelen mesajı al, Gemini + MCP ile yanıtla."""
    response = await chat.send_message(msg.text)
    return {"response": response.text}
