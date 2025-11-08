---
description: Create complete FastMCP server with all features - orchestrates setup, components, auth, deployment, verification, and testing
argument-hint: <server-name> [--language=python|typescript] [--purpose="description"] [--collection=path] [--auth=type] [--deployment=type] [--skip-questions]
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

## Command Purpose

`/fastmcp:new-server` is the MAIN ORCHESTRATOR for building complete FastMCP servers.

It chains multiple slash commands sequentially to build a production-ready server:
1. Creates base server structure (Python or TypeScript)
2. Adds API wrapper tools (if Postman collection provided)
3. Adds additional components (if specified)
4. Configures authentication (if specified)
5. Sets up deployment (if specified)
6. Verifies server structure and compliance
7. Generates and runs comprehensive tests
8. Provides complete summary and next steps

**This command ORCHESTRATES other commands - it does NOT invoke agents directly!**

## Phase 1: Parse Arguments and Gather Requirements

**Parse $ARGUMENTS to extract:**
- `server-name` - First positional argument
- `--language=python|typescript` - Language choice
- `--purpose="description"` - Server purpose
- `--collection=/path/to/collection.json` - Optional Postman collection
- `--auth=oauth|jwt|bearer` - Optional authentication type
- `--deployment=stdio|http|cloud` - Optional deployment type
- `--skip-questions` - Skip interactive questions

**If `--skip-questions` provided OR all parameters present:**
- Skip to Phase 2 immediately
- Use provided parameters

**If parameters missing:**
- Use TodoWrite to track requirements gathering
- Ask interactive questions:
  - Language: "Which language: Python or TypeScript?"
  - Purpose: "What will this MCP server do?"
  - Components: "What features do you need? (tools, resources, prompts)"
  - Authentication: "Do you need authentication? (OAuth, JWT, Bearer, none)"
  - Deployment: "Where will you deploy? (STDIO/local, HTTP/remote, FastMCP Cloud)"

**Update TodoWrite with detected/gathered parameters**

## Phase 2: Create Base Server Structure

**Action: Invoke new-server-base setup agent**

**For Python servers:**

Use Task tool NOW to invoke the fastmcp-setup agent:

```
Task(
  subagent_type="fastmcp:fastmcp-setup",
  description="Create Python FastMCP server structure",
  prompt="Create FastMCP Python server with these requirements:

**Project name:** {server-name}
**Purpose:** {purpose from Phase 1}
**Location:** {current-directory}/{server-name}

Create complete Python FastMCP server with:
- Project directory structure
- pyproject.toml with fastmcp dependency
- server.py with FastMCP initialization
- .env.example with placeholders
- .gitignore for Python projects
- README.md with setup instructions

Follow FastMCP SDK best practices. Generate functional starter code, not placeholders."
)
```

**For TypeScript servers:**

Use Task tool NOW to invoke the fastmcp-setup-ts agent:

```
Task(
  subagent_type="fastmcp:fastmcp-setup-ts",
  description="Create TypeScript FastMCP server structure",
  prompt="Create FastMCP TypeScript server with these requirements:

**Project name:** {server-name}
**Purpose:** {purpose from Phase 1}
**Location:** {current-directory}/{server-name}

Create complete TypeScript FastMCP server with:
- Project directory structure
- package.json with fastmcp dependency
- tsconfig.json with proper configuration
- src/server.ts with FastMCP initialization
- .env.example with placeholders
- .gitignore for Node.js/TypeScript
- README.md with setup instructions

Follow FastMCP SDK best practices. Generate functional starter code, not placeholders."
)
```

**WAIT for agent completion.**

**After completion:**
- Verify server directory was created
- Confirm server files exist
- Update TodoWrite: mark "Create base server" as completed
- Capture server path for next phases

**If agent failed:**
- Report error to user
- STOP workflow - do not proceed to Phase 3

## Phase 3: Add API Wrapper Tools (if --collection provided)

**Check if `--collection` parameter was provided in Phase 1.**

**If YES:**

Use SlashCommand tool NOW to invoke add-api-wrapper command:

```
SlashCommand(command="/fastmcp:add-api-wrapper {server-name} --collection={collection-path}")
```

**WAIT for command completion.**

**After completion:**
- Verify tools were generated
- Update TodoWrite: mark "Add API wrapper tools" as completed

**If NO collection provided:**
- Skip to Phase 4

