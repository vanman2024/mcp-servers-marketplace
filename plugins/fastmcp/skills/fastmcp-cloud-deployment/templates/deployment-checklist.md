# FastMCP Cloud Deployment Checklist

Use this checklist to ensure a successful deployment. Copy and check off items as you complete them.

## Pre-Deployment Checklist

### Code Quality & Validation

- [ ] All code changes committed to git
- [ ] No uncommitted or untracked files (except .env)
- [ ] Code passes syntax validation (`scripts/validate-server.sh`)
- [ ] No hardcoded secrets or API keys in code
- [ ] Debug mode disabled for production

### Dependencies

- [ ] `requirements.txt` (Python) or `package.json` (TypeScript) up to date
- [ ] All dependencies have pinned versions (using `==` or exact versions)
- [ ] FastMCP dependency included and version specified
- [ ] No development-only dependencies in production requirements

### Configuration Files

- [ ] `fastmcp.json` exists with correct configuration
  - [ ] Server name matches deployment target
  - [ ] Version number updated
  - [ ] Entry point correctly specified
  - [ ] Environment variables documented in `env` array
  - [ ] Health check endpoint configured (if applicable)
- [ ] `.env.example` documents all required environment variables
- [ ] `.gitignore` includes `.env` and `.env.*` (except `.env.example`)

### Environment Variables

- [ ] All required environment variables identified
- [ ] Environment variables documented with descriptions
- [ ] No placeholder values (your-api-key, TODO, etc.)
- [ ] Secrets stored securely (not in code or git)
- [ ] Production environment variables configured in deployment target

### Testing

- [ ] Local testing passed (`scripts/test-local.sh`)
- [ ] STDIO transport tested (if applicable)
- [ ] HTTP transport tested (if applicable)
- [ ] All tools/resources tested manually
- [ ] Error handling verified

### Security

- [ ] No secrets committed to git repository
- [ ] `.env` file not tracked by git
- [ ] CORS configured appropriately for production
- [ ] SSL/TLS certificates valid (for HTTPS deployments)
- [ ] Authentication/authorization implemented (if required)
- [ ] Rate limiting configured (if exposing public endpoints)

## Deployment Checklist

### For FastMCP Cloud Deployment

- [ ] GitHub repository created for server
- [ ] Code pushed to GitHub repository
- [ ] `fastmcp.json` in repository root
- [ ] Connected to FastMCP Cloud dashboard
- [ ] Environment variables set in FastMCP Cloud
- [ ] Deployment triggered
- [ ] Build logs reviewed for errors
- [ ] Deployment status shows "Active"

### For HTTP Deployment (Your Infrastructure)

- [ ] Server infrastructure provisioned (VPS, container, etc.)
- [ ] Dependencies installed on server
- [ ] Environment variables configured on server
- [ ] Server process manager configured (systemd, PM2, Docker, etc.)
- [ ] Firewall rules configured
- [ ] SSL/TLS certificates installed (for HTTPS)
- [ ] Reverse proxy configured (nginx, caddy, etc.)
- [ ] Health check endpoint accessible

### For STDIO Deployment (Local/IDE)

- [ ] Server files in correct location
- [ ] IDE configuration file created (`.mcp.json`, `claude_desktop_config.json`, etc.)
- [ ] Environment variables in `.env` file
- [ ] Server path correctly specified in IDE config
- [ ] IDE restarted to load configuration

## Post-Deployment Verification

### Accessibility Tests

- [ ] Deployment URL is accessible
- [ ] DNS resolution working (for domain deployments)
- [ ] Health endpoint responding (`scripts/verify-deployment.sh`)
- [ ] MCP endpoint responding to JSON-RPC requests
- [ ] SSL/TLS certificate valid (for HTTPS)

### Functional Tests

- [ ] Server returns list of tools via `tools/list` request
- [ ] Sample tool execution succeeds
- [ ] Error handling returns appropriate error messages
- [ ] Authentication working (if configured)
- [ ] Rate limiting enforced (if configured)

### Performance Tests

- [ ] Response time acceptable (< 3 seconds)
- [ ] Server handles multiple concurrent requests
- [ ] Memory usage within expected limits
- [ ] No memory leaks during extended operation

### Monitoring & Logging

- [ ] Logging configured and working
- [ ] Log levels appropriate for environment
- [ ] Error tracking configured (if using Sentry, etc.)
- [ ] Metrics collection working (if configured)
- [ ] Alerts configured for critical failures

## Deployment Tracking

### Record Deployment

- [ ] Update `.fastmcp-deployments.json` with deployment details
- [ ] Record deployment timestamp
- [ ] Record git commit hash
- [ ] Record version number
- [ ] Note any issues encountered

### Documentation

- [ ] README.md updated with deployment URL
- [ ] Environment variables documented
- [ ] Deployment process documented
- [ ] Troubleshooting notes added (if needed)

## Rollback Plan

### Prepare for Issues

- [ ] Previous version deployment details saved
- [ ] Rollback procedure documented
- [ ] Backup of critical data (if applicable)
- [ ] Contact information for support ready

### If Deployment Fails

1. [ ] Review deployment logs for errors
2. [ ] Check environment variables are set correctly
3. [ ] Verify dependencies installed successfully
4. [ ] Test health endpoint manually
5. [ ] Check server logs for runtime errors
6. [ ] If critical: Rollback to previous version
7. [ ] Document issue in deployment tracking
8. [ ] Fix issue locally and redeploy

## Sign-Off

- **Deployed by**: ___________________________
- **Date/Time**: ___________________________
- **Environment**: [ ] Development [ ] Staging [ ] Production
- **Deployment Target**: [ ] STDIO [ ] HTTP [ ] FastMCP Cloud
- **Version**: ___________________________
- **Status**: [ ] Success [ ] Success with warnings [ ] Failed

**Notes**:

---

**Next Steps After Deployment**:
1. Monitor logs for first 24 hours
2. Verify no error spikes
3. Check performance metrics
4. Notify team of successful deployment
5. Update project documentation
