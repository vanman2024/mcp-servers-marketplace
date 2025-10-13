# Gemini MCP Server (HTTP)

Google Gemini AI capabilities for text generation, vision analysis, code review, and structured outputs.

## Features

- **Text Generation**: High-quality text generation with multiple models
- **Code Analysis**: Bug detection, performance analysis, security review
- **Vision & Multimodal**: Image analysis and comparison
- **Structured Output**: JSON generation with schema validation
- **Entity Extraction**: Named entity recognition from text
- **Conversation**: Multi-turn chat conversations
- **Content Analysis**: Summarization and translation
- **HTTP Transport**: FastMCP with streamable-http

## Tools

### Text Generation
- `generate_text(prompt, model?, temperature?, max_output_tokens?, safety_level?)` - Generate text with Gemini
- `analyze_code(code, language?, analysis_type?, model?)` - Comprehensive code analysis

### Vision & Multimodal
- `analyze_image(image_path, prompt, model?)` - Analyze images with text prompts
- `compare_images(image1_path, image2_path, comparison_prompt?, model?)` - Compare two images

### Structured Output
- `generate_json(prompt, schema, model?)` - Generate JSON matching a schema
- `extract_entities(text, entity_types, model?)` - Extract named entities from text

### Conversation
- `chat_conversation(messages, model?, temperature?)` - Multi-turn conversations

### Content Analysis
- `summarize_text(text, length?, focus?, model?)` - Intelligent text summarization
- `translate_text(text, target_language, source_language?, model?)` - Language translation

## Configuration

### Environment Variables

```bash
# Google AI API key (required)
GOOGLE_API_KEY=your_google_api_key_here
# OR
GEMINI_API_KEY=your_google_api_key_here

# Server port
GEMINI_MCP_PORT=8014
```

### Default Settings
- **Default port**: 8014
- **Transport**: streamable-http
- **Default model**: gemini-2.0-flash
- **Temperature**: 0.7

## Installation

```bash
# Install dependencies
pip install fastmcp python-dotenv uvicorn httpx google-generativeai Pillow

# Run server
python src/gemini_server.py
```

## Usage Examples

### Text Generation
```python
{
    "name": "generate_text",
    "arguments": {
        "prompt": "Write a technical explanation of how machine learning works",
        "model": "gemini-1.5-pro",
        "temperature": 0.8,
        "max_output_tokens": 1000
    }
}
```

### Code Analysis
```python
{
    "name": "analyze_code",
    "arguments": {
        "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
        "language": "python",
        "analysis_type": "comprehensive"
    }
}
```

### Image Analysis
```python
{
    "name": "analyze_image",
    "arguments": {
        "image_path": "/path/to/image.jpg",
        "prompt": "Describe what you see in this image and identify any text or important details"
    }
}

{
    "name": "compare_images",
    "arguments": {
        "image1_path": "/path/to/before.jpg",
        "image2_path": "/path/to/after.jpg",
        "comparison_prompt": "What changes were made between these two screenshots?"
    }
}
```

### Structured JSON Generation
```python
{
    "name": "generate_json",
    "arguments": {
        "prompt": "Create a sample user profile for a software developer",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "skills": {"type": "array", "items": {"type": "string"}},
                "experience_years": {"type": "number"},
                "contact": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string"},
                        "github": {"type": "string"}
                    }
                }
            }
        }
    }
}
```

### Entity Extraction
```python
{
    "name": "extract_entities",
    "arguments": {
        "text": "John Smith works at Google in Mountain View, California. He started on January 15, 2020 and reports to Sarah Johnson.",
        "entity_types": ["person", "organization", "location", "date"]
    }
}
```

### Multi-turn Conversation
```python
{
    "name": "chat_conversation",
    "arguments": {
        "messages": [
            {"role": "user", "content": "What is machine learning?"},
            {"role": "assistant", "content": "Machine learning is a subset of artificial intelligence..."},
            {"role": "user", "content": "Can you give me a practical example?"}
        ],
        "temperature": 0.7
    }
}
```

### Content Analysis
```python
{
    "name": "summarize_text",
    "arguments": {
        "text": "Long article text here...",
        "length": "medium",
        "focus": "main_points"
    }
}

{
    "name": "translate_text",
    "arguments": {
        "text": "Hello, how are you today?",
        "target_language": "Spanish",
        "source_language": "English"
    }
}
```

## Model Options

### Available Models
- `gemini-2.0-flash` - Latest model with multimodal capabilities (December 2024)
- `gemini-1.5-pro` - Powerful model for complex reasoning
- `gemini-1.5-flash` - Fast and efficient for most tasks

### Model Capabilities
- **Text Generation**: All models
- **Vision**: All models (gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash)  
- **Code Analysis**: All models (pro recommended)
- **Structured Output**: All models

## Safety Settings

### Safety Levels
- `strict` - Block low and above harmful content
- `moderate` - Block medium and above (default)
- `permissive` - Block only high-level harmful content

### Safety Categories
- Harassment
- Hate speech  
- Sexually explicit content
- Dangerous content

## Code Analysis Types

### Analysis Options
- `comprehensive` - Full analysis (bugs, performance, security, readability)
- `bugs` - Focus on potential bugs and errors
- `performance` - Optimization opportunities
- `security` - Security vulnerabilities
- `explain` - Code explanation and documentation

## HTTP Endpoints

The server runs on `http://localhost:8014` with MCP tools available at:
- `POST /tools/call` - Execute MCP tools
- `GET /tools/list` - List available tools
- `GET /health` - Health check

## Rate Limits

Google AI API has limits:
- **Free tier**: 15 requests per minute, 1,500 requests per day
- **Paid tier**: Higher limits based on billing
- **Token limits**: Vary by model

## Error Handling

Common errors and solutions:
- **401**: Invalid API key
- **429**: Rate limit exceeded - implement backoff
- **400**: Invalid request format
- **403**: Safety filters blocked content

## Best Practices

### Text Generation
- Use appropriate temperature (0.0-2.0)
- Set reasonable token limits
- Consider safety settings for content

### Vision Analysis
- Use clear, high-quality images
- Provide specific, detailed prompts
- Supported formats: JPEG, PNG, WebP, HEIC

### Code Analysis
- Include language hints for better analysis
- Specify analysis type for focused results
- Review security recommendations carefully

### Structured Output
- Provide clear, well-defined schemas
- Handle JSON parsing errors gracefully
- Validate generated data against schema

## Cost Optimization

### Model Selection
- Use `gemini-1.5-flash` for routine tasks
- Use `gemini-1.5-pro` for complex reasoning
- Consider prompt length for cost efficiency

### Token Management
- Set appropriate max_output_tokens
- Use summarization for long texts
- Batch related requests when possible

## Security Notes

- API key has access to Google AI services
- Content is processed by Google's AI models
- Consider privacy implications for sensitive data
- Vision analysis sends images to Google

## Getting an API Key

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Set the `GOOGLE_API_KEY` environment variable

## Testing

```bash
# Test text generation
curl -X POST http://localhost:8014/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "generate_text",
    "arguments": {
        "prompt": "Explain quantum computing in simple terms",
        "max_output_tokens": 200
    }
  }'

# Test code analysis
curl -X POST http://localhost:8014/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "analyze_code",
    "arguments": {
        "code": "print(\"Hello World\")",
        "language": "python",
        "analysis_type": "explain"
    }
  }'
```