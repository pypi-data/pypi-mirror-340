import argparse
import logging
import os
from contextlib import asynccontextmanager
from importlib.metadata import version

from mcp.server.fastmcp import FastMCP

from cloudflare_images_mcp.add_image import add_image_to_cloudflare_images
from cloudflare_images_mcp.context import AppContext

logger = logging.getLogger(__name__)


def main():
    """MCP Cloudflare Images: Add images to Cloudflare Images."""
    parser = argparse.ArgumentParser(description="MCP Cloudflare Images: Add images to Cloudflare Images.")
    parser.add_argument("--version", action="version", version=version("cloudflare-images-mcp"))
    parser.add_argument("--account-id", type=str, help="The account ID to use for the Cloudflare API.")
    parser.add_argument("--api-token", type=str, help="The API token to use for the Cloudflare API.")
    args = parser.parse_args()

    account_id = args.account_id or os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = args.api_token or os.environ.get("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        raise ValueError(
            "Cloudflare account ID and API token must be provided either as arguments "
            "(--account-id and --api-token) or as environment variables "
            "(CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN)."
        )

    @asynccontextmanager
    async def lifespan(self):
        yield AppContext(account_id=account_id, api_token=api_token)

    server = FastMCP("cloudflare-images-mcp", lifespan=lifespan)
    server.add_tool(add_image_to_cloudflare_images)

    server.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    main()
