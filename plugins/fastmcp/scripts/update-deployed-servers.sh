#!/bin/bash
# Update DEPLOYED_SERVERS.md with last sync timestamp

SERVER_NAME="$1"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

if [ -z "$SERVER_NAME" ]; then
    echo "Usage: ./scripts/update-deployed-servers.sh <server-name>"
    exit 1
fi

# Update last synced timestamp in DEPLOYED_SERVERS.md
case "$SERVER_NAME" in
    "signalhire-mcp")
        sed -i "s/- \*\*Last Synced\*\*:.*/- **Last Synced**: $TIMESTAMP/" DEPLOYED_SERVERS.md
        ;;
    "cats-mcp-server")
        # Find the cats section and update it
        # TODO: Make this more robust
        ;;
esac

echo "✅ Updated DEPLOYED_SERVERS.md for $SERVER_NAME"
