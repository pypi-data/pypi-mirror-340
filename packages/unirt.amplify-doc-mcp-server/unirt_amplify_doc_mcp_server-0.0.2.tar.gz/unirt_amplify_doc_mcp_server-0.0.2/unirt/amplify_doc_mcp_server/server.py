"""Amplify Gen 2 Documentation MCP Server implementation."""

import argparse
import httpx
import json
import os
import sys
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from pydantic import AnyUrl, Field
from typing import List, Optional, Union
from unirt.amplify_doc_mcp_server.models import AmplifyDocSearchResult
from unirt.amplify_doc_mcp_server.util import (
    clean_search_results,
    extract_content_from_html,
    format_documentation_result,
    is_html_content,
)


# Set up logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 ModelContextProtocol/1.0 (Amplify Documentation Server)'

# Initialize FastMCP
mcp = FastMCP(
    'unirt.amplify-doc-mcp-server',
    instructions="""
    # AWS Amplify Gen 2 Documentation MCP Server

    This server provides tools to access AWS Amplify Gen 2 documentation and search for content.

    ## Best Practices

    - For long documentation pages, make multiple calls to `read_amplify_documentation` with different `start_index` values for pagination
    - When searching, use specific technical terms rather than general phrases
    - Filter by platform (react, vue, swift, android, flutter) to get platform-specific documentation
    - Always cite the documentation URL when providing information to users

    ## Tool Selection Guide

    - Use `search_amplify_documentation` when: You need to find documentation about a specific Amplify feature
    - Use `read_amplify_documentation` when: You have a specific documentation URL and need its content
    """,
    dependencies=[
        'pydantic',
        'httpx',
        'beautifulsoup4',
        'markdownify',
        'loguru',
    ],
)


