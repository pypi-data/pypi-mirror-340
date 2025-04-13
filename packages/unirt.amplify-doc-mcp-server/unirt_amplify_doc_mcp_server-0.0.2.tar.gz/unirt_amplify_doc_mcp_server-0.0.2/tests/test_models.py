"""Tests for data models in the Amplify Documentation MCP Server."""

from unirt.amplify_doc_mcp_server.models import AmplifyDocSearchResult


class TestAmplifyDocSearchResult:
    """Tests for AmplifyDocSearchResult model."""

    def test_search_result_creation(self):
        """Test creation of AmplifyDocSearchResult."""
        result = AmplifyDocSearchResult(
            url='https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/',
            title='Set up Amplify Auth',
            platform='react',
            snippet='Amplify Auth is powered by Amazon Cognito...',
            highlighted_terms=['Auth', 'Cognito'],
        )
        assert result.url == 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        assert result.title == 'Set up Amplify Auth'
        assert result.platform == 'react'
        assert result.snippet == 'Amplify Auth is powered by Amazon Cognito...'
        assert 'Auth' in result.highlighted_terms
        assert 'Cognito' in result.highlighted_terms

    def test_search_result_with_subtitle(self):
        """Test creation of AmplifyDocSearchResult with subtitle."""
        result = AmplifyDocSearchResult(
            url='https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/',
            title='Set up Amplify Auth',
            subtitle='Authentication',
            platform='react',
            snippet='Amplify Auth is powered by Amazon Cognito...',
            highlighted_terms=['Auth'],
        )
        assert result.url == 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        assert result.title == 'Set up Amplify Auth'
        assert result.subtitle == 'Authentication'
        assert result.platform == 'react'
        assert result.snippet == 'Amplify Auth is powered by Amazon Cognito...'
        assert 'Auth' in result.highlighted_terms

    def test_search_result_minimal(self):
        """Test creation of AmplifyDocSearchResult with minimal fields."""
        result = AmplifyDocSearchResult(
            url='https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/',
            title='Set up Amplify Auth',
            platform='react',
        )
        assert result.url == 'https://docs.amplify.aws/react/build-a-backend/auth/set-up-auth/'
        assert result.title == 'Set up Amplify Auth'
        assert result.platform == 'react'
        assert result.snippet is None
        assert result.subtitle is None
        assert result.highlighted_terms == []
