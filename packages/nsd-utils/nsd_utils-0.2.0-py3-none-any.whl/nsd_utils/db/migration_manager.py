# nsd_utils/db/migration_manager.py

import asyncpg
import os
from pathlib import Path
from nsd_utils.db.session_manager import get_pool

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

async def init_migrations_table(conn: asyncpg.Connection):
    await conn.execute("CREATE TABLE IF NOT EXISTS schema_version(id INT PRIMARY KEY DEFAULT 1,version INT NOT NULL)")
    row = await conn.fetchrow("SELECT version FROM schema_version WHERE id=1")
    if not row:
        await conn.execute("INSERT INTO schema_version(id, version) VALUES(1, 0)")

async def get_current_version(conn: asyncpg.Connection):
    row = await conn.fetchrow("SELECT version FROM schema_version WHERE id=1")
    if row:
        return row["version"]
    return 0

async def set_current_version(conn: asyncpg.Connection, v: int):
    await conn.execute("UPDATE schema_version SET version=$1 WHERE id=1", v)

async def apply_migrations():
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await init_migrations_table(conn)
            cv = await get_current_version(conn)
            fs = []
            for f in MIGRATIONS_DIR.glob("*.sql"):
                prefix = f.name.split("_", 1)[0]
                try:
                    n = int(prefix)
                    fs.append((n, f))
                except:
                    pass
            fs.sort(key=lambda x: x[0])
            for num, path in fs:
                if num > cv:
                    sql = path.read_text("utf-8")
                    await conn.execute(sql)
                    await set_current_version(conn, num)
