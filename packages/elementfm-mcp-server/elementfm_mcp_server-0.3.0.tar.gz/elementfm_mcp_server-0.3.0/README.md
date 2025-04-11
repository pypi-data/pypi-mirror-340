# ELEMENT.FM MCP Server

This is the MCP server implementation for the ELEMENT.FM API.

## Configuration

Before using the server, you need to set up your API key as an environment variable:

```bash
export API_KEY=your_api_key_here
```

You can also optionally configure the frontend URL if you are self hosting (defaults to https://app.element.fm):

```bash
export FRONTEND_ROOT_URL=https://your-custom-url.com
```

## Usage

```bash
uvx elementfm_mcp_server  # For standard I/O mode
# or
uvx elementfm_mcp_server sse   # For Server-Sent Events mode port 8000
```

## Docker

To run the server with docker you can do

```
make
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
- Recipient management
- Workspace search

## Development

To set up the development environment:

```
devbox shell
```

## License

GPLv3