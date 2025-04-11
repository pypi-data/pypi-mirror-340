# nsd_utils/db/session_manager.py

import asyncpg
from typing import Optional

_pool: Optional[asyncpg.Pool] = None

async def init_db_pool(dsn: str):
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn)
    return _pool

async def get_pool():
    if _pool is None:
        raise RuntimeError("DB Pool not initialized")
    return _pool

async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
