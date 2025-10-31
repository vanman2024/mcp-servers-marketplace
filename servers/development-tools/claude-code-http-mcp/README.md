# Claude Code HTTP MCP Server

A comprehensive FastMCP server that integrates Claude Code SDK with OpenAI Responses API for the SynapseAI platform. This server positions Claude as the PRIMARY development tool while enabling seamless orchestration through OpenAI's Responses API.

## 🎯 Purpose in SynapseAI Architecture

This server bridges OpenAI Responses API (orchestrator) with Claude Code SDK (primary developer) to create a powerful autonomous development system:

```
OpenAI Responses API → Claude Code MCP Server → Claude Code SDK
    (Orchestration)         (Integration)         (Development)
```

### Key Architectural Principles:
- **Claude as Primary Developer**: Handles 80%+ of all development work
- **OpenAI as Orchestrator**: Manages workflows, coordination, and UI generation
- **Seamless Integration**: Minimal latency handoffs between systems
- **Production Quality**: All outputs are deployment-ready

## 🏗️ Server Organization

### 🛠️ Tools (6 main development tools)
- **execute_development_task**: Core development execution (Claude as primary)
- **coordinate_with_openai_responses_api**: Seamless OpenAI integration
- **debug_across_stack**: Universal debugging tool (all languages/frameworks)
- **generate_comprehensive_tests**: Complete testing suite generation
- **manage_parallel_claude_instances**: Multi-instance coordination
- **optimize_performance**: Performance and scalability optimization

### 📚 Resources (7 comprehensive resource endpoints)
- **integration-patterns**: SynapseAI integration patterns and best practices
- **responses-api-bridge**: OpenAI Responses API bridge specifications
- **execution-templates/{mode}**: Claude execution templates by mode
- **project-examples/{type}**: Example project configurations
- **best-practices**: Development and integration best practices
- **architecture-patterns**: System architecture patterns
- **performance-metrics**: Performance monitoring and optimization

### 💡 Prompts (6 specialized prompts)
- **claude_primary_developer_prompt**: Optimized for Claude as main developer
- **claude_debugging_specialist_prompt**: Universal debugging across all stacks
- **claude_testing_specialist_prompt**: Comprehensive testing across frameworks
- **openai_claude_coordination_prompt**: Seamless handoff coordination
- **synapse_integration_optimization_prompt**: System performance optimization
- **parallel_execution_coordination_prompt**: Multi-instance management

## 🚀 Features

### Core Integration Capabilities
- **Primary Development Mode**: Claude handles all coding tasks
- **Universal Debugging**: Debug across Python, TypeScript, SQL, and more
- **Comprehensive Testing**: Generate tests for all frameworks (pytest, jest, playwright)
- **Performance Optimization**: Automatic performance tuning and scalability
- **Parallel Execution**: Coordinate multiple Claude instances
- **Quality Assurance**: Built-in quality gates and security scanning

### OpenAI Responses API Integration
- **Stateless Operation**: Compatible with OpenAI's stateless API design
- **Streaming Support**: Real-time progress updates via server-sent events
- **Function Calling**: Native OpenAI function calling compatibility
- **Session Correlation**: Maintain context across API boundaries
- **Error Recovery**: Graceful degradation and retry mechanisms

### SynapseAI Ecosystem Integration
- **Supabase Integration**: Direct database operations and activity tracking
- **GitHub Integration**: Automatic repository management and deployment
- **Vercel Integration**: Seamless deployment pipeline integration
- **MCP Server Coordination**: Work with other MCP servers in the ecosystem
- **Real-time Monitoring**: Live progress tracking and performance metrics

## 📦 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

Required environment variables:
- `ANTHROPIC_API_KEY`: For Claude Code SDK integration
- `OPENAI_API_KEY`: For OpenAI Responses API coordination
- `CLAUDE_CODE_MCP_PORT`: Server port (default: 8035)

### 3. Run the Server
```bash
python src/claude_code_server.py
```

The server will start on `http://localhost:8035` by default.

## 🔧 Usage with Claude

### 1. Add to Claude Configuration
```bash
claude mcp add --transport http claude-code-http http://localhost:8035
```

### 2. Execute Development Tasks
```bash
# Primary development task
/mcp__claude_code__execute_development_task "Build user authentication system" "SaaS project with FastAPI backend" "primary_developer"

# Universal debugging
/mcp__claude_code__debug_across_stack "Login endpoint returning 500 error" "backend,database" "error_logs" "stack_trace"

# Comprehensive testing
/mcp__claude_code__generate_comprehensive_tests "user_auth_module" "unit,integration,e2e" 95 true true
```

### 3. Access Resources
```bash
# Integration patterns
/mcp_resource claude-code://integration-patterns

# Execution templates
/mcp_resource claude-code://execution-templates/primary_developer

# Project examples
/mcp_resource claude-code://project-examples/saas
```

## 🎯 Integration with OpenAI Responses API

### Function Calling Pattern
```python
# OpenAI Responses API calls Claude Code MCP
response = await openai.responses.create({
    "model": "gpt-4",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "claude_code_execute_development_task",
                "description": "Execute development task using Claude as primary developer",
                "parameters": {
                    "task_description": "Build user authentication system",
                    "execution_mode": "primary_developer"
                }
            }
        }
    ],
    "tool_choice": "required"
})
```

