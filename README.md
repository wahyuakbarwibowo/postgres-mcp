# postgres-mcp

MCP server minimal untuk mengakses PostgreSQL dari client MCP dengan guard
untuk operasi yang berisiko.

## Fitur

- `query` menjalankan SQL dalam transaksi `READ ONLY` dan mengembalikan maksimal
  500 baris.
- `execute` memerlukan `confirm=true` sebelum menjalankan perubahan data.
- `TRUNCATE`, `DROP DATABASE/TABLE/SCHEMA`, dan `ALTER TABLE ... DROP` selalu
  diblokir dan tidak dapat di-confirm.
- Query dan transaksi memiliki timeout untuk mencegah koneksi macet.

`query` bergantung pada PostgreSQL untuk menolak operasi tulis karena transaksi
read-only. Client tetap perlu memvalidasi SQL dan meminta persetujuan user untuk
operasi yang mengubah data.

## Prasyarat

- [uv](https://docs.astral.sh/uv/) terinstall (dependency di-resolve otomatis saat run).
- Env `DATABASE_URL`, contoh: `postgresql://user:pass@localhost:5432/db`

Jalankan server secara langsung:

```bash
uv run --no-project --with "mcp[cli]",psycopg,psycopg-pool python /path/to/postgres-mcp/server.py
```

Ganti `/path/to/postgres-mcp` dengan lokasi clone.

## Claude Code

```bash
claude mcp add postgres --env DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  -- uv run --no-project --with "mcp[cli]",psycopg,psycopg-pool python /path/to/postgres-mcp/server.py
```

Atau lewat `.mcp.json` di root project:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uv",
      "args": ["run", "--no-project", "--with", "mcp[cli],psycopg,psycopg-pool", "python", "/path/to/postgres-mcp/server.py"],
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
args = ["run", "--no-project", "--with", "mcp[cli],psycopg,psycopg-pool", "python", "/path/to/postgres-mcp/server.py"]

[mcp_servers.postgres.env]
DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
```

Atau via CLI:

```bash
codex mcp add postgres --env DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  -- uv run --no-project --with "mcp[cli],psycopg,psycopg-pool" python /path/to/postgres-mcp/server.py
```

## OpenCode

Tambahkan ke `opencode.json` (project) atau `~/.config/opencode/opencode.json` (global):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "postgres": {
      "type": "local",
      "command": ["uv", "run", "--no-project", "--with", "mcp[cli],psycopg,psycopg-pool", "python", "/path/to/postgres-mcp/server.py"],
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
      "args": ["run", "--no-project", "--with", "mcp[cli],psycopg,psycopg-pool", "python", "/path/to/postgres-mcp/server.py"],
      "env": { "DATABASE_URL": "postgresql://user:pass@localhost:5432/db" }
    }
  }
}
```

## Pengujian

```bash
uv run --no-project --with "mcp[cli]",psycopg,psycopg-pool python test_guard.py
```
