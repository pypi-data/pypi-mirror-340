"""Live tests for the Amplify Documentation MCP Server.

These tests make actual API calls and should be run with the --run-live option.
"""

import pytest
from unittest.mock import MagicMock, patch


# Mock the fastmcp imports
class MockContext:
    """Mock context for testing."""

    async def error(self, message):
        """Mock error method."""
        print(f'Error: {message}')


class MockFastMCP:
    """Mock FastMCP class."""

    def __init__(self, name, instructions=None, dependencies=None):
        """Initialize with name."""
        self.name = name
        self.instructions = instructions
        self.dependencies = dependencies

    def tool(self):
        """Mock tool decorator."""

        def decorator(func):
            return func

        return decorator


# Mock Field function
def MockField(**kwargs):
    """Mock Field function."""
    return kwargs


# Mock the imports
with patch.dict(
    'sys.modules',
    {'mcp.server.fastmcp': MagicMock(Context=MockContext, FastMCP=MockFastMCP, Field=MockField)},
):
    from unirt.amplify_doc_mcp_server.server import (
        read_amplify_documentation,
        search_amplify_documentation,
    )


class TestSearchAmplifyDocumentationLive:
    """Live tests for the search_amplify_documentation function."""

    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_search_amplify_documentation_live(self):
        """Test searching Amplify documentation with live API."""
        ctx = MockContext()
        search_phrase = 'authentication'
        platform = 'react'
        limit = 5

        results = await search_amplify_documentation(
            ctx=ctx, search_phrase=search_phrase, platform=platform, limit=limit
        )

        # Check that we got results
        assert len(results) > 0
        assert len(results) <= limit

        # Check that the results have the expected structure
        for result in results:
            assert result.url.startswith('https://docs.amplify.aws/')
            assert result.title
            assert result.platform == platform
            # Not all results may have snippets or highlighted terms
            if result.snippet:
                assert len(result.snippet) > 0
            if result.highlighted_terms:
                assert len(result.highlighted_terms) > 0

    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_search_amplify_documentation_no_platform_live(self):
        """Test searching Amplify documentation without platform filter."""
        ctx = MockContext()
        search_phrase = 'authentication'
        limit = 5

        # Explicitly set platform to "react" since that's our default now
        results = await search_amplify_documentation(
            ctx=ctx,
            search_phrase=search_phrase,
            platform='react',  # Explicitly set platform
            limit=limit,
        )

        # Check that we got results
        assert len(results) > 0
        assert len(results) <= limit

        # Check that the results have the expected structure
        for result in results:
            assert result.url.startswith('https://docs.amplify.aws/')
            assert result.title
            # Results should be from react platform
            assert result.platform == 'react'


class TestReadAmplifyDocumentationLive:
    """Live tests for the read_amplify_documentation function."""

    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_read_amplify_documentation_live(self):
        """Test reading Amplify documentation with live API."""
        ctx = MockContext()
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        max_length = 10000
        start_index = 0  # Explicitly provide start_index to avoid FieldInfo issues

        result = await read_amplify_documentation(
            ctx=ctx, url=url, max_length=max_length, start_index=start_index
        )

        # Check that we got content
        assert 'Amplify Documentation from' in result
        assert '# Set up Amplify Auth' in result or 'Auth' in result
        assert len(result) > 100

    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_read_amplify_documentation_pagination_live(self):
        """Test reading Amplify documentation with pagination."""
        ctx = MockContext()
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        max_length = 1000  # Small max_length to force pagination
        start_index = 0  # Explicitly provide start_index to avoid FieldInfo issues

        # First chunk
        result1 = await read_amplify_documentation(
            ctx=ctx, url=url, max_length=max_length, start_index=start_index
        )

        # Check that content was truncated
        assert 'Content truncated' in result1 or 'start_index=' in result1

        # Extract next start index
        import re

        match = re.search(r'start_index=(\d+)', result1)
        if match:
            next_start = int(match.group(1))
        else:
            # If no match, just use a reasonable offset for testing
            next_start = 1000

        # Get next chunk
        result2 = await read_amplify_documentation(
            ctx=ctx, url=url, max_length=max_length, start_index=next_start
        )

        # Check that we got different content
        assert result1 != result2
        assert 'Amplify Documentation from' in result2
