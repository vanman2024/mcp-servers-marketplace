# Enhanced V0 MCP Server - Rollback Plan

## 🚨 Emergency Rollback Procedures

### Immediate Rollback (< 5 minutes)

If the deployment fails during the initial startup or critical issues are detected:

```bash
#\!/bin/bash
# EMERGENCY ROLLBACK SCRIPT

echo "🚨 EMERGENCY ROLLBACK INITIATED"

# 1. Stop current server immediately
echo "Stopping current server..."
pkill -f "vercel_v0_server.py" || true
rm -f /var/run/mcp/v0-enhanced.pid

# 2. Restore backup data
echo "Restoring backup data..."
if [ -d "/var/mcp-data.backup.$(date +%Y%m%d)" ]; then
    rm -rf /var/mcp-data
    cp -r /var/mcp-data.backup.$(date +%Y%m%d) /var/mcp-data
    echo "✓ Data restored from today's backup"
else
    echo "⚠️ No backup found for today, using latest backup"
    latest_backup=$(ls -t /var/mcp-data.backup.* | head -1)
    rm -rf /var/mcp-data
    cp -r "$latest_backup" /var/mcp-data
fi

# 3. Revert to previous version
echo "Reverting to previous version..."
cd /opt/mcp-servers/vercel-v0-enhanced-mcp
git checkout HEAD~1

# 4. Restart with previous version
echo "Starting previous version..."
nohup python src/vercel_v0_server.py > /var/log/mcp/v0-enhanced-rollback.log 2>&1 &
echo $\! > /var/run/mcp/v0-enhanced.pid

# 5. Verify rollback success
sleep 10
if curl -f http://localhost:8015/health > /dev/null 2>&1; then
    echo "✅ ROLLBACK SUCCESSFUL - Server responding"
else
    echo "🚨 ROLLBACK FAILED - Manual intervention required"
    exit 1
fi

echo "✅ Emergency rollback completed successfully"
```

### Gradual Rollback (Issues discovered post-deployment)

For issues discovered after deployment is live and stable:

#### Phase 1: Traffic Diversion (1-2 minutes)
```bash
# Route traffic to backup server
# Update load balancer or reverse proxy configuration
echo "Diverting traffic to backup server..."

# If using nginx
sudo sed -i 's/localhost:8015/localhost:8014/g' /etc/nginx/sites-available/mcp-servers
sudo nginx -s reload
```

#### Phase 2: Investigation (5-15 minutes)
```bash
# Collect diagnostic information
echo "Collecting diagnostics..."
curl http://localhost:8015/health > /tmp/health-check.log
tail -100 /var/log/mcp/v0-enhanced.log > /tmp/server-logs.log
ps aux | grep vercel_v0_server > /tmp/process-info.log

# Test specific functionality
python diagnostic_test.py > /tmp/diagnostic-results.log
```

#### Phase 3: Decision Point
- **If fixable quickly**: Apply hotfix and restore traffic
- **If requires investigation**: Complete rollback

#### Phase 4: Complete Rollback (if needed)
```bash
# Stop problematic version
pkill -f "vercel_v0_server.py"

# Deploy previous stable version
cd /opt/mcp-servers/vercel-v0-enhanced-mcp
git checkout tags/v0.9.0  # Last known stable version

# Start stable version
nohup python src/vercel_v0_server.py > /var/log/mcp/v0-enhanced.log 2>&1 &

# Restore traffic
sudo sed -i 's/localhost:8014/localhost:8015/g' /etc/nginx/sites-available/mcp-servers
sudo nginx -s reload
```

## Rollback Decision Matrix

| Issue Severity | Time to Fix | Action |
|---------------|-------------|--------|
| Critical (Server down) | Any | Immediate rollback |
| High (Errors >10%) | >30 minutes | Immediate rollback |
| High (Errors 5-10%) | <30 minutes | Gradual rollback + hotfix |
| Medium (Performance degraded) | <15 minutes | Monitor + hotfix |
| Low (Minor bugs) | Any | Schedule fix |

## Data Recovery Procedures

### Session Data Recovery
```bash
# Sessions are stored in JSON files - easy to restore
cp /var/mcp-data.backup.*/v0-sessions.json /var/mcp-data/
cp /var/mcp-data.backup.*/v0-projects.json /var/mcp-data/
cp /var/mcp-data.backup.*/v0-deployments.json /var/mcp-data/
```

### Configuration Recovery
```bash
# Restore server configuration
cp /opt/mcp-servers/vercel-v0-enhanced-mcp.backup/deployment-config.json ./
```

## Testing Rollback Procedures

### Pre-Deployment Rollback Test
```bash
# Test rollback procedure before deployment
echo "Testing rollback procedure..."

# Create test backup
cp -r /var/mcp-data /var/mcp-data.test-backup

# Simulate deployment failure
pkill -f "vercel_v0_server.py"

# Execute rollback script
./emergency-rollback.sh

# Verify rollback worked
if curl -f http://localhost:8015/health; then
    echo "✅ Rollback test successful"
else
    echo "🚨 Rollback test failed"
fi

# Cleanup test backup
rm -rf /var/mcp-data.test-backup
```

## Communication Plan

### Rollback Initiated
1. **Immediate**: Slack alert to #devops
2. **5 minutes**: Email to development team
3. **15 minutes**: Status page update if user-facing

### Rollback Completed
1. **Immediate**: All-clear in Slack
2. **30 minutes**: Post-mortem scheduled
3. **1 hour**: Detailed incident report

## Post-Rollback Actions

### ✅ Immediate (0-30 minutes)
- [ ] Verify all services operational
- [ ] Check data integrity
- [ ] Monitor error rates
- [ ] Document rollback reason

### ✅ Short-term (1-4 hours)
- [ ] Investigate root cause
- [ ] Create hotfix if possible
- [ ] Update deployment procedures
- [ ] Notify stakeholders

### ✅ Long-term (1-3 days)
- [ ] Conduct post-mortem
- [ ] Improve testing procedures
- [ ] Update rollback automation
- [ ] Plan next deployment

## Rollback Success Criteria

### ✅ Rollback Successful When:
- [ ] Server responds on port 8015
- [ ] Health check returns 200 OK
- [ ] All 20 MCP tools accessible
- [ ] Session data intact
- [ ] Performance restored to baseline
- [ ] Error rate <1%
- [ ] No data loss detected

## Prevention Measures

### ✅ To Reduce Rollback Need:
- [ ] Comprehensive testing in staging
- [ ] Gradual deployment (canary/blue-green)
- [ ] Automated health checks
- [ ] Performance monitoring
- [ ] Feature flags for new functionality

---

**Last Updated**: July 26, 2025  
**Version**: 1.0  
**Tested**: ☐ Yes ☐ No  
**Approved By**: ________________

EOF < /dev/null
