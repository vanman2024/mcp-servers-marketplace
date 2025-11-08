---
description: Verify MCP servers follow proper FastMCP framework structure and conventions
argument-hint: [server-path or "all"]
---

## Security Requirements

**CRITICAL:** All generated files must follow security rules:

@docs/security/SECURITY-RULES.md

**Key requirements:**
- Never hardcode API keys or secrets
- Use placeholders: `your_service_key_here`
- Protect `.env` files with `.gitignore`
- Create `.env.example` with placeholders only
- Document key acquisition for users

**Arguments**: $ARGUMENTS

Goal: Analyze Python-based MCP servers to verify they follow FastMCP framework conventions, identifying non-compliant servers and providing detailed remediation recommendations.

Core Principles:
- Detect actual server structure, don't assume
- Provide actionable remediation steps
- Support both single-server and bulk verification
- Report compliance status clearly

Phase 1: Discovery
Goal: Identify which MCP servers need to be verified

Actions:
- Parse $ARGUMENTS to determine scope:
  - If "all" or empty: Verify all Python servers in marketplace
  - If path provided: Verify specific server
  - If category: Verify all servers in that category
- Use TodoWrite to create task list with identified servers
- List all Python-based MCP servers to verify:
  !{bash find /home/gotime2022/.claude/plugins/marketplaces/mcp-servers/servers -name "server.py" -o -name "*.py" -path "*/src/*" | grep -v venv | grep -v ".venv"}

Phase 2: Initial Analysis
Goal: Quick scan to categorize servers

Actions:
- For each server identified, check:
  - Uses FastMCP framework (imports `from fastmcp import FastMCP`)
  - Has proper server initialization (`mcp = FastMCP(...)`)
  - Has lifespan management (`@asynccontextmanager async def lifespan()`)
  - Uses modern FastMCP 2.x patterns
- Create summary of:
  - Compliant servers
  - Non-compliant servers
  - Servers needing updates
- Update todos with categorization

Phase 3: Detailed Verification
Goal: Run comprehensive FastMCP framework validation

Actions:

Launch the fastmcp-verifier agent to perform deep analysis:

Task(description="Verify FastMCP compliance", subagent_type="fastmcp-verifier", prompt="You are the fastmcp-verifier agent. Analyze the MCP servers identified to verify they follow proper FastMCP framework structure and conventions.

Servers to verify: $ARGUMENTS

For each server, validate:

1. **Framework Import & Initialization**
   - Imports FastMCP from `fastmcp` package
   - Creates server instance: `mcp = FastMCP(name, instructions, version)`
   - Uses proper FastMCP constructor parameters

2. **Lifecycle Management (FastMCP 2.x)**
   - Has `@asynccontextmanager async def lifespan()` function
   - Lifespan contains startup and shutdown logic
   - Server initialization includes `lifespan=lifespan` parameter
   - No deprecated patterns (old-style `with_context` or manual server start)

3. **Tool Definitions**
   - Uses `@mcp.tool` decorator for all tools
   - Proper type hints with `Annotated[type, Field(description=...)]`
   - Includes `Context` parameter for logging/progress
   - Uses `ctx.info()`, `ctx.warning()`, `ctx.report_progress()` appropriately

4. **Resource Definitions**
   - Uses `@mcp.resource(uri)` decorator
   - Proper URI patterns (e.g., `servername://resource/path`)
   - Returns appropriate data structures

5. **Prompt Definitions**
   - Uses `@mcp.prompt` decorator
   - Takes parameters for dynamic prompt generation
   - Returns helpful guidance strings

6. **Server Execution**
   - Has `if __name__ == \"__main__\":` block
   - Calls `mcp.run()` for STDIO mode
   - No custom server runners (unless specifically needed)

7. **Environment & Configuration**
   - Loads `.env` from server directory
   - Uses `load_dotenv()` properly
   - Has proper environment variable handling

8. **Code Quality**
   - Proper async/await usage
   - Type hints throughout
   - Docstrings for tools/resources/prompts
   - Error handling with meaningful messages

For each server analyzed, provide:

**Compliance Report Structure:**
```
Server: [name]
Path: [path]
Status: [COMPLIANT / NEEDS_UPDATES / NON_COMPLIANT]

✅ Passing Checks:
- [List what's correct]

❌ Failing Checks:
- [List violations]

⚠️  Warnings:
- [List concerns]

📝 Remediation Steps:
1. [Step-by-step fixes needed]
2. [Include code examples]
3. [Reference FastMCP docs]

Priority: [HIGH / MEDIUM / LOW]
```

Expected output:
- Comprehensive compliance report for all servers
- Categorized by compliance status
- Prioritized remediation plan
- Example code fixes for common issues
- Summary statistics (X of Y servers compliant)")

Update todos as verification progresses.

Phase 4: Generate Remediation Plan
Goal: Create actionable next steps

Actions:
- Review agent's verification report
- Identify highest priority fixes
- Group fixes by type:
  - Quick wins (simple updates)
  - Medium effort (pattern refactoring)
  - Major rewrites (non-FastMCP servers)
- Create prioritized task list
- Update todos

Phase 5: Summary
Goal: Present verification results and recommendations

Actions:
- Mark all todos complete
- Display comprehensive summary:
  - **Overall Statistics**
    - Total servers analyzed: X
    - Fully compliant: X
    - Need updates: X
    - Non-compliant: X
  - **By Priority**
    - High priority fixes: [list]
    - Medium priority fixes: [list]
    - Low priority improvements: [list]
  - **Quick Wins** (can fix now)
    - [List servers with simple fixes]
  - **Major Updates Needed**
    - [List servers requiring significant work]
  - **Recommended Next Steps**
    1. Fix high priority issues first
    2. Update servers to FastMCP 2.x patterns
    3. Add missing lifecycle management
    4. Improve type hints and documentation

- Offer to:
  - Fix specific servers automatically
  - Generate migration guides for non-compliant servers
  - Create tracking issues for remediation work
