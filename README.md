## MCP Servers

A collection of Model Context Protocol (MCP) servers and related utilities. This monorepo groups multiple HTTP-based MCP servers (Python and Node.js) for services like Supabase, GitHub, DigitalOcean, Figma, Vercel, and more.

### Structure
- Each folder contains a standalone MCP server or example.
- Many Python servers use `requirements.txt` or `pyproject.toml`.
- Some JavaScript/TypeScript examples include a `package.json`.
- Environment examples live as `.env.example` files; real `.env` files are ignored.

### Getting Started
- Consult each server’s README or `.env.example` for configuration.
- Create local `.env` files as needed (not committed).
- Install dependencies per server (Python `pip`/`uv`/`poetry`, Node `npm`/`pnpm`/`yarn`).

### Contributing
- Keep secrets in `.env` files and never commit them.
- Prefer small, focused changes per server.

### License
- Add a license if you plan to open source.