@mcp.tool()
async def search_amplify_documentation(
    ctx: Context,
    search_phrase: str = Field(description='Search phrase to use'),
    platform: Optional[str] = Field(
        default='react',
        description='Filter by platform (e.g., "react", "vue", "swift", "android", "flutter"). Defaults to "react".',
    ),
    limit: int = Field(
        default=10,
        description='Maximum number of results to return',
    ),
) -> List[AmplifyDocSearchResult]:
    """Search AWS Amplify Gen 2 documentation using the official search API.

    ## Usage

    This tool searches across all AWS Amplify Gen 2 documentation for pages matching your search phrase.
    Use it to find relevant documentation when you don't have a specific URL.

    ## Search Tips

    - Use specific technical terms rather than general phrases
    - Include feature names to narrow results (e.g., "authentication react" instead of just "authentication")
    - Filter by platform to get platform-specific documentation
    - Use quotes for exact phrase matching

    ## Platform Options

    - react: React/JavaScript implementation
    - vue: Vue.js implementation
    - swift: iOS Swift implementation
    - android: Android implementation
    - flutter: Flutter implementation

    ## Result Interpretation

    Each result includes:
    - url: The documentation page URL
    - title: The page title
    - subtitle: The page subtitle or section
    - platform: The platform (react, vue, etc.)
    - snippet: A brief excerpt or summary
    - highlighted_terms: Terms that matched the search query

    Args:
        ctx: MCP context for logging and error handling
        search_phrase: Search phrase to use
        platform: Filter by platform
        limit: Maximum number of results to return

    Returns:
        List of search results with URLs, titles, and context snippets
    """
    logger.debug(f'Searching Amplify documentation for: {search_phrase}')

    # Validate parameters
    # Check if limit is a FieldInfo object (happens in tests with mocked imports)
    if hasattr(limit, 'default'):
        limit = limit.default

    if limit <= 0:
        error_msg = f'limit must be positive, got {limit}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return []

    if limit > 50:
        logger.warning('limit exceeds maximum of 50, capping to 50')
        limit = 50

    # Algolia API information
    app_id = 'WUUEEESZ67'
    api_key = '096fb25a5abb771ed2ac4391e80673c4'
    index_name = 'amplify'

    # Build facet filters
    facet_filters = ['gen:gen2']
    if platform:
        facet_filters.append(f'platform:{platform}')

    # Build request payload
    payload = {
        'requests': [
            {
                'indexName': index_name,
                'query': search_phrase,
                'params': (
                    'attributesToRetrieve=['
                    '"hierarchy.lvl0",'
                    '"hierarchy.lvl1",'
                    '"hierarchy.lvl2",'
                    '"hierarchy.lvl3",'
                    '"hierarchy.lvl4",'
                    '"hierarchy.lvl5",'
                    '"hierarchy.lvl6",'
                    '"content",'
                    '"type",'
                    '"url"]'
                    '&attributesToSnippet=['
                    '"hierarchy.lvl1:10",'
                    '"hierarchy.lvl2:10",'
                    '"hierarchy.lvl3:10",'
                    '"hierarchy.lvl4:10",'
                    '"hierarchy.lvl5:10",'
                    '"hierarchy.lvl6:10",'
                    '"content:10"]'
                    '&snippetEllipsisText=…'
                    '&highlightPreTag=<mark>'
                    '&highlightPostTag=</mark>'
                    f'&hitsPerPage={limit}'
                    '&clickAnalytics=false'
                    f'&facetFilters={json.dumps(facet_filters)}'
                ),
            }
        ]
    }

    # Make request to Algolia API
    url = f'https://{app_id}-dsn.algolia.net/1/indexes/*/queries'
    headers = {
        'X-Algolia-API-Key': api_key,
        'X-Algolia-Application-Id': app_id,
        'Content-Type': 'application/json',
        'User-Agent': DEFAULT_USER_AGENT,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            search_response = response.json()

            # Clean and format search results
            cleaned_results = clean_search_results(search_response)

            # Convert to AmplifyDocSearchResult objects
            results = [AmplifyDocSearchResult(**result) for result in cleaned_results]

            logger.debug(f'Found {len(results)} results for "{search_phrase}"')
            return results

    except httpx.HTTPError as e:
        error_msg = f'Error searching Amplify documentation: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return []
    except Exception as e:
        error_msg = f'Unexpected error searching Amplify documentation: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return []


@mcp.tool()
async def read_amplify_documentation(
    ctx: Context,
    url: Union[AnyUrl, str] = Field(
        description='URL of the AWS Amplify documentation page to read'
    ),
    max_length: int = Field(
        default=10000,
        description='Maximum number of characters to return.',
    ),
    start_index: int = Field(
        default=0,
        description='Starting character index for pagination.',
    ),
) -> str:
    """Fetch and convert an AWS Amplify documentation page to markdown format.

    ## Usage

    This tool retrieves the content of an AWS Amplify documentation page and converts it to markdown format.
    For long documents, you can make multiple calls with different start_index values to retrieve
    the entire content in chunks.

    ## URL Requirements

    - Must be from the docs.amplify.aws domain

    ## Example URLs

    - https://docs.amplify.aws/react/build-a-backend/auth/
    - https://docs.amplify.aws/flutter/start/getting-started/

    ## Output Format

    The output is formatted as markdown text with:
    - Preserved headings and structure
    - Code blocks for examples
    - Lists and tables converted to markdown format

    ## Handling Long Documents

    If the response indicates the document was truncated, you have several options:

    1. **Continue Reading**: Make another call with start_index set to the end of the previous response
    2. **Stop Early**: For very long documents, if you've already found the specific information needed, you can stop reading

    Args:
        ctx: MCP context for logging and error handling
        url: URL of the AWS Amplify documentation page to read
        max_length: Maximum number of characters to return
        start_index: Starting character index for pagination

    Returns:
        Markdown content of the AWS Amplify documentation
    """
    url_str = str(url)
    logger.debug(f'Fetching documentation from {url_str}')

    # Validate URL
    if not url_str.startswith('https://docs.amplify.aws/'):
        error_msg = f'Invalid URL: {url_str}. URL must be from the docs.amplify.aws domain'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return f'<e>{error_msg}</e>'

    # Validate parameters
    if max_length <= 0:
        error_msg = f'max_length must be positive, got {max_length}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return f'<e>{error_msg}</e>'

    # Check if start_index is a FieldInfo object (happens in live tests with mocked imports)
    if hasattr(start_index, 'default'):
        start_index = start_index.default

    if start_index < 0:
        error_msg = f'start_index must be non-negative, got {start_index}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return f'<e>{error_msg}</e>'

    # Fetch the documentation page
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url_str,
                follow_redirects=True,
                headers={'User-Agent': DEFAULT_USER_AGENT},
                timeout=30.0,
            )
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')
            page_raw = response.text

            # Check if content is HTML
            if not is_html_content(page_raw, content_type):
                error_msg = f'Content at {url_str} is not HTML.'
                logger.error(error_msg)
                await ctx.error(error_msg)
                return f'<e>{error_msg}</e>'

            # Extract content from HTML
            markdown_content = extract_content_from_html(page_raw)

            # Format the result with pagination information
            result = format_documentation_result(
                url_str, markdown_content, start_index, max_length
            )

            # Log if content was truncated
            if len(markdown_content) > start_index + max_length:
                logger.debug(
                    f'Content truncated at {start_index + max_length} of {len(markdown_content)} characters'
                )

            return result

    except httpx.HTTPError as e:
        error_msg = f'Error fetching Amplify documentation: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return f'<e>{error_msg}</e>'
    except Exception as e:
        error_msg = f'Error processing Amplify documentation: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        return f'<e>{error_msg}</e>'


def main():
    """Run the MCP server with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='Model Context Protocol (MCP) server for AWS Amplify Gen 2 Documentation'
    )
    parser.add_argument('--sse', action='store_true', help='Use SSE transport')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')

    args = parser.parse_args()

    # Log startup information
    logger.info('Starting AWS Amplify Gen 2 MCP Server')

    # Run server with appropriate transport
    if args.sse:
        logger.info(f'Using SSE transport on port {args.port}')
        mcp.settings.port = args.port
        mcp.run(transport='sse')
    else:
        logger.info('Using standard stdio transport')
        mcp.run()


if __name__ == '__main__':
    main()
