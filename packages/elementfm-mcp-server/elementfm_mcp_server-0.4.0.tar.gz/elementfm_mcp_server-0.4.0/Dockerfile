FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Install dependencies
COPY pyproject.toml .
COPY README.md .
COPY elementfm_mcp_server ./elementfm_mcp_server

RUN uv pip install --system .

# Set default environment variable
ENV FRONTEND_ROOT_URL=https://app.element.fm

# Expose port
EXPOSE 8000

# Run MCP server
CMD ["python", "elementfm_mcp_server/server.py", "sse"]
