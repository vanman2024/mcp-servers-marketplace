# MCP Servers Marketplace - Claude Code Configuration

## 🚨 CRITICAL: Security Rules - NO HARDCODED API KEYS

**This is the HIGHEST PRIORITY security rule for ALL plugins in this marketplace.**

### Absolute Prohibition

❌ **NEVER EVER** hardcode API keys, secrets, or credentials in:
- Agent prompts
- Command prompts
- Skill documentation
- Example code
- MCP server implementations
- Scripts or configuration

### Required Practice

✅ **ALWAYS use placeholders:**
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
FASTMCP_API_KEY=your_fastmcp_key_here
```

✅ **ALWAYS read from environment:**
```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

### Comprehensive Security Guidelines

See `@docs/security/SECURITY-RULES.md` for full validation checklist and comprehensive security guidelines.

**Before ANY commit to this marketplace:**
- [ ] No real API keys in any file
- [ ] All examples use obvious placeholders
- [ ] `.gitignore` protects secrets
- [ ] Setup docs explain key acquisition

**Violations = Immediate fix required before merge**

---

## MCP Server Development Guidelines

This marketplace contains plugins for building and deploying FastMCP servers.

### Plugin Structure

All MCP server plugins follow the FastMCP framework conventions and integrate with Claude Code's plugin system.

### Component Types

- **Agents**: Specialized for FastMCP server setup, deployment, testing, verification
- **Commands**: User-facing commands for creating, configuring, and managing MCP servers
- **Skills**: Reusable patterns and templates for MCP development

### Reference

For complete FastMCP documentation and patterns, see plugin-specific documentation.
