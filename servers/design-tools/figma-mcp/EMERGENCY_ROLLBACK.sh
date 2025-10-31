#!/bin/bash
# Emergency Rollback Script
cd /home/gotime2022/mcp-kernel-new/servers/http
rm -rf figma-mcp
mv figma-mcp-backup-20250717_220115 figma-mcp
echo "✅ Rollback complete - original structure restored"
