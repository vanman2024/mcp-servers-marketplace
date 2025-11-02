# ngrok HTTP MCP Server

A comprehensive Model Context Protocol (MCP) server that provides full integration with the ngrok API, enabling agents to create, manage, and monitor ngrok tunnels, edges, backends, and security policies for testing and development workflows.

## 🚀 Features

### Core Capabilities
- **Tunnel Management**: Create, configure, and monitor HTTP/HTTPS/TCP tunnels
- **Edge Configuration**: Advanced routing, load balancing, and traffic management
- **Backend Services**: Connect tunnels to local services and cloud backends
- **Authentication**: OAuth, basic auth, API keys, and custom authentication
- **Domain Management**: Reserved domains, custom domains, and SSL certificates
- **Security Policies**: IP restrictions, rate limiting, and comprehensive security controls

### MCP Integration
- **15 Standalone Tools**: Direct ngrok operations with @mcp.tool() decorators
- **4 Complex Orchestration Tools**: Multi-step workflows via NgrokOrchestrator class
- **12 Resource Endpoints**: Static and dynamic data access
- **7 Specialized Prompts**: Development workflow guidance
- **FastMCP Framework**: Full compliance with streamable-http transport

## 📁 Project Structure

```
servers/http/ngrok-http-mcp/
├── src/
│   └── ngrok_server.py          # Main MCP server implementation (2000+ lines)
├── requirements.txt             # Python dependencies
├── .env.example                # Environment configuration template
├── README.md                   # This documentation
└── .gitignore                  # Git ignore patterns
```

## 🔧 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- ngrok account and API key
- Virtual environment (recommended)

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your ngrok credentials
# Required: NGROK_API_KEY, NGROK_AUTHTOKEN
# Optional: NGROK_DEFAULT_REGION, custom domains, etc.
```

### 4. Get ngrok Credentials
1. **API Key**: https://dashboard.ngrok.com/api/keys
2. **Auth Token**: https://dashboard.ngrok.com/get-started/your-authtoken

### 5. Run the Server
```bash
python src/ngrok_server.py
```

The server will start on `http://localhost:8030` by default.

## 🛠️ Tools Overview

### Standalone Tools (15)

#### Core Tunnel Operations
1. **`create_tunnel`** - Create HTTP/HTTPS/TCP tunnels with advanced configuration
2. **`list_tunnels`** - List all active tunnels with filtering options
3. **`stop_tunnel`** - Stop specific tunnels gracefully
4. **`tunnel_traffic`** - Get detailed traffic metrics and analytics
5. **`tunnel_logs`** - Retrieve tunnel activity logs and events
6. **`tunnel_inspect`** - Real-time tunnel inspection and diagnostics

#### Edge & Backend Management
7. **`create_https_edge`** - Create HTTPS edges with custom routing
8. **`create_tcp_edge`** - Create TCP edges for non-HTTP traffic
9. **`create_backend`** - Configure backend services and load balancing
10. **`manage_edge_modules`** - Add/remove edge modules (compression, auth, etc.)
11. **`edge_routes`** - Configure path-based routing rules
12. **`edge_monitoring`** - Comprehensive edge metrics and monitoring

#### Security & Authentication
13. **`manage_credentials`** - Manage authentication credentials and policies
14. **`reserve_domain`** - Reserve custom domains and configure SSL
15. **`ip_policies`** - Configure IP restrictions and geo-blocking

### Complex Orchestration Tools (4)

#### NgrokOrchestrator Class Methods
1. **`full_application_setup`** - Complete application deployment with tunnels, security, and monitoring
2. **`development_environment`** - Set up comprehensive development environment
3. **`load_testing_setup`** - Configure load testing infrastructure with monitoring
4. **`event_stream_analysis`** - Real-time event analysis and alerting

## 📊 Resources (12)

### Static Resources
1. **`ngrok/status`** - Server health and configuration
2. **`ngrok/tunnels`** - All active tunnels overview
3. **`ngrok/edges`** - Edge configurations and status
4. **`ngrok/domains`** - Reserved and custom domains
5. **`ngrok/backends`** - Backend service configurations
6. **`ngrok/credentials`** - Authentication credential status
7. **`ngrok/ip-policies`** - IP restriction policies
8. **`ngrok/api-keys`** - API key management
9. **`ngrok/usage`** - Account usage and billing information
10. **`ngrok/events`** - Recent system events and logs
11. **`ngrok/regions`** - Available ngrok regions and latency

### Dynamic Resources
12. **`tunnels/real-time/{tunnel_id}`** - Live tunnel metrics and traffic data

## 🎯 Prompts (7)

### Development Workflow Prompts
1. **`local_development_prompt`** - Set up local development tunneling
2. **`production_deployment_prompt`** - Configure production-ready deployments
3. **`api_testing_prompt`** - API testing and webhook development
4. **`microservices_prompt`** - Microservices architecture setup
5. **`staging_environment_prompt`** - Staging environment configuration
6. **`ci_cd_integration_prompt`** - CI/CD pipeline integration
7. **`security_configuration_prompt`** - Comprehensive security setup

