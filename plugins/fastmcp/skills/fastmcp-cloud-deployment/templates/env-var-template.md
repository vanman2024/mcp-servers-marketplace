# Environment Variables Documentation

## Overview

This document describes all environment variables used by the FastMCP server. Keep this file updated as you add new environment variables.

## Required Variables

These variables MUST be set for the server to function.

### DATABASE_URL
- **Type**: String (URL)
- **Description**: Connection string for the database
- **Format**: `postgresql://user:password@host:port/database` or `sqlite:///path/to/db.sqlite`
- **Example**: `postgresql://admin:secret@localhost:5432/myapp`
- **Security**: Contains credentials - never commit to git

### API_KEY
- **Type**: String
- **Description**: API key for authenticating with external service
- **Format**: Alphanumeric string (32-64 characters)
- **Example**: `sk_live_1234567890abcdef1234567890abcdef`
- **Security**: Sensitive - store in secrets manager

## Optional Variables

These variables have defaults but can be customized.

### LOG_LEVEL
- **Type**: String (enum)
- **Description**: Logging verbosity level
- **Format**: One of: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`
- **Example**: `DEBUG`
- **Notes**: Use `DEBUG` for development, `INFO` or `WARNING` for production

### PORT
- **Type**: Integer
- **Description**: Port number for HTTP server
- **Format**: 1-65535
- **Default**: `8000`
- **Example**: `3000`
- **Notes**: Only relevant for HTTP transport mode

### MAX_RETRIES
- **Type**: Integer
- **Description**: Maximum number of retry attempts for failed operations
- **Format**: Non-negative integer
- **Default**: `3`
- **Example**: `5`

### TIMEOUT
- **Type**: Integer
- **Description**: Request timeout in seconds
- **Format**: Positive integer
- **Default**: `30`
- **Example**: `60`

### ENABLE_MONITORING
- **Type**: Boolean
- **Description**: Enable Prometheus metrics endpoint
- **Format**: `true` or `false`
- **Default**: `false`
- **Example**: `true`
- **Notes**: Exposes `/metrics` endpoint when enabled

### CORS_ORIGINS
- **Type**: String (comma-separated URLs)
- **Description**: Allowed origins for CORS
- **Format**: Comma-separated list of URLs
- **Default**: `*` (allow all)
- **Example**: `https://app.example.com,https://staging.example.com`
- **Notes**: Restrict in production for security

## Development-Only Variables

These variables are only used in development environments.

### DEBUG
- **Type**: Boolean
- **Description**: Enable debug mode with detailed error messages
- **Format**: `true` or `false`
- **Default**: `false`
- **Example**: `true`
- **Notes**: NEVER enable in production - exposes sensitive information

### MOCK_EXTERNAL_API
- **Type**: Boolean
- **Description**: Use mock responses instead of calling external APIs
- **Format**: `true` or `false`
- **Default**: `false`
- **Example**: `true`
- **Notes**: Useful for testing without API credits

## Environment-Specific Configurations

### Development (.env.development)
```bash
LOG_LEVEL=DEBUG
DEBUG=true
MOCK_EXTERNAL_API=true
PORT=8000
CORS_ORIGINS=*
```

### Staging (.env.staging)
```bash
LOG_LEVEL=INFO
DEBUG=false
MOCK_EXTERNAL_API=false
PORT=8000
CORS_ORIGINS=https://staging.example.com
ENABLE_MONITORING=true
```

### Production (.env.production)
```bash
LOG_LEVEL=WARNING
DEBUG=false
MOCK_EXTERNAL_API=false
PORT=8000
CORS_ORIGINS=https://app.example.com
ENABLE_MONITORING=true
MAX_RETRIES=5
TIMEOUT=60
```

## Setting Environment Variables

### Local Development (.env file)
```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

### FastMCP Cloud
```bash
# Set via FastMCP Cloud dashboard
# Settings > Environment Variables > Add Variable

# Or via CLI (if available)
fastmcp env set DATABASE_URL "postgresql://..."
fastmcp env set API_KEY "sk_live_..."
```

### Docker
```bash
# Via docker-compose.yml
environment:
  - DATABASE_URL=postgresql://...
  - API_KEY=sk_live_...

# Or via .env file loaded by docker-compose
docker-compose --env-file .env.production up
```

### Systemd Service
```ini
# /etc/systemd/system/myserver.service
[Service]
Environment="DATABASE_URL=postgresql://..."
Environment="API_KEY=sk_live_..."
Environment="LOG_LEVEL=INFO"
```

## Validation

Run the environment variable checker before deployment:

```bash
# Check current environment
./scripts/check-env-vars.sh

# Check specific env file
ENV_FILE=.env.production ./scripts/check-env-vars.sh
```

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use `.env.example`** - Document variables without values
3. **Rotate secrets regularly** - Especially after team member departures
4. **Use different values per environment** - Never reuse production secrets in dev
5. **Restrict access** - Only give access to necessary team members
6. **Use secrets managers** - For production (AWS Secrets Manager, HashiCorp Vault, etc.)
7. **Monitor for leaks** - Use git hooks to prevent accidental commits

## Troubleshooting

### Variable Not Set Error
```
Error: Required environment variable DATABASE_URL not set
```

**Solution**: Add the variable to your `.env` file or environment

### Invalid Variable Format
```
Error: DATABASE_URL must be a valid URL
```

**Solution**: Check the format matches the expected pattern (see variable documentation above)

### Variable Ignored
If a variable seems to have no effect:
1. Check spelling matches exactly (case-sensitive)
2. Ensure `.env` file is in the correct location
3. Restart the server after changing `.env`
4. Check if variable is loaded: `echo $VARIABLE_NAME`

## Checklist

Before deployment, verify:
- [ ] All required variables documented in this file
- [ ] All variables in `.env.example` have descriptions
- [ ] No secrets in `.env.example` (use placeholders)
- [ ] `.env` in `.gitignore`
- [ ] Production values different from development
- [ ] Sensitive variables stored in secrets manager
- [ ] Environment checker passes: `./scripts/check-env-vars.sh`

---

**Last Updated**: YYYY-MM-DD
**Maintainer**: Your Name <your.email@example.com>
