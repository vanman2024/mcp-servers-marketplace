# Figma MCP Server Deployment Guide

## Quick Start

1. **Validate Configuration**
   ```bash
   cd servers/http/figma-mcp
   python validate_config.py
   ```

2. **Fix Any Issues**
   - If Figma token is missing: Get one from https://www.figma.com/developers/access-tokens
   - If Supabase is not configured: Set up your Supabase project

3. **Start the Server**
   ```bash
   ./start.sh
   ```

## Deployment Steps

### 1. Environment Setup

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Figma API Token (get from https://www.figma.com/developers/access-tokens)
FIGMA_PAT=figd_YOUR_ACTUAL_TOKEN_HERE

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here

# Optional
PORT=8031
FIGMA_DEBUG=false
```

### 2. Database Setup (First Time Only)

If using Supabase for component storage:

1. Go to your Supabase dashboard
2. Navigate to SQL Editor
3. Create a new query
4. Paste the contents of `migrations/001_initial_schema.sql`
5. Run the query

### 3. Dependencies Installation

The start script automatically installs dependencies, but you can do it manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Validation

Always validate before starting:
```bash
python validate_config.py
```

Expected output:
```
✓ FIGMA_PAT found
✓ Token format looks correct
✓ Figma API connection successful!
✓ Supabase connection successful!
```

### 5. Running the Server

#### Development Mode
```bash
./start.sh
```

#### Production Mode with PM2
```bash
pm2 start ecosystem.config.js
```

#### Docker Deployment
```bash
docker build -t figma-mcp-server .
docker run -p 8031:8031 --env-file .env figma-mcp-server
```

### 6. Health Check

Verify the server is running:
```bash
curl http://localhost:8031/health
```

## Troubleshooting

### Common Issues

1. **"Figma authentication token not found!"**
   - Set `FIGMA_PAT` or `FIGMA_ACCESS_TOKEN` environment variable
   - Use `.env` file or export directly

2. **"Invalid or expired token"**
   - Regenerate token at https://www.figma.com/developers/access-tokens
   - Ensure token has "File content" scope

3. **"Tables not found - please run database migrations"**
   - Run the migration script in Supabase SQL Editor
   - Check SUPABASE_URL and SUPABASE_SERVICE_KEY are correct

4. **Port already in use**
   - Change PORT in `.env` to a different value
   - Or kill the existing process: `lsof -i :8031 | grep LISTEN`

### Debug Mode

Enable detailed logging:
```bash
export FIGMA_DEBUG=true
./start.sh
```

## Integration with Claude Desktop

Add to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "figma": {
      "command": "python",
      "args": [
        "/path/to/figma-mcp/src/figma_server.py"
      ],
      "env": {
        "FIGMA_PAT": "your-token-here",
        "SUPABASE_URL": "your-supabase-url",
        "SUPABASE_SERVICE_KEY": "your-service-key"
      }
    }
  }
}
```

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Limit token permissions** to only what's needed
5. **Use HTTPS** in production environments

## Monitoring

### Logs
- Server logs: Check console output or redirect to file
- Enable debug mode for detailed logging
- Use PM2 for log management in production

### Metrics
- Monitor `/health` endpoint
- Track API rate limits
- Watch for authentication failures

## Updates

To update the server:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
./start.sh
```

## Support

- Check `README.md` for detailed documentation
- Run `python validate_config.py` for configuration issues
- Enable debug mode for troubleshooting
- Create an issue on GitHub for bugs