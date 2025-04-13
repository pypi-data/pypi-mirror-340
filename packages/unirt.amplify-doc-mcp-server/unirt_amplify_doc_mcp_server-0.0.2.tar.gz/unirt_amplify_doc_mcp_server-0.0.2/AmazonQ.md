# AWS Amplify Documentation MCP Server Development Project

## Project Overview
- Develop a Model Context Protocol (MCP) server to access and search AWS Amplify Gen 2 documentation
- This MCP server is used to query information about AWS Amplify Gen 2 and retrieve reference information when implementing applications using Amplify Gen 2
- Reference the AWS Documentation MCP Server implementation while adapting it to Amplify-specific requirements
- Provide two main tools: Search Documentation (search functionality using Algolia search API) and Read Documentation (content extraction optimized for Amplify documentation structure)

## Implemented Features

### 1. Project Structure

```
.
├── unirt/
│   ├── __init__.py
│   └── amplify_doc_mcp_server/
│       ├── __init__.py
│       ├── models.py          # Data models
│       ├── server.py          # Main server implementation and tool definitions
│       └── util.py            # Utility functions
├── tests/                     # Test code
│   ├── conftest.py            # Common test settings
│   ├── resources/             # Test resources
│   ├── test_live.py           # Live tests
│   ├── test_models.py         # Model tests
│   ├── test_server.py         # Server tests
│   ├── test_util.py           # Utility tests
│   └── test_util_with_resources.py # Tests using resources
├── pyproject.toml             # Project settings
└── README.md                  # Project description
```

### 2. Implemented Tools

#### 2.1 `search_amplify_documentation`

```python
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
```

- **Function**: Search Amplify Gen 2 documentation using the Algolia search API
- **Features**:
  - Filtering by platform (react, vue, swift, android, flutter)
  - Uses React platform by default
  - Search results include URL, title, snippet, highlighted terms, and other information
  - Limited to Gen 2 documentation

#### 2.2 `read_amplify_documentation`

```python
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
```

- **Function**: Retrieve Amplify documentation pages and convert them to Markdown format
- **Features**:
  - Only supports URLs from the docs.amplify.aws domain
  - Pagination functionality to retrieve long documents in chunks
  - Optimized HTML to Markdown conversion
  - Removes unnecessary elements (navigation, footer, etc.)

### 3. Data Model

```python
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
```

### 4. Test Implementation

- **Unit Tests**: Function-level tests using mocks
- **Live Tests**: Tests that call the actual API (run with the `--run-live` option)
- **Resource-based Tests**: Tests using sample HTML and JSON

## Technical Features

1. **FastMCP Framework**: Used for MCP server implementation
2. **Asynchronous Processing**: Asynchronous HTTP requests using `httpx`
3. **Error Handling**: Comprehensive error handling and reporting
4. **Content Processing**: HTML to Markdown conversion using BeautifulSoup and markdownify
5. **Test Strategy**: Separation of unit tests and live tests

## Future Improvements (Idea)

1. **Add Caching Functionality**:
   - Cache frequently accessed documents to reduce response time
   - Set TTL (Time To Live) for periodic updates

2. **Improve Search Results**:
   - Optimize code block extraction and display
   - Adjust relevance scores
   - Group search results (by topic, etc.)

3. **Strengthen Error Handling**:
   - More detailed error messages
   - Add retry functionality
   - Detect and handle rate limits

4. **Performance Optimization**:
   - Parallel request processing
   - Optimize response size
   - Pre-filter unnecessary HTML

5. **Add New Features**:
   - `recommend_amplify_documentation`: Recommend related documentation
   - `list_amplify_examples`: List sample code
   - `get_amplify_version_info`: Get version information

## Development Rules

### Running Tests

```bash
# Unit tests (excluding live tests)
pytest -m "not live"

# Live tests
pytest tests/test_live.py --run-live -v

# All tests
pytest
```

### Code Quality Checks

```bash
# Code formatting and linting
ruff format .
ruff check .
```

### Commit Message Convention

```
<type>: <description>

[optional body]

[optional footer]
```

Types to use:

- feat: New feature
- fix: Bug fix
- docs: Documentation changes only
- style: Changes that do not affect code meaning (whitespace, formatting, etc.)
- refactor: Code changes that are neither bug fixes nor new features
- test: Adding or modifying tests
- chore: Changes to build process or tools
