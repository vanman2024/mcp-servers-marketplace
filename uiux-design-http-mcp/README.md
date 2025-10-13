# UI/UX Design HTTP MCP Server

A comprehensive FastMCP server for UI/UX design workflows with sequential thinking capabilities, OpenAI integration, and orchestration of other MCP servers for complete design pipeline automation.

## Features

- **Sequential design thinking** with structured problem-solving approach
- **Design system generation** with automated component creation
- **User journey mapping** with AI-powered insights
- **Accessibility evaluation** against WCAG standards
- **Cross-platform design** strategies and optimization
- **MCP server orchestration** to leverage V0, MUI, and other design tools
- **AI-powered analysis** using OpenAI for design critique and insights

## Server Organization

### 🛠️ Tools (6 main tools)
- **Sequential Design Thinking**: Apply structured thinking process to design challenges
- **Generate Design System**: Create comprehensive design systems with components
- **Create User Journey Map**: Map user journeys with touchpoints and emotions
- **Evaluate Accessibility**: WCAG compliance evaluation with recommendations
- **Orchestrate Design Pipeline**: Complete design pipeline using multiple MCP servers
- **MCP Tool Integration**: Call tools from other MCP servers (V0, MUI, etc.)

### 📚 Resources (5 resource endpoints)
- **Templates**: Complete design system templates and component specifications
- **UI Patterns**: Common design patterns and best practices library
- **Accessibility Guidelines**: WCAG guidelines and implementation checklists
- **Design Examples**: Platform-specific examples (mobile, web, desktop)
- **Design Process Workflows**: Complete design methodologies and processes

### 💡 Prompts (7 specialized prompts)
- **Design Critique**: Comprehensive design evaluation and feedback generation
- **User Persona Development**: Detailed user persona creation from research
- **Accessibility Audit**: WCAG compliance auditing and recommendations
- **Design System Scaling**: Strategies for evolving design systems
- **User Flow Optimization**: Conversion-focused flow optimization
- **Cross-Platform Design**: Multi-platform design strategy development
- **Design System Governance**: Team collaboration and adoption frameworks

## Key Capabilities

### Sequential Thinking Integration
Uses the sequential-thinking MCP server to apply structured problem-solving to design challenges, ensuring thorough analysis and systematic approach to complex design problems.

### Multi-Server Orchestration
Coordinates with multiple MCP servers:
- **Vercel V0**: For modern React component generation
- **MUI Server**: For Material-UI component creation
- **Sequential Thinking**: For structured problem analysis
- **OpenAI Tools**: For AI-powered insights
- **GitHub**: For version control and collaboration

### AI-Powered Analysis
Leverages OpenAI GPT-4 for:
- Design critique and feedback
- User journey analysis
- Accessibility evaluation
- Design pattern recommendations

### Comprehensive Design Pipeline
End-to-end design workflow including:
1. Sequential design thinking
2. Design system generation
3. Component creation via multiple servers
4. Accessibility validation
5. User journey mapping
6. Cross-platform optimization

## Setup

1. **Install dependencies:**
   ```bash
   cd servers/http/uiux-design-http-mcp
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and server URLs
   export OPENAI_API_KEY=your_openai_api_key
   export V0_API_KEY=your_v0_api_key
   export UIUX_DESIGN_MCP_PORT=8025
   ```

3. **Start other MCP servers** (for full orchestration):
   ```bash
   # Start V0 server on port 8010
   # Start MUI server on port 8020
   # Start Sequential Thinking server on port 8013
   ```

4. **Run the server:**
   ```bash
   python src/uiux_design_server.py
   ```

## Usage with Claude

1. **Add to Claude:**
   ```bash
   claude mcp add --transport http uiux-design-http http://localhost:8025
   ```

2. **Use design tools:**
   ```bash
   # Sequential design thinking
   /mcp__uiux-design-http__sequential_design_thinking "Create mobile app for fitness tracking" "Health-conscious millennials"
   
   # Generate design system
   /mcp__uiux-design-http__generate_design_system "FitApp" '["#007AFF", "#34C759"]' "modular" '["button", "card", "form"]'
   
   # Create user journey map
   /mcp__uiux-design-http__create_user_journey_map "FitApp" "Health-conscious millennial" '["awareness", "signup", "onboarding", "daily_use", "goal_achievement"]'
   
   # Evaluate accessibility
   /mcp__uiux-design-http__evaluate_accessibility '[{"name": "login_form", "type": "form", "interactive": true, "colors": ["#007AFF"]}]' "AA"
   
   # Orchestrate full pipeline
   /mcp__uiux-design-http__orchestrate_design_pipeline "FitApp" '{"challenge": "fitness tracking", "target_users": "millennials", "brand_colors": ["#007AFF"]}' '["mobile", "web"]'
   ```

