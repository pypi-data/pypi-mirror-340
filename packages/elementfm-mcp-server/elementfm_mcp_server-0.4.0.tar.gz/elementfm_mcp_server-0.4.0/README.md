# ELEMENT.FM MCP Server

This is the MCP server implementation for the [ELEMENT.FM](https://element.fm) API.

## Configuration

Before using the server, you need to set up your API key as an environment variable:

```bash
export API_KEY=your_api_key_here
```

You can also optionally configure the frontend URL if you are self hosting (defaults to https://app.element.fm):

```bash
export FRONTEND_ROOT_URL=https://your-custom-url.com
```

## Python Usage

Pre-built script is [published to pypi](https://pypi.org/project/elementfm-mcp-server/)

```bash
uvx elementfm_mcp_server  # For standard I/O mode
# or
uvx elementfm_mcp_server sse   # For Server-Sent Events mode port 8000
```

## Docker Usage

To build the server with docker you can do

```
make
```

Or you can use the pre-build contaner image

```
docker run --rm -d -e API_KEY=api_key -p 8000:8000 registry.gitlab.com/elementfm/mcp:latest
```

Example Cursor mcp.json:

```
{
  "mcpServers": {
    "elementfm": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## Features

The MCP server provides the following functionality:

- Workspace management (create, list, get)
- Show management (create, list, get, update)
- Episode management (create, list, get, update, publish)
- AI features (transcription, chapter generation, show notes generation)
- Workspace invitations
- Workspace search

## Development

To set up the development environment:

```
devbox shell
```

## License

GPLv3