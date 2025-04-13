"""Tests for utility functions using test resources."""

import json
import os
from unirt.amplify_doc_mcp_server.util import (
    clean_search_results,
    extract_content_from_html,
)


class TestCleanSearchResultsWithResources:
    """Tests for clean_search_results function using test resources."""

    def test_clean_search_results_with_sample_data(self):
        """Test cleaning search results with sample data."""
        # Load sample search response
        sample_file = os.path.join(
            os.path.dirname(__file__), 'resources', 'sample_search_response.json'
        )
        with open(sample_file, 'r') as f:
            sample_response = json.load(f)

        # Clean the results
        results = clean_search_results(sample_response)

        # Check that we got results
        assert len(results) > 0

        # Check that the first result has the expected structure
        first_result = results[0]
        assert first_result['url'].startswith('https://docs.amplify.aws/')
        assert 'title' in first_result
        assert 'platform' in first_result
        assert first_result['platform'] == 'react'

        # Check that highlighted terms are extracted
        assert 'highlighted_terms' in first_result
        assert len(first_result['highlighted_terms']) > 0


class TestExtractContentFromHtmlWithResources:
    """Tests for extract_content_from_html function using test resources."""

    def test_extract_content_from_sample_html(self):
        """Test extracting content from sample HTML."""
        # Load sample HTML
        sample_file = os.path.join(
            os.path.dirname(__file__), 'resources', 'sample_html_content.html'
        )
        with open(sample_file, 'r') as f:
            sample_html = f.read()

        # Extract content
        content = extract_content_from_html(sample_html)

        # Check that we got content
        assert len(content) > 0
        assert '# Set up Amplify Auth' in content

        # Check that the content contains markdown elements
        assert '#' in content  # Headers
        assert '```' in content  # Code blocks

        # Check that navigation and footer are not included
        assert 'Home' not in content
        assert 'Documentation' not in content
