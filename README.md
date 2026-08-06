# postgres-mcp

MCP server Postgres dengan guard destruktif:

- `query` — read-only (SELECT/EXPLAIN), dijalankan dalam transaksi `READ ONLY`.
- `execute` — INSERT/UPDATE/DELETE wajib `confirm=true`; client harus minta persetujuan user dulu.
- `TRUNCATE`, `DROP DATABASE/TABLE/SCHEMA`, `ALTER TABLE ... DROP` diblokir permanen, tidak bisa di-confirm.

## Prasyarat

- [uv](https://docs.astral.sh/uv/) terinstall (dependency di-resolve otomatis saat run).
- Env `DATABASE_URL`, contoh: `postgresql://user:pass@localhost:5432/db`

Perintah dasar untuk menjalankan server (dipakai semua client di bawah):

```bash
uv run --no-project --with "mcp[cli]",psycopg python /path/to/postgres-mcp/server.py
```

Ganti `/path/to/postgres-mcp` dengan lokasi clone kamu.

## Claude Code

```bash
claude mcp add postgres --env DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  -- uv run --no-project --with "mcp[cli]",psycopg python /path/to/postgres-mcp/server.py
```

Atau lewat `.mcp.json` di root project:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uv",
      "args": ["run", "--no-project", "--with", "mcp[cli],psycopg", "python", "/path/to/postgres-mcp/server.py"],
      "env": { "DATABASE_URL": "postgresql://user:pass@localhost:5432/db" }
    }
  }
}
```

## Codex CLI

Tambahkan ke `~/.codex/config.toml`:

```toml
[mcp_servers.postgres]
command = "uv"
args = ["run", "--no-project", "--with", "mcp[cli],psycopg", "python", "/path/to/postgres-mcp/server.py"]

[mcp_servers.postgres.env]
DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
```

Atau via CLI:

```bash
codex mcp add postgres --env DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  -- uv run --no-project --with "mcp[cli],psycopg" python /path/to/postgres-mcp/server.py
```

## OpenCode

Tambahkan ke `opencode.json` (project) atau `~/.config/opencode/opencode.json` (global):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "postgres": {
      "type": "local",
      "command": ["uv", "run", "--no-project", "--with", "mcp[cli],psycopg", "python", "/path/to/postgres-mcp/server.py"],
      "environment": { "DATABASE_URL": "postgresql://user:pass@localhost:5432/db" },
      "enabled": true
    }
  }
}
```

## Kilo Code

Buka **MCP Servers → Edit MCP Settings** (global: `mcp_settings.json`, atau per-project: `.kilocode/mcp.json`):

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uv",
      "args": ["run", "--no-project", "--with", "mcp[cli],psycopg", "python", "/path/to/postgres-mcp/server.py"],
      "env": { "DATABASE_URL": "postgresql://user:pass@localhost:5432/db" }
    }
  }
}
```

## Test

```bash
uv run --no-project --with "mcp[cli]",psycopg python test_guard.py
```
