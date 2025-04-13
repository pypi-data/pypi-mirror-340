"""Tests for utility functions in the Amplify Documentation MCP Server."""

from unirt.amplify_doc_mcp_server.util import (
    clean_search_results,
    extract_content_from_html,
    format_documentation_result,
    is_html_content,
)
from unittest.mock import MagicMock, patch


class TestIsHtmlContent:
    """Tests for is_html_content function."""

    def test_html_tag_in_content(self):
        """Test detection of HTML content by HTML tag."""
        content = '<html><body>Test content</body></html>'
        assert is_html_content(content, '') is True

    def test_html_content_type(self):
        """Test detection of HTML content by content type."""
        content = 'Some content'
        assert is_html_content(content, 'text/html; charset=utf-8') is True

    def test_empty_content_type(self):
        """Test detection with empty content type."""
        content = 'Some content without HTML tags'
        assert is_html_content(content, '') is True

    def test_non_html_content(self):
        """Test detection of non-HTML content."""
        content = 'Plain text content'
        assert is_html_content(content, 'text/plain') is False


class TestFormatDocumentationResult:
    """Tests for format_documentation_result function."""

    def test_normal_content(self):
        """Test formatting normal content."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'Test content'
        result = format_documentation_result(url, content, 0, 100)
        assert result == f'Amplify Documentation from {url}:\n\n{content}'

    def test_start_index_beyond_content(self):
        """Test when start_index is beyond content length."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'Test content'
        result = format_documentation_result(url, content, 100, 100)
        assert '<e>No more content available.</e>' in result

    def test_empty_truncated_content(self):
        """Test when truncated content is empty."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'Test content'
        # This should result in empty truncated content
        result = format_documentation_result(url, content, 12, 100)
        assert '<e>No more content available.</e>' in result

    def test_truncated_content_with_more_available(self):
        """Test when content is truncated with more available."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'A' * 200  # 200 characters
        max_length = 100
        result = format_documentation_result(url, content, 0, max_length)
        assert 'A' * 100 in result
        assert 'start_index=100' in result
        assert 'Content truncated' in result

    def test_truncated_content_exact_fit(self):
        """Test when content fits exactly in max_length."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'A' * 100
        result = format_documentation_result(url, content, 0, 100)
        assert 'Content truncated' not in result

    def test_content_shorter_than_max_length(self):
        """Test when content is shorter than max_length."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'A' * 50  # 50 characters
        max_length = 100
        result = format_documentation_result(url, content, 0, max_length)
        assert 'A' * 50 in result
        assert 'Content truncated' not in result

    def test_partial_content_with_remaining(self):
        """Test when reading partial content with more remaining."""
        url = 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        content = 'A' * 200  # 200 characters
        start_index = 50
        max_length = 100
        result = format_documentation_result(url, content, start_index, max_length)
        assert 'A' * 100 in result
        assert 'start_index=150' in result
        assert 'Content truncated' in result


class TestExtractContentFromHTML:
    """Tests for extract_content_from_html function."""

    def test_extract_content_from_html(self):
        """Test extracting content from HTML."""
        html = '<html><body><main><h1>Test</h1><p>This is a test.</p></main></body></html>'
        with patch('bs4.BeautifulSoup') as mock_bs:
            mock_soup = MagicMock()
            mock_bs.return_value = mock_soup
            mock_main = MagicMock()
            mock_soup.select_one.return_value = mock_main

            with patch('markdownify.markdownify') as mock_markdownify:
                mock_markdownify.return_value = '# Test\n\nThis is a test.'
                result = extract_content_from_html(html)
                assert result == '# Test\n\nThis is a test.'
                mock_bs.assert_called_once()
                mock_markdownify.assert_called_once()

    def test_extract_content_from_html_no_content(self):
        """Test extracting content from HTML with no content."""
        html = '<html><body></body></html>'
        with patch('bs4.BeautifulSoup') as mock_bs:
            mock_soup = MagicMock()
            mock_bs.return_value = mock_soup
            mock_soup.select_one.return_value = None
            mock_soup.body = None

            with patch('markdownify.markdownify') as mock_markdownify:
                mock_markdownify.return_value = ''
                result = extract_content_from_html(html)
                assert '<e>' in result
                mock_bs.assert_called_once()

    def test_extract_content_from_html_exception(self):
        """Test extracting content from HTML with exception."""
        html = '<html><body><h1>Test</h1><p>This is a test.</p></body></html>'
        with patch('bs4.BeautifulSoup') as mock_bs:
            mock_bs.side_effect = Exception('Test exception')
            result = extract_content_from_html(html)
            assert '<e>Error converting HTML to Markdown' in result
            mock_bs.assert_called_once()


class TestCleanSearchResults:
    """Tests for clean_search_results function."""

    def test_clean_search_results_empty(self):
        """Test cleaning empty search results."""
        search_response = {'results': [{'hits': []}]}
        result = clean_search_results(search_response)
        assert result == []

    def test_clean_search_results_with_data(self):
        """Test cleaning search results with data."""
        # Create a mock search response
        search_response = {
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

        with patch('bs4.BeautifulSoup') as mock_bs:
            mock_soup = MagicMock()
            mock_bs.return_value = mock_soup
            mock_soup.get_text.return_value = 'Set up Amplify Auth'
            mock_highlight = MagicMock()
            mock_highlight.get_text.return_value = 'Auth'
            mock_soup.find_all.return_value = [mock_highlight]

            result = clean_search_results(search_response)

            assert len(result) == 1
            assert (
                result[0]['url']
                == 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
            )
            assert result[0]['title'] == 'Set up Amplify Auth'
            assert result[0]['platform'] == 'react'
            assert 'Auth' in result[0]['highlighted_terms']

    def test_clean_search_results_platform_extraction(self):
        """Test platform extraction from URL."""
        search_response = {
            'results': [
                {
                    'hits': [
                        {
                            'url': 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/',
                            'hierarchy': {'lvl0': 'Title', 'lvl1': 'Subtitle'},
                        },
                        {
                            'url': 'https://docs.amplify.aws/flutter/build-a-backend/auth/set-up-auth/',
                            'hierarchy': {'lvl0': 'Title', 'lvl1': 'Subtitle'},
                        },
                        {
                            'url': 'https://docs.amplify.aws/swift/build-a-backend/auth/set-up-auth/',
                            'hierarchy': {'lvl0': 'Title', 'lvl1': 'Subtitle'},
                        },
                    ]
                }
            ]
        }

        result = clean_search_results(search_response)

        assert len(result) == 3
        assert result[0]['platform'] == 'react'
        assert result[1]['platform'] == 'flutter'
        assert result[2]['platform'] == 'swift'