## 💻 Usage Examples

### Basic Tunnel Creation
```python
# Create a simple HTTP tunnel
result = await create_tunnel(
    name="my-app",
    protocol="http",
    addr="localhost:3000",
    subdomain="my-app-dev"
)
```

### Complex Application Setup
```python
# Full application deployment
result = await orchestrator.full_application_setup(
    app_name="ecommerce-api",
    services={
        "api": {"port": 8000, "protocol": "http"},
        "websocket": {"port": 8001, "protocol": "http"},
        "admin": {"port": 8002, "protocol": "http"}
    },
    domain="api.mycompany.com",
    security_level="production"
)
```

### Real-time Monitoring
```python
# Get live tunnel metrics
metrics = await edge_monitoring(
    edge_id="edghts_1234567890",
    metrics="all",
    time_range="1h"
)
```

## 🔒 Security Features

### Authentication Options
- **OAuth Integration**: Google, GitHub, Microsoft, custom providers
- **Basic Authentication**: Username/password protection
- **API Key Authentication**: Token-based access control
- **IP Restrictions**: Allowlist/denylist by IP or CIDR
- **Geographic Restrictions**: Country-based access control

### Security Policies
- **Rate Limiting**: Request throttling and abuse prevention
- **DDoS Protection**: Automated traffic analysis and blocking
- **SSL/TLS Enforcement**: Certificate management and HTTPS redirection
- **Header Security**: CORS, CSP, and security header injection
- **Request Validation**: Input sanitization and validation rules

## 🌍 Regional Configuration

### Supported Regions
- **US**: `us` (default), `us-cal-1`
- **Europe**: `eu`, `eu-west-1`
- **Asia Pacific**: `ap`, `ap-southeast-1`
- **Australia**: `au`
- **South America**: `sa`
- **India**: `in`
- **Japan**: `jp`

### Configuration Example
```bash
# In .env file
NGROK_DEFAULT_REGION=eu
```

## 🔧 Development

### Testing the Server
```bash
# Test server health
curl http://localhost:8030/health

# Test MCP protocol
curl -X POST http://localhost:8030/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

### Adding New Tools
1. Add new `@mcp.tool()` decorated function
2. Follow existing patterns for error handling
3. Update documentation
4. Test with MCP client

### Custom Orchestration
1. Add method to `NgrokOrchestrator` class
2. Use context integration for logging
3. Implement comprehensive error handling
4. Document workflow steps

## 📈 Monitoring & Analytics

### Built-in Metrics
- **Tunnel Performance**: Response times, throughput, error rates
- **Geographic Distribution**: Request origins and routing
- **Security Events**: Authentication failures, blocked requests
- **Resource Usage**: Bandwidth, connection counts, API quotas

### Integration Options
- **Webhook Notifications**: Real-time event streaming
- **Log Aggregation**: Structured logging with metadata
- **Alert Policies**: Automated alerting for thresholds
- **Dashboard Export**: Metrics export for external dashboards

## 🚨 Troubleshooting

### Common Issues

#### Connection Failures
```bash
# Check ngrok service status
ngrok status

# Verify API credentials
curl -H "Authorization: Bearer $NGROK_API_KEY" \
  https://api.ngrok.com/tunnels
```

#### Authentication Problems
- Verify API key is valid and has correct permissions
- Check authtoken is properly configured
- Ensure account is not suspended or quota exceeded

#### Performance Issues
- Monitor tunnel metrics for bottlenecks
- Check local service health and responsiveness
- Verify network connectivity and DNS resolution

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG_TUNNELS=true
python src/ngrok_server.py
```

## 📚 API Reference

### FastMCP Compliance
This server fully implements the FastMCP framework:
- **Transport**: `streamable-http` for OpenAI Responses API compatibility
- **Tool Patterns**: Both standalone `@mcp.tool()` and class-based tools
- **Resource Management**: Static and dynamic resource endpoints
- **Prompt Integration**: Specialized workflow prompts
- **Error Handling**: Comprehensive error responses and logging

### ngrok API Coverage
- **Tunnels API**: Full CRUD operations and management
- **Edges API**: Complete edge configuration and routing
- **Backends API**: Service discovery and load balancing
- **Credentials API**: Authentication and authorization
- **IP Policies API**: Security and access control
- **Domains API**: Custom domain and SSL management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🔗 Links

- **ngrok Documentation**: https://ngrok.com/docs
- **ngrok Python API**: https://python-api.docs.ngrok.com/
- **FastMCP Framework**: https://github.com/jlowin/fastmcp
- **MCP Specification**: https://spec.modelcontextprotocol.io/

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review ngrok documentation and status page
3. Open an issue in the project repository
4. Contact ngrok support for API-related issues

---

**Note**: This MCP server provides comprehensive ngrok integration for testing, development, and production workflows. It follows FastMCP patterns and provides full compatibility with the Model Context Protocol specification.