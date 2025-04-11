# Cloudflare Images MCP 🛠️

## Simple MCP Tool to add images to Cloudflare Images

### Configuration

> **ℹ️ Note:** Instead of providing `--account-id` and `--api-token` as arguments, you can also use the environment variables `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` respectively.

```json
{
  "mcpServers": {
    "cloudflare-images-mcp": {
      "command": "uvx",
      "args": [
        "cloudflare-images-mcp",
        "--account-id",
        "your-account-id",
        "--api-token",
        "your-api-token"
      ]
    }
  }
}
```
