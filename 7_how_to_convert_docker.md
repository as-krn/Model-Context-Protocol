# How to Run MCP Server in Docker and Gemini Agent Locally

This document explains how to set up and run the MCP server in a Docker container, while running the Gemini agent locally on your host machine. This approach keeps the server containerized for portability, while allowing the agent to run natively for easier interaction.

## Architecture Overview

**This setup uses a hybrid architecture:**

1. **Docker Container**: Runs the MCP server (8.mcp_docker_server.py) with HTTP transport on port 1923  
2. **Local Host**: Runs the Gemini agent (6.mcp_gemini_agent.py) which connects to the Dockerized server  
3. **Volume Mount**: The "/reports" directory is shared between container and host for file persistence  

---

## Why Two Server Files?

- mcp_server.py: For development and testing locally with stdio transport (faster, simpler)  
- mcp_docker_server.py: For production Docker deployment with HTTP transport (network-accessible, containerized)  

This approach provides the best of both worlds: easy local development and robust containerized deployment.


# For Local Development:

# Test Locally with stdio transport
fastmcp run 4_mcp_server.py:mcp<br>
npx @modelcontextprotocol/inspector

# For Docker Deployment:

```bash
# Build and run Docker container with custom name
docker build -t arxiv-mcp-server .
docker run -d --name mcp-arxiv-server -p 1923:1923 -v ${PWD}/reports:/app/reports arxiv-mcp-server

# Test Docker container
npx @modelcontextprotocol/inspector --transport streamable-http --url http://localhost:1923

