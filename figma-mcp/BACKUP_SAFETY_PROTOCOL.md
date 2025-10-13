# Backup Safety Protocol

## ✅ BACKUP CREATED
**Location**: `/home/gotime2022/mcp-kernel-new/servers/http/figma-mcp-backup-20250717_220115`
**Date**: 2025-07-17 22:01:15
**Size**: Complete copy of entire figma-mcp directory

## Safety Measures
1. **Full Directory Backup**: Complete copy created before any changes
2. **Move Operations Only**: Using `mv` commands, not `rm` - no deletion
3. **Staged Approach**: One phase at a time with verification
4. **Rollback Plan**: Can restore entire directory if needed

## Rollback Instructions
If anything goes wrong:
```bash
cd /home/gotime2022/mcp-kernel-new/servers/http
rm -rf figma-mcp
mv figma-mcp-backup-20250717_220115 figma-mcp
```

## Phase-by-Phase Safety
Each phase will:
1. Create directory structure first
2. Move files (not delete)
3. Verify critical files exist
4. Test server startup
5. Only proceed if everything works

## Critical Files to Verify After Each Phase
- `src/figma_server_db.py` (main server file)
- `src/figma_server.py` (HTTP server)
- `config.json` (configuration)
- `requirements.txt` (dependencies)

## Emergency Recovery
If server stops working at any point:
1. Stop reorganization immediately
2. Restore from backup
3. Identify what went wrong
4. Fix and retry

## File Movement Strategy
- Use `mv` commands (atomic operations)
- Move directories in bulk when possible
- Verify file counts before/after
- Check file permissions remain correct

## Test After Each Phase
```bash
cd /home/gotime2022/mcp-kernel-new/servers/http/figma-mcp
python src/figma_server_db.py --test
```

## Backup Verification
Current backup contains:
- All Python files
- All SQL files  
- All JSON files
- All configuration files
- All documentation
- All temporary files

**Ready to proceed safely with reorganization!**