### Coordination Flow
1. **OpenAI Orchestration**: Plans and coordinates the overall workflow
2. **Task Handoff**: Passes development tasks to Claude via MCP
3. **Claude Development**: Claude executes as primary developer (80%+ of work)
4. **Result Integration**: Results flow back to OpenAI for continued orchestration
5. **Quality Assurance**: Automatic testing, validation, and deployment preparation

## 🔄 Execution Modes

### Primary Developer Mode (Default)
- Claude handles complete feature implementation
- Production-ready code with comprehensive testing
- Security best practices and performance optimization
- Documentation and deployment configurations

### Debugging Specialist Mode
- Universal debugging across all languages and frameworks
- Root cause analysis and comprehensive fixes
- Prevention strategies and monitoring recommendations
- Cross-stack expertise (Python, TypeScript, SQL, etc.)

### Testing Specialist Mode
- Comprehensive test generation across all frameworks
- Unit, integration, E2E, performance, and security testing
- High coverage targets (>90%) with edge case handling
- CI/CD integration and automated quality gates

### Optimization Mode
- Performance analysis and optimization
- Scalability improvements and resource management
- Caching strategies and database optimization
- Monitoring and alerting setup

## 📊 Performance Metrics

### Target Performance
- **Handoff Latency**: < 100ms between OpenAI and Claude
- **Task Completion**: < 5 minutes average for standard tasks
- **Code Quality**: > 95% automated quality score
- **Test Coverage**: > 90% minimum coverage
- **Deployment Readiness**: 100% of completed tasks

### Monitoring and Alerts
- Real-time performance tracking
- Quality metric monitoring
- Resource utilization alerts
- Error rate and retry monitoring
- Integration health checks

## 🏆 Best Practices

### Claude as Primary Developer
- Route all coding tasks to Claude first
- Use Claude for debugging across all languages
- Claude generates all test suites and quality assurance
- Claude handles performance optimization and security
- Claude ensures deployment readiness

### OpenAI Orchestration
- OpenAI creates project plans and coordinates workflows
- OpenAI manages handoffs between multiple Claude instances
- OpenAI generates UI components via v0 integration
- OpenAI provides progress updates and user communication
- OpenAI handles high-level decision making and planning

### Quality Assurance
- Automatic test generation with >90% coverage
- Built-in security scanning and validation
- Performance benchmarking and optimization
- Code quality gates before deployment
- Comprehensive documentation generation

### Scalability
- Parallel Claude instances for large projects
- Dependency-aware task coordination
- Resource management and load balancing
- Horizontal scaling based on demand
- Performance monitoring and optimization

## 🔐 Security

- No hardcoded API keys (environment variables only)
- Automatic security vulnerability scanning
- Input validation and sanitization
- Rate limiting and abuse prevention
- Audit logging and monitoring

## 🔧 Development

### Testing
```bash
# Run tests
python -m pytest tests/

# Coverage report
python -m pytest --cov=src tests/
```

### Debugging
```bash
# Enable debug mode
export CLAUDE_CODE_DEBUG=true
python src/claude_code_server.py
```

## 📈 Future Enhancements

- [ ] Advanced Claude Code SDK integration with real execution
- [ ] Enhanced parallel instance coordination
- [ ] Custom agent training and specialization
- [ ] Advanced performance monitoring and optimization
- [ ] Integration with additional SynapseAI services
- [ ] Real-time collaboration features

## 📞 Support

For issues and feature requests, please refer to the SynapseAI documentation or contact the development team.

## 🧪 Test Results (Latest Run: 2025-07-27)

### Test Summary
- **Total Tests**: 22
- **Passed**: 12
- **Failed**: 10
- **Success Rate**: 54.55%
- **Deployment Status**: ❌ NOT_READY

### Known Issues
1. **MCP Protocol Compliance**: Server requires StreamableHTTP client implementation
2. **Standard HTTP/SSE clients**: Receive 406 Not Acceptable response
3. **Session Management**: MCP protocol initialization requires specific session handling

### Critical Failures
- `execute_claude_code_direct`: Command line option parsing error
- `error_missing_params`: Parameter validation not raising errors correctly
- `mcp_initialization`: Protocol initialization failing with standard clients

### Performance Metrics
- Average tool execution time: < 1ms (excellent)
- Small task completion: 859.66ms
- Medium task completion: 812.01ms
- Large task completion: 936.37ms

### Deployment Requirements
Before cloud deployment, the following issues must be resolved:
1. Implement proper MCP protocol compliance
2. Fix critical test failures
3. Improve test coverage to >85%
4. Add proper error handling for missing parameters
5. Update session management for cloud compatibility

### Test Report Location
Detailed test reports available at:
- Console Report: `test-claude-code-comprehensive-*/reports/final_report_console.txt`
- HTML Report: `test-claude-code-comprehensive-*/reports/final_report.html`
- JSON Report: `test-claude-code-comprehensive-*/reports/final_report.json`

---

**Built for SynapseAI** - Empowering autonomous software development through intelligent AI coordination.