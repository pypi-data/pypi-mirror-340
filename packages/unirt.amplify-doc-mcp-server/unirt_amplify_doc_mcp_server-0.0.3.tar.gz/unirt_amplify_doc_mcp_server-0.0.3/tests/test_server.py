"""Tests for the Amplify Documentation MCP Server."""

import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


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


# Set up the mocks
mock_fastmcp = MagicMock()
mock_fastmcp.Context = MockContext
mock_fastmcp.FastMCP = MockFastMCP
mock_fastmcp.Field = MockField

# Mock the imports
with patch.dict('sys.modules', {'mcp.server.fastmcp': mock_fastmcp, 'loguru': MagicMock()}):
    # Import the functions to test
    from unirt.amplify_doc_mcp_server.server import (
        read_amplify_documentation,
        search_amplify_documentation,
    )


class TestSearchAmplifyDocumentation:
    """Tests for the search_amplify_documentation function."""

    @pytest.mark.asyncio
    async def test_search_amplify_documentation(self):
        """Test searching Amplify documentation."""
        ctx = MockContext()
        search_phrase = 'auth'
        platform = 'react'
        limit = 5

        # Mock the response from Algolia API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {
                    'hits': [
                        {
                            'url': 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/#pageMain',
                            'hierarchy': {
                                'lvl0': 'Set up Amplify Auth - AWS Amplify Gen 2 Documentation',
                                'lvl1': 'Set up Amplify Auth',
                            },
                            '_snippetResult': {
                                'hierarchy': {
                                    'lvl1': {'value': 'Set up Amplify <mark>Auth</mark>'}
                                }
                            },
                        }
                    ]
                }
            ]
        }

        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with patch('unirt.amplify_doc_mcp_server.server.clean_search_results') as mock_clean:
                mock_clean.return_value = [
                    {
                        'url': 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/',
                        'title': 'Set up Amplify Auth',
                        'subtitle': None,
                        'platform': 'react',
                        'snippet': 'Set up Amplify Auth',
                        'highlighted_terms': ['Auth'],
                    }
                ]

                results = await search_amplify_documentation(
                    ctx=ctx, search_phrase=search_phrase, platform=platform, limit=limit
                )

                assert len(results) == 1
                assert (
                    results[0].url
                    == 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
                )
                assert results[0].title == 'Set up Amplify Auth'
                assert results[0].platform == 'react'
                assert 'Auth' in results[0].highlighted_terms

                # Verify the API call
                mock_post.assert_called_once()
                args, kwargs = mock_post.call_args
                assert kwargs['json']['requests'][0]['query'] == search_phrase
                assert 'facetFilters' in kwargs['json']['requests'][0]['params']
                assert f'platform:{platform}' in kwargs['json']['requests'][0]['params']

    @pytest.mark.asyncio
    async def test_search_amplify_documentation_error(self):
        """Test searching Amplify documentation with an error."""
        ctx = MockContext()
        search_phrase = 'auth'

        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.HTTPError('Connection error')

            results = await search_amplify_documentation(ctx=ctx, search_phrase=search_phrase)

            assert results == []
            mock_post.assert_called_once()


class TestReadAmplifyDocumentation:
    """Tests for the read_amplify_documentation function."""

    @pytest.mark.asyncio
    async def test_read_amplify_documentation(self):
        """Test reading Amplify documentation."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        ctx = MockContext()
        html_content = '<html><body><h1>Test</h1><p>This is a test.</p></body></html>'
        markdown_content = '# Test\n\nThis is a test.'
        formatted_result = f'Amplify Documentation from {url}:\n\n{markdown_content}'

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_content
        mock_response.headers = {'content-type': 'text/html'}

        # Patch the server module
        with (
            patch('unirt.amplify_doc_mcp_server.server.is_html_content', return_value=True),
            patch(
                'unirt.amplify_doc_mcp_server.server.extract_content_from_html',
                return_value=markdown_content,
            ),
            patch(
                'unirt.amplify_doc_mcp_server.server.format_documentation_result',
                return_value=formatted_result,
            ),
        ):
            # Patch the AsyncClient.get method
            with patch('httpx.AsyncClient.__aenter__', return_value=MagicMock()) as mock_client:
                mock_client.return_value.get = AsyncMock(return_value=mock_response)

                # Call the function
                result = await read_amplify_documentation(
                    ctx=ctx, url=url, max_length=10000, start_index=0
                )

                # Verify the result
                assert result == formatted_result

    @pytest.mark.asyncio
    async def test_read_amplify_documentation_invalid_url(self):
        """Test reading Amplify documentation with an invalid URL."""
        url = 'https://example.com/invalid'
        ctx = MockContext()

        result = await read_amplify_documentation(
            ctx=ctx, url=url, max_length=10000, start_index=0
        )

        assert '<e>Invalid URL' in result

    @pytest.mark.asyncio
    async def test_read_amplify_documentation_http_error(self):
        """Test reading Amplify documentation with an HTTP error."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        ctx = MockContext()

        with patch('httpx.AsyncClient.__aenter__') as mock_client:
            mock_client.return_value.get = AsyncMock(
                side_effect=httpx.HTTPError('Connection error')
            )

            result = await read_amplify_documentation(
                ctx=ctx, url=url, max_length=10000, start_index=0
            )

            assert '<e>Error fetching' in result
            assert 'Connection error' in result

    @pytest.mark.asyncio
    async def test_read_amplify_documentation_non_html(self):
        """Test reading Amplify documentation with non-HTML content."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        ctx = MockContext()

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'Plain text content'
        mock_response.headers = {'content-type': 'text/plain'}

        # Patch the server module
        with patch('unirt.amplify_doc_mcp_server.server.is_html_content', return_value=False):
            # Patch the AsyncClient.get method
            with patch('httpx.AsyncClient.__aenter__') as mock_client:
                mock_client.return_value.get = AsyncMock(return_value=mock_response)

                result = await read_amplify_documentation(
                    ctx=ctx, url=url, max_length=10000, start_index=0
                )

                assert '<e>Content at' in result
                assert 'is not HTML' in result
