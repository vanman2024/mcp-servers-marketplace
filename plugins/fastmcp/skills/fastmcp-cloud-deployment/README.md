# FastMCP Cloud Deployment Skill

Production-ready deployment lifecycle management for FastMCP servers.

## Overview

This skill provides comprehensive tools for managing the complete deployment lifecycle of FastMCP MCP servers, from pre-deployment validation through post-deployment verification and troubleshooting.

## Features

### Functional Scripts (4)
- **validate-server.sh** - Pre-deployment validation (syntax, dependencies, config)
- **test-local.sh** - Local testing (STDIO and HTTP transports)
- **check-env-vars.sh** - Environment variable verification
- **verify-deployment.sh** - Post-deployment health checks and verification

### Templates (3)
- **.fastmcp-deployments.json** - Deployment tracking structure
- **deployment-checklist.md** - Step-by-step deployment guide
- **env-var-template.md** - Environment variable documentation template

### Examples (2)
- **successful-deployment.md** - Complete end-to-end deployment workflow
- **troubleshooting.md** - Common issues and solutions

## Quick Start

### Pre-Deployment

```bash
cd /path/to/your/server

# Validate server is ready
./scripts/validate-server.sh .

# Check environment variables
./scripts/check-env-vars.sh .

# Test locally
TRANSPORT=both ./scripts/test-local.sh .
```

### Post-Deployment

```bash
# Verify deployment is working
./scripts/verify-deployment.sh https://your-server.fastmcp.app/mcp
```

## Use Cases

This skill is automatically loaded by Claude when you:
- Deploy MCP servers to FastMCP Cloud
- Validate server configurations before deployment
- Test server functionality locally
- Verify deployment health and accessibility
- Troubleshoot deployment issues
- Track deployment history

## Deployment Lifecycle

1. **Pre-Deployment Validation** - Ensure code quality and configuration
2. **Local Testing** - Verify functionality before deploying
3. **Environment Verification** - Validate all required variables set
4. **Deployment** - Deploy to FastMCP Cloud, HTTP, or STDIO
5. **Post-Deployment Verification** - Confirm deployment is working correctly

## Script Documentation

See [scripts/README.md](scripts/README.md) for detailed documentation of all scripts including usage examples, environment variables, and exit codes.

## Examples

### Complete Workflow
See [examples/successful-deployment.md](examples/successful-deployment.md) for a complete end-to-end deployment example with real script output and best practices.

### Troubleshooting
See [examples/troubleshooting.md](examples/troubleshooting.md) for common issues and their solutions organized by deployment phase.

## Templates

### Deployment Tracking
Copy [templates/.fastmcp-deployments.json](templates/.fastmcp-deployments.json) to track all your deployments with metadata, validation results, and environment variables.

### Deployment Checklist
Use [templates/deployment-checklist.md](templates/deployment-checklist.md) as a comprehensive checklist for each deployment to ensure nothing is missed.

### Environment Variables
Use [templates/env-var-template.md](templates/env-var-template.md) as a template for documenting all environment variables in your server.

## Integration

This skill integrates with:
- **FastMCP deployment agent** - Primary consumer of deployment lifecycle tools
- **mcp-server-config skill** - Uses configuration templates
- **newman-runner skill** - Can integrate API testing before deployment

## Dependencies

Scripts require standard Unix tools:
- bash
- curl
- jq (optional but recommended)
- python3 or tsx (depending on server language)

See [scripts/README.md](scripts/README.md) for complete dependency information.

## Validation Status

All scripts are:
- ✅ Executable with proper permissions
- ✅ Error handling and clear output
- ✅ Configurable via environment variables
- ✅ Tested and production-ready

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for complete validation details.

## Support

For issues or questions:
1. Check [examples/troubleshooting.md](examples/troubleshooting.md)
2. Review script output for specific error messages
3. Consult [scripts/README.md](scripts/README.md) for usage details
4. Refer to FastMCP documentation: https://gofastmcp.com/docs

## Version

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-15

---

**Part of the FastMCP Plugin Ecosystem**
