"""Data models for the Amplify Gen 2 Documentation MCP Server."""

from pydantic import BaseModel, Field
from typing import List, Optional


class AmplifyDocSearchResult(BaseModel):
    """Search result from AWS Amplify documentation."""

    url: str = Field(description='URL of the documentation page')
    title: str = Field(description='Title of the documentation page')
    subtitle: Optional[str] = Field(
        None, description='Subtitle or section of the documentation page'
    )
    platform: str = Field(description='Platform (react, vue, swift, etc.)')
    snippet: Optional[str] = Field(None, description='Brief excerpt or summary of the content')
    highlighted_terms: List[str] = Field(
        default_factory=list, description='Terms that matched the search query'
    )
