"""Postgres MCP server dengan guard destruktif.

- `query`  : SELECT/EXPLAIN saja, dijalankan dalam transaksi read-only.
- `execute`: INSERT/UPDATE/DELETE — wajib confirm=True (client harus minta
  persetujuan user dulu).
- TRUNCATE, DROP, ALTER ... DROP diblokir total, tidak bisa di-confirm.

Env: DATABASE_URL (contoh: postgresql://user:pass@localhost:5432/db)
"""

import os
import re

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("postgres")

BLOCKED = re.compile(
    r"\b(truncate|drop\s+(database|table|schema|owned)|alter\s+table\s+\S+\s+drop)\b",
    re.IGNORECASE,
)
DELETE_RE = re.compile(r"\bdelete\b", re.IGNORECASE)


# ponytail: pool kecil & hemat — min 0 koneksi saat idle, maks 2, koneksi
# nganggur ditutup setelah 60 detik supaya tidak makan memory server DB.
pool = ConnectionPool(
    os.environ.get("DATABASE_URL", ""),
    min_size=0,
    max_size=2,
    max_idle=60,
    open=False,
    kwargs={
        "row_factory": dict_row,
        "application_name": "postgres-mcp",
        # query macet dibunuh 30s, transaksi nganggur dibunuh 10s
        "options": "-c statement_timeout=30000 -c idle_in_transaction_session_timeout=10000",
    },
)

MAX_ROWS = 500


def _connect():
    if pool.closed:
        pool.open()
    return pool.connection()


@mcp.tool()
def query(sql: str) -> list[dict]:
    """Jalankan query read-only (SELECT/EXPLAIN). Ditolak jika mengubah data."""
    if BLOCKED.search(sql):
        raise ValueError("Perintah destruktif (TRUNCATE/DROP) diblokir permanen.")
    with _connect() as conn:
        conn.execute("SET TRANSACTION READ ONLY")
        cur = conn.execute(sql)
        return cur.fetchmany(MAX_ROWS) if cur.description else []


@mcp.tool()
def execute(sql: str, confirm: bool = False) -> str:
    """Jalankan INSERT/UPDATE/DELETE. WAJIB tanya persetujuan user dulu,
    lalu panggil ulang dengan confirm=true. TRUNCATE/DROP selalu ditolak."""
    if BLOCKED.search(sql):
        raise ValueError("TRUNCATE/DROP diblokir permanen, tidak bisa di-confirm.")
    if not confirm:
        verb = "DELETE" if DELETE_RE.search(sql) else "perubahan data"
        raise ValueError(
            f"Butuh konfirmasi user untuk {verb}. Tampilkan SQL ke user, "
            "minta persetujuan, lalu panggil ulang dengan confirm=true."
        )
    with _connect() as conn:
        cur = conn.execute(sql)
        return f"OK, {cur.rowcount} baris terpengaruh."


if __name__ == "__main__":
    mcp.run()
