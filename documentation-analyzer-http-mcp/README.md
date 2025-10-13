# Documentation Analyzer HTTP MCP Server

AI-powered documentation analysis and management server with comprehensive tools for indexing, analyzing, searching, and managing project documentation.

## Features

- **Comprehensive Documentation Indexing**: Index multiple file types with metadata extraction
- **AI-Powered Quality Analysis**: Automated quality assessment with improvement suggestions  
- **Advanced Search Capabilities**: Full-text search with relevance scoring
- **Change Detection**: Detect and track documentation changes over time
- **Smart Categorization**: AI-powered document categorization
- **Summary Generation**: Generate comprehensive documentation summaries
- **Real-time Updates**: Live monitoring of documentation changes

## Server Organization

The server is organized into clear sections:

### 🛠️ Tools (13 main tools)

#### **Core Documentation Tools**
- **index_documentation**: Comprehensive file indexing with metadata extraction
- **search_documentation**: Advanced search with relevance scoring
- **get_documentation_stats**: Detailed index statistics and metrics
- **detect_documentation_changes**: Change detection and tracking

#### **AI-Powered Analysis Tools**  
- **analyze_documentation_quality**: Quality assessment with improvement suggestions
- **generate_documentation_summary**: Comprehensive summary generation
- **ai_categorize_documentation**: Smart document categorization
- **ai_summarize_documentation**: AI-powered content summarization

### 📚 Resources (5+ resource endpoints)

- **docs://index**: Complete documentation index with metadata
- **docs://stats**: Real-time index statistics and metrics
- **docs://search/{query}**: Direct search access via resource endpoint
- **docs://quality/{path}**: Quality assessment for specific documents
- **docs://relationships**: Document relationships and cross-references

### 💡 Prompts (5 specialized prompts)

#### **Analysis & Planning Prompts**
- **analyze_project_documentation**: Comprehensive project documentation analysis
- **generate_documentation_template**: Create templates for specific doc types
- **documentation_migration_plan**: Plan format conversions and migrations
- **api_documentation_review**: Review API documentation completeness
- **create_onboarding_documentation**: Design onboarding documentation structure

## Capabilities

### Document Processing
- **Multi-format Support**: Markdown, reStructuredText, HTML, code files, config files
- **Metadata Extraction**: Headers, word counts, code blocks, classes, functions
- **Content Analysis**: Quality metrics, structure assessment, completeness scoring
- **Change Tracking**: Hash-based change detection with detailed diff reporting

### AI Integration
- **Quality Assessment**: Automated scoring across multiple quality dimensions
- **Smart Categorization**: AI-powered document type classification
- **Content Summarization**: Context-aware summary generation
- **Improvement Suggestions**: Actionable recommendations for documentation enhancement

### Search & Discovery
- **Full-text Search**: Token-based search with relevance scoring
- **Faceted Search**: Filter by document type, quality score, or modification date
- **Relationship Mapping**: Track cross-references and dependencies
- **Statistics Dashboard**: Comprehensive metrics and usage analytics

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export DOCUMENTATION_ANALYZER_MCP_PORT=8036     # Optional
   export OPENAI_API_KEY=your_openai_key           # For AI features
   export ANTHROPIC_API_KEY=your_anthropic_key     # Alternative AI provider
   ```

3. Run the server:
   ```bash
   python src/documentation_analyzer_server.py
   ```

## Usage with Claude

1. Add to Claude:
   ```bash
   claude mcp add --transport http documentation-analyzer-http http://localhost:8036
   ```

2. Use tools:
   - List: `/mcp`
   - Index documentation: `/mcp__documentation_analyzer__index_documentation "/path/to/docs" true`
   - Search: `/mcp__documentation_analyzer__search_documentation "API reference"`
   - Quality analysis: `/mcp__documentation_analyzer__analyze_documentation_quality`

3. Access resources:
   ```bash
   /mcp_resource docs://index
   /mcp_resource docs://stats  
   /mcp_resource docs://search/installation
   /mcp_resource docs://quality/README.md
   ```

## Configuration

The server can be configured via environment variables:

- `DOCUMENTATION_ANALYZER_MCP_PORT`: Server port (default: 8036)
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `ANTHROPIC_API_KEY`: Anthropic API key for AI features

### Supported File Types

- **Documentation**: `.md`, `.rst`, `.txt`, `.adoc`, `.html`, `.xml`
- **Code Files**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.h`, `.hpp`, `.go`, `.rs`, `.rb`, `.php`, `.cs`, `.swift`, `.kt`
- **Configuration**: `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.conf`

## API Examples

### Index Project Documentation
```python
result = await index_documentation(
    directory="/path/to/project/docs",
    recursive=True,
    extensions=[".md", ".rst", ".py"]
)
```

### Search Documentation
```python
results = await search_documentation(
    query="authentication API",
    limit=10,
    doc_types=[".md"]
)
```

### Analyze Documentation Quality
```python
analysis = await analyze_documentation_quality(
    paths=["docs/api/", "README.md"],
    include_suggestions=True
)
```

### Generate Project Summary
```python
summary = await generate_documentation_summary(
    format="markdown",
    include_toc=True
)
```

## Integration with DevLoop Workflow

This server integrates seamlessly with the DevLoop SDLC workflow:

1. **Planning Phase**: Analyze existing documentation to understand project structure
2. **Development Phase**: Monitor documentation changes during feature development
3. **Testing Phase**: Validate documentation quality as part of QA process
4. **Deployment Phase**: Generate updated documentation summaries
5. **Maintenance Phase**: Track documentation drift and suggest improvements

## Performance Considerations

- **Indexing**: Optimized for projects with up to 10,000 documents
- **Search**: Sub-second response times for typical queries
- **Memory Usage**: Efficient in-memory indexing with configurable cache limits
- **Concurrency**: Thread-safe operations for parallel access

## Quality Metrics

The quality analysis evaluates documents across five dimensions:

1. **Completeness**: Word count, section coverage, depth of information
2. **Clarity**: Sentence structure, readability, technical complexity
3. **Structure**: Header organization, logical flow, navigation
4. **Consistency**: Formatting, terminology, style adherence
5. **Technical Accuracy**: Code examples, API documentation, technical details

Each dimension is scored 0-10, with an overall quality score calculated as the average.

## AI Features

When AI API keys are configured, the server provides enhanced capabilities:

- **Advanced Categorization**: Use natural language processing for document classification
- **Intelligent Summarization**: Context-aware content summarization
- **Quality Insights**: Deep analysis of documentation effectiveness
- **Improvement Recommendations**: Specific, actionable suggestions for enhancement

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Permission Errors**: Check read permissions for indexed directories
3. **Memory Issues**: Reduce index size or increase available memory
4. **AI Features Not Working**: Verify API keys are correctly set

### Debug Mode

Enable detailed logging by setting:
```bash
export PYTHONPATH=.
export DOCUMENTATION_ANALYZER_DEBUG=1
python src/documentation_analyzer_server.py
```

## Contributing

This server follows the FastMCP development patterns:

1. **Simple Tools**: Use `@mcp.tool()` decorator for standalone operations
2. **Complex Tools**: Use class-based pattern for multi-step operations
3. **Resources**: Provide direct data access via URI patterns
4. **Prompts**: Include specialized prompts for common documentation tasks

## License

Part of the MCP Kernel project. See project root for license information.