3. **Access design resources:**
   ```bash
   # Design system templates
   /mcp_resource design://templates/design-system
   
   # UI patterns library
   /mcp_resource design://patterns/ui-patterns
   
   # Accessibility guidelines
   /mcp_resource design://guidelines/accessibility
   
   # Design examples by category
   /mcp_resource design://examples/mobile
   /mcp_resource design://examples/web
   
   # Design process workflows
   /mcp_resource design://workflows/design-process
   ```

4. **Use specialized prompts:**
   ```bash
   # Design critique
   /mcp_prompt design_critique_prompt "Mobile app with complex navigation" "busy professionals"
   
   # User persona development
   /mcp_prompt user_persona_development_prompt "fitness app" "survey data shows users want simple tracking"
   
   # Accessibility audit
   /mcp_prompt accessibility_audit_prompt "web dashboard" "AAA"
   
   # Design system scaling
   /mcp_prompt design_system_scaling_prompt "basic component library" "need dark mode and mobile components"
   ```

## Advanced Features

### MCP Server Orchestration
The server can coordinate with other MCP servers to create a complete design pipeline:

```python
# Example: Generate components using multiple servers
orchestrator.call_mcp_tool('vercel-v0', 'generate_component', 
                          prompt="Create modern button component",
                          component_name="PrimaryButton")

orchestrator.call_mcp_tool('mui', 'generate_component',
                          component_type="card",
                          variant="elevated")
```

### Sequential Thinking Integration
Applies structured thinking to design challenges:

```python
# Multi-step design thinking process
sequential_design_thinking(
    design_challenge="Improve mobile app onboarding",
    target_users="first-time users",
    thinking_steps=7
)
```

### AI-Powered Analysis
Uses OpenAI for intelligent design insights:

```python
# AI-powered user journey analysis
create_user_journey_map(
    product_name="E-commerce App",
    user_persona="Busy parent shopping online",
    journey_stages=["discovery", "research", "purchase", "delivery"]
)
```

## Architecture

The server is built with:
- **FastMCP framework** for HTTP MCP server implementation
- **Async/await patterns** for concurrent processing
- **Type hints** for code clarity and IDE support
- **Comprehensive error handling** with graceful degradation
- **Context-aware logging** and progress reporting
- **Modular design** for easy extension and maintenance

## Extension Points

To add new design capabilities:

1. **Add new tools** using the `@mcp.tool()` decorator
2. **Create resources** with `@mcp.resource()` for design assets
3. **Develop prompts** using `@mcp.prompt` for AI interactions
4. **Extend orchestration** by adding new MCP server integrations
5. **Enhance analysis** by integrating additional AI models or services

## Best Practices

- **User-centered approach**: Always prioritize user needs and accessibility
- **Design system consistency**: Maintain coherent design languages
- **Iterative improvement**: Use feedback loops for continuous enhancement
- **Cross-platform thinking**: Consider all target platforms from the start
- **Performance optimization**: Balance visual richness with performance
- **Accessibility first**: Build inclusive designs from the beginning

## Contributing

To contribute to the UI/UX Design MCP Server:

1. Follow the established code organization patterns
2. Add comprehensive docstrings for all functions
3. Include proper error handling and logging
4. Test with multiple design scenarios
5. Update documentation for new features
6. Consider cross-platform implications for new tools

## Dependencies

- `fastmcp>=2.0.0` - FastMCP framework for HTTP MCP servers
- `httpx>=0.24.0` - HTTP client for MCP server communication
- `openai>=1.0.0` - OpenAI API integration for AI analysis
- `pydantic>=2.0.0` - Data validation and type checking
- `uvicorn>=0.24.0` - ASGI server for HTTP transport

## License

This MCP server is part of the MCP kernel testing suite and follows the same licensing terms.