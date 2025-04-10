# mcp-server-chatgpt-app

## Prerequisite

- [ChatGPT macOS app](https://openai.com/chatgpt/download/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Required Permissions

Before using the server, you need to grant the following permissions:

1. Open System Settings > Privacy & Security > Accessibility
2. Click the "+" button and add your mcp client (cursor, chatwise, etc.)
3. Make sure the checkbox next to your mcp client app is checked


## Usage

### cursor

update `.mcp.json` to add the following:

```
{
    "mcpServers": {
      "chatgpt": {
        "command": "uvx",
        "args": ["mcp-server-chatgpt-app"],
        "env": {},
        "disabled": false,
        "autoApprove": []
      }
    }
}
```

### chatwise

Go to Settings -> Tools -> Add and use the following config:

```
Type: stdio
ID: ChatGPT
Command: uvx mcp-server-chatgpt-app
```

## local development

```
uv --directory $HOME/Developer/mcp-server-chatgpt-app/src/mcp_server_chatgpt run server.py
```