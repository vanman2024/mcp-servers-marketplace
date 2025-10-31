# SignalHire MCP Server (Standalone)

**FastMCP server for SignalHire API** - Completely standalone with 13 tools, 7 resources, and 8 prompts for contact enrichment and lead generation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /home/gotime2022/Projects/Mcp-Servers/signalhire
pip install -r requirements.txt
```

Or use the automated installer:

```bash
chmod +x install.sh
./install.sh
```

### 2. Configure Environment (Self-Contained)

The server automatically loads `.env` from its own directory:

```bash
# Copy the example file
cp .env.example .env

# Edit with your API key
nano .env
```

Add your SignalHire API key and callback server URL in the `.env` file:

```bash
# Your SignalHire API key
SIGNALHIRE_API_KEY=your_actual_api_key_here

# Your external callback server (e.g., DigitalOcean)
EXTERNAL_CALLBACK_URL=https://your-callback-server.com/signalhire/callback
```

**That's it!** The server is completely self-contained - no global environment variables needed.

**Using an external callback server?** See [EXTERNAL_CALLBACK_SETUP.md](EXTERNAL_CALLBACK_SETUP.md) for detailed configuration.

### 3. Run the Server

```bash
python server.py
```

You should see:
```
✅ SignalHire MCP Server started successfully
📡 Webhook callback URL: http://localhost:8000/signalhire/callback
```

### 4. Install in Claude Code

The `.mcp.json` is already configured for self-contained operation:

```bash
cd /home/gotime2022/Projects/Mcp-Servers/signalhire
fastmcp install claude-code .mcp.json
```

**No environment variables to configure!** The server loads its `.env` file automatically.

Restart Claude Code and the server will be ready to use.

## 📦 What's Included

### 13 MCP Tools

**Core API (5)**:
1. `search_prospects` - Search 900M+ profiles
2. `reveal_contact` - Get contact info for profile
3. `batch_reveal_contacts` - Bulk enrichment
4. `check_credits` - View remaining credits
5. `scroll_search_results` - Paginate search results

**Workflows (5)**:
6. `search_and_enrich` - Combined search + enrichment
7. `enrich_linkedin_profile` - Single profile enrichment
8. `validate_email` - Email validation
9. `export_results` - Export to CSV/JSON/Excel
10. `get_search_suggestions` - Query suggestions

**Management (3)**:
11. `get_request_status` - Check request status
12. `list_requests` - View request history
13. `clear_cache` - Clear local cache

### 7 MCP Resources

1. `signalhire://contacts/{uid}` - Get cached contact
2. `signalhire://cache/stats` - Cache statistics
3. `signalhire://recent-searches` - Recent searches
4. `signalhire://credits` - Current credits
5. `signalhire://rate-limits` - Rate limit status
6. `signalhire://requests/history` - Request history
7. `signalhire://account` - Account info

### 8 MCP Prompts

1. `enrich-linkedin-profile` - Profile enrichment guide
2. `bulk-enrich-contacts` - Bulk enrichment guide
3. `search-candidates-by-criteria` - Search guide
4. `search-and-enrich-workflow` - Complete workflow
5. `manage-credits` - Credit management
6. `validate-bulk-emails` - Email validation
7. `export-search-results` - Export guide
8. `troubleshoot-webhook` - Webhook debugging

## 🏗️ Architecture

**Standalone Design** - All code self-contained:

```
signalhire/
├── server.py              # Main MCP server (837 lines)
├── lib/                   # Core functionality (14 files, ~3000 lines)
│   ├── signalhire_client.py  # API client (57 KB)
│   ├── callback_server.py    # FastAPI webhook server (11 KB)
│   ├── contact_cache.py      # Local caching
│   ├── config.py             # Configuration management
│   └── ... (10 more files)
├── models/                # Pydantic models (9 files, ~1500 lines)
│   ├── person_callback.py
│   ├── operations.py
│   └── ... (7 more files)
├── storage/               # Storage adapters (3 files, ~600 lines)
│   ├── mem0_adapter.py
│   └── supabase_adapter.py
├── requirements.txt       # All dependencies
├── .mcp.json             # MCP configuration
└── README.md             # This file
```

**Total:** ~7,000 lines of production-ready code, all consolidated!

### Why Standalone & Self-Contained?

✅ **No external dependencies** - No `signalhireagent` package needed
✅ **Self-contained configuration** - `.env` file in server directory, no global env vars
✅ **FastMCP Cloud ready** - Single directory deployment with config included
✅ **Easy maintenance** - All code and config in one place
✅ **Simple deployment** - Just push to GitHub and deploy
✅ **Portable** - Copy the directory anywhere, it just works

## 📝 Usage Examples

### In Claude Code

```
User: "Search SignalHire for 25 Python engineers in San Francisco"
Claude: *calls search_prospects tool*
Claude: "Found 1,234 matching profiles. Here are the first 25..."

User: "Enrich them all"
Claude: *calls batch_reveal_contacts*
Claude: "Enrichment started. Request ID: abc123"
```

### With FastMCP CLI

```bash
# Run with inspector
fastmcp dev server.py

# Run in HTTP mode
fastmcp run server.py --transport http --port 8000
```

## 🚢 Deployment

### Local Development

```bash
# Run from this directory
python server.py
```

### FastMCP Cloud Deployment

**Self-contained deployment - your `.env` file is included!**

1. **Prepare for deployment:**
   ```bash
   cd /home/gotime2022/Projects/Mcp-Servers/signalhire

   # Make sure .env exists with your API key
   cp .env.example .env
   nano .env  # Add your SIGNALHIRE_API_KEY

   # Initialize git if not already done
   git init
   git add .
   git commit -m "Initial SignalHire MCP server"
   git push origin main
   ```

2. **Deploy to FastMCP Cloud:**
   - Go to https://fastmcp.cloud
   - Connect your GitHub repository
   - **No environment variables needed!** (`.env` file is included)
   - Deploy!

3. **Use the hosted URL:**
   ```json
   {
     "mcpServers": {
       "signalhire": {
         "url": "https://your-server.fastmcp.cloud"
       }
     }
   }
   ```

**Note:** Make sure your `.env` file is committed to your repo (it's safe since it's in your private repo). If you prefer, you can still use FastMCP Cloud's environment variables feature instead.

### HTTP Mode (for remote access)

```bash
fastmcp run server.py --transport http --port 8000
```

Access at: `http://localhost:8000/mcp`

### Docker Deployment

```bash
# Build image
docker build -t signalhire-mcp .

# Run container
docker run -p 8000:8000 --env-file .env signalhire-mcp
```

## 🐛 Troubleshooting

### "Module not found" errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### "Webhook not receiving callbacks"

Check callback server:
```bash
curl http://localhost:8000/health
```

If behind firewall, use ngrok:
```bash
ngrok http 8000
```

### Server won't start

1. Check Python version (need >= 3.10):
   ```bash
   python3 --version
   ```

2. Test syntax:
   ```bash
   python3 -m py_compile server.py
   ```

3. Check environment variables:
   ```bash
   cat .env
   ```

## 📚 Documentation

- **SignalHire API Docs**: https://www.signalhire.com/api-docs
- **FastMCP Docs**: https://gofastmcp.com
- **FastMCP Cloud**: https://fastmcp.cloud

## 🔗 API Limits

- **Rate Limit**: 600 items/minute
- **Search Concurrency**: 3 concurrent requests max
- **ScrollId Expiry**: 15 seconds
- **Daily Limit**: 5,000 reveals/day
- **Search Profile Limit**: 5,000 profiles/day

## 💡 Best Practices

1. **Use batch operations** for multiple contacts (more efficient)
2. **Cache results** to avoid redundant API calls
3. **Monitor credits** before large operations
4. **Use semantic search** (Mem0) for natural language queries
5. **Export results** regularly for backup

## 📄 License

Same license as signalhireagent project.

---

**Built with [FastMCP](https://gofastmcp.com) - The fastest way to build MCP servers in Python**

**Architecture**: Standalone (no external packages)
**Status**: Production-ready
**FastMCP Cloud**: ✅ Ready for deployment
