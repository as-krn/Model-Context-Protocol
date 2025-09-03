# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the MCP server script to the container
COPY 8_mcp_docker_server.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for reports
RUN mkdir -p /app/reports

# Expose the port the MCP server will run on
EXPOSE 1923

# Default command to run the MCP server
CMD ["python", "8_mcp_docker_server.py"]