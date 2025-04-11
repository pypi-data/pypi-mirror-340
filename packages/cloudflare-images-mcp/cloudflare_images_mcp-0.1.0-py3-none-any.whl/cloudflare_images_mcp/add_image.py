import json
import os
from typing import Annotated
from urllib.parse import urlparse

import httpx
from mcp import ErrorData, McpError
from mcp.server.fastmcp import Context
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, TextContent
from pydantic import Field


async def add_image_to_cloudflare_images(
    image_source: Annotated[str, Field(description="The source of the image to upload. Can be a URL or a local file path.")],
    ctx: Context,
    metadata: Annotated[dict[str, str] | None, Field(description="The metadata to add to the image.")] = None,
) -> TextContent:
    """
    Adds an image to Cloudflare Images from a URL or a local file path.

    Usage:
       add_image_to_cloudflare_images("https://example.com/image.png") # URL
       add_image_to_cloudflare_images("/path/to/local/image.jpeg") # Local file path
       add_image_to_cloudflare_images("https://example.com/image.png", metadata={"key": "value"}) # URL with metadata
    """

    api_url = f"https://api.cloudflare.com/client/v4/accounts/{ctx.request_context.lifespan_context.account_id}/images/v1"

    parsed_url = urlparse(image_source)
    is_url = all([parsed_url.scheme, parsed_url.netloc])

    if is_url:
        # Prepare data for URL upload
        post_files = {"url": (None, image_source)}
    else:
        if not os.path.isfile(image_source):
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message=f"Local file not found: {image_source}",
                )
            )

        post_files = {"file": open(image_source, "rb")}

    async with httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {ctx.request_context.lifespan_context.api_token}",
        }
    ) as client:
        try:
            # Make the request with either data (for URL) or files (for local file)
            response = await client.post(api_url, files=post_files)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            result_data = response.json()
            return TextContent(type="text", text=json.dumps(result_data["result"], indent=2))
        except httpx.HTTPStatusError as e:
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message=f"Cloudflare API indicated failure for {image_source}: {e.response.text}",
                )
            ) from e
        except Exception as e:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Error adding image to Cloudflare Images: {e}",
                )
            ) from e
