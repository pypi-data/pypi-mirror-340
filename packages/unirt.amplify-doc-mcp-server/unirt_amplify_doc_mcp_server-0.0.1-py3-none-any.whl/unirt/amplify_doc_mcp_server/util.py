"""Utility functions for Amplify Documentation MCP Server."""

import markdownify
from typing import Any, Dict, List


def extract_content_from_html(html: str) -> str:
    """Extract and convert Amplify documentation HTML content to Markdown format.

    Args:
        html: Raw HTML content to process

    Returns:
        Simplified markdown version of the content
    """
    if not html:
        return '<e>Empty HTML content</e>'

    try:
        # First use BeautifulSoup to clean up the HTML
        from bs4 import BeautifulSoup

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Try to find the main content area - Amplify specific selectors
        main_content = None

        # Common content container selectors for Amplify documentation
        content_selectors = [
            'main',
            'article',
            '.main',
            '.main-content',
            '#main-content',
            '.amplify-flex.main',
            '.layout-main',
            '.page-content',
            '.docs-main-content',
            '#amplify-docs-content',
            '.amplify-content',
            '.docs-content',
            "div[role='main']",
        ]

        # Try to find the main content using common selectors
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                main_content = content
                break

        # If no main content found, use the body
        if not main_content:
            main_content = soup.body if soup.body else soup

        # Remove navigation elements that might be in the main content
        nav_selectors = [
            'noscript',
            '.prev-next',
            '.layout-sidebar',
            '.layout-header',
            '.breadcrumb__container',
            '.footer',
            '.navbar',
            '.toc',
            '.next-prev',
            '.page-last-updated',
            '.feedback',
            '.repo-actions',
            '.layout-sidebar-feedback',
            '.layout-sidebar-menu',
            '.amplify-message',
            '.amplify-breadcrumbs',
            '.amplify-togglebuttongroup',
            '.color-switcher',
            '.footer__links',
            '.footer__content',
            '.footer-wrapper',
        ]

        for selector in nav_selectors:
            for element in main_content.select(selector):
                element.decompose()

        # Define tags to strip - these are elements we don't want in the output
        tags_to_strip = [
            'script',
            'style',
            'noscript',
            'meta',
            'link',
            'footer',
            'nav',
            'aside',
            'header',
            # Amplify documentation specific elements
            'amplify-cookie-consent-container',
            'amplify-feedback-container',
            'amplify-page-header',
            'amplify-page-header-container',
            'amplify-filter-selector',
            'amplify-breadcrumb-container',
            'amplify-page-footer',
            'amplify-page-footer-container',
            'amplify-footer',
            'amplify-cookie-banner',
            # Common unnecessary elements
            'js-show-more-buttons',
            'js-show-more-text',
            'feedback-container',
            'feedback-section',
            'doc-feedback-container',
            'doc-feedback-section',
            'warning-container',
            'warning-section',
            'cookie-banner',
            'cookie-notice',
            'copyright-section',
            'legal-section',
            'terms-section',
        ]

        # Use markdownify on the cleaned HTML content
        content = markdownify.markdownify(
            str(main_content),
            heading_style=markdownify.ATX,
            autolinks=True,
            default_title=True,
            escape_asterisks=True,
            escape_underscores=True,
            newline_style='SPACES',
            strip=tags_to_strip,
        )

        if not content:
            return '<e>Page failed to be simplified from HTML</e>'

        return content
    except Exception as e:
        return f'<e>Error converting HTML to Markdown: {str(e)}</e>'


def is_html_content(page_raw: str, content_type: str) -> bool:
    """Determine if content is HTML.

    Args:
        page_raw: Raw page content
        content_type: Content-Type header

    Returns:
        True if content is HTML, False otherwise
    """
    return '<html' in page_raw[:100] or 'text/html' in content_type or not content_type


def format_documentation_result(url: str, content: str, start_index: int, max_length: int) -> str:
    """Format documentation result with pagination information.

    Args:
        url: Documentation URL
        content: Content to format
        start_index: Start index for pagination
        max_length: Maximum content length

    Returns:
        Formatted documentation result
    """
    original_length = len(content)

    if start_index >= original_length:
        return f'Amplify Documentation from {url}:\n\n<e>No more content available.</e>'

    # Calculate the end index, ensuring we don't go beyond the content length
    end_index = min(start_index + max_length, original_length)
    truncated_content = content[start_index:end_index]

    if not truncated_content:
        return f'Amplify Documentation from {url}:\n\n<e>No more content available.</e>'

    actual_content_length = len(truncated_content)
    remaining_content = original_length - (start_index + actual_content_length)

    result = f'Amplify Documentation from {url}:\n\n{truncated_content}'

    # Only add the prompt to continue fetching if there is still remaining content
    if remaining_content > 0:
        next_start = start_index + actual_content_length
        result += f'\n\n<e>Content truncated. Call the read_amplify_documentation tool with start_index={next_start} to get more content.</e>'

    return result


def clean_search_results(search_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Clean and format search results from Algolia.

    Args:
        search_response: Raw search response from Algolia API

    Returns:
        Cleaned and formatted search results
    """
    cleaned_results = []

    # Extract hits from the search response
    hits = []
    if 'results' in search_response and len(search_response['results']) > 0:
        hits = search_response['results'][0].get('hits', [])

    for result in hits:
        # Extract platform information from URL
        platform = 'unknown'
        if 'url' in result:
            import re

            platform_match = re.search(r'docs\.amplify\.aws/([^/]+)', result.get('url', ''))
            if platform_match:
                platform = platform_match.group(1)

        # Extract title and subtitle from hierarchy
        title = result.get('hierarchy', {}).get('lvl0', '')
        subtitle = result.get('hierarchy', {}).get('lvl1', '')

        # Remove " - AWS Amplify Gen 2 Documentation" suffix from title if present
        title = re.sub(r' - AWS Amplify Gen 2 Documentation$', '', title)
        title = re.sub(r' - React - AWS Amplify Gen 2 Documentation$', '', title)

        # Clean snippet from _snippetResult or _highlightResult
        snippet = ''
        highlighted_terms = []

        # First try to get content from _snippetResult
        if '_snippetResult' in result:
            if 'content' in result['_snippetResult']:
                snippet = result['_snippetResult']['content'].get('value', '')
            elif (
                'hierarchy' in result['_snippetResult']
                and 'lvl1' in result['_snippetResult']['hierarchy']
            ):
                snippet = result['_snippetResult']['hierarchy']['lvl1'].get('value', '')

        # If no snippet found, try to get content from the actual content field
        if not snippet and 'content' in result and result['content']:
            # Take first 200 characters as snippet
            snippet = result['content'][:200] + '...'

        # Extract highlighted terms from snippet
        if snippet:
            try:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(snippet, 'html.parser')
                # Extract highlighted terms (marked with <mark> tags in Algolia response)
                for highlight in soup.find_all('mark'):
                    term = highlight.get_text()
                    if term and term not in highlighted_terms:
                        highlighted_terms.append(term)

                # Clean the snippet by removing HTML tags
                clean_snippet = soup.get_text()
                snippet = clean_snippet
            except Exception:
                pass

        # Create the cleaned result object
        cleaned_result = {
            'url': result.get('url', '').split('#')[0],  # Remove fragment identifier
            'title': title,
            'subtitle': subtitle,
            'platform': platform,
            'snippet': snippet,
            'highlighted_terms': highlighted_terms,
        }

        cleaned_results.append(cleaned_result)

    return cleaned_results