## Phase 4: Add Additional Components (if needed)

**Check if additional components needed beyond API wrapper.**

Common scenarios:
- User wants custom tools beyond API wrapper
- User wants resources for data access
- User wants prompts for LLM interactions

**If additional components needed:**

Use SlashCommand tool NOW:

```
SlashCommand(command="/fastmcp:add-components {component-types} --server-path={detected-path}")
```

Where `{component-types}` might be: `tools`, `resources`, `prompts`, or combinations.

**WAIT for command completion.**

**After completion:**
- Update TodoWrite: mark "Add components" as completed

**If no additional components needed:**
- Skip to Phase 5

## Phase 5: Configure Authentication (if --auth provided)

**Check if `--auth` parameter was provided in Phase 1.**

**If YES:**

Use SlashCommand tool NOW:

```
SlashCommand(command="/fastmcp:add-auth {auth-type} --server-path={detected-path}")
```

Where `{auth-type}` is: `oauth`, `jwt`, or `bearer`

**WAIT for command completion.**

**After completion:**
- Verify authentication was configured
- Update TodoWrite: mark "Configure authentication" as completed

**If NO auth specified:**
- Skip to Phase 6

## Phase 6: Set Up Deployment (if --deployment provided)

**Check if `--deployment` parameter was provided in Phase 1.**

**If YES:**

Use SlashCommand tool NOW:

```
SlashCommand(command="/fastmcp:add-deployment {deployment-type} --server-path={detected-path}")
```

Where `{deployment-type}` is: `stdio`, `http`, or `cloud`

**WAIT for command completion.**

**After completion:**
- Verify deployment configuration created
- Update TodoWrite: mark "Set up deployment" as completed

**If NO deployment specified:**
- Default to STDIO (already in base server)
- Skip to Phase 7

## Phase 7: Verify Server Structure

**Action: Verify server compliance**

Use SlashCommand tool NOW:

```
SlashCommand(command="/fastmcp:fastmcp-verify {detected-path}")
```

**WAIT for command completion.**

**After completion:**
- Review verification report
- Check for compliance issues
- Update TodoWrite: mark "Verify server" as completed

**If verification found critical issues:**
- Report issues to user
- Suggest fixes
- Allow user to decide whether to continue

## Phase 8: Generate and Run Tests

**Action: Create comprehensive test suite**

Use SlashCommand tool NOW:

```
SlashCommand(command="/fastmcp:test --server-path={detected-path} --run --coverage")
```

**WAIT for command completion.**

**After completion:**
- Review test results
- Check test coverage
- Update TodoWrite: mark "Run tests" as completed

**If tests failed:**
- Report failures to user
- Suggest fixes
- Server is created but may need adjustments

## Phase 9: Complete Summary

**Display comprehensive summary:**

```
✅ FastMCP Server Created Successfully!

**Server Details:**
- Name: {server-name}
- Language: {Python|TypeScript}
- Location: {full-path}
- Purpose: {purpose}

**Components Added:**
- Base server structure ✓
- API wrapper tools (if applicable) ✓
- Additional components (if applicable) ✓
- Authentication (if applicable) ✓
- Deployment configuration (if applicable) ✓

**Verification:**
- Structure validation: {PASSED|FAILED}
- Test results: {PASSED|FAILED}
- Test coverage: {percentage}%

**Next Steps:**
1. Navigate to server: cd {server-name}
2. Review and customize server.py (or src/server.ts)
3. Run server locally: {command based on language}
4. Test with MCP client
5. Deploy to {deployment-target}

**Documentation:**
- FastMCP Docs: https://gofastmcp.com
- Server README: {server-name}/README.md
```

**Update TodoWrite: mark all tasks completed**

## Error Handling

At each phase, if a command or agent fails:
1. Report the specific error to user
2. Explain what went wrong
3. Suggest remediation steps
4. Ask if they want to:
   - Retry the failed step
   - Skip the step and continue
   - Abort the workflow

Do NOT silently continue past errors.

## Command Execution Rules

**CRITICAL:**
- Use SlashCommand tool for invoking commands
- Use Task tool for invoking agents
- WAIT for each step to complete before proceeding
- Do NOT run commands in parallel
- Do NOT describe what "will happen" - actually INVOKE the tools
- Update TodoWrite after each phase

This ensures the orchestration actually executes, not just describes the workflow.
