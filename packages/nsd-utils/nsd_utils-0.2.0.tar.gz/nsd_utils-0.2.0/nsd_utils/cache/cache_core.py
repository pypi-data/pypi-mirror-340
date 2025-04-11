# nsd_utils/cache/cache_core.py

import time
from typing import Any, Optional

memory_cache = {}
memory_cache_expire = {}

def cache_get(key: str):
    now = time.time()
    if key in memory_cache:
        if memory_cache_expire[key] == 0 or memory_cache_expire[key] > now:
            return memory_cache[key]
        else:
            del memory_cache[key]
            del memory_cache_expire[key]

def cache_set(key: str, value: Any, ttl: int = 0):
    now = time.time()
    memory_cache[key] = value
    if ttl > 0:
        memory_cache_expire[key] = now + ttl
    else:
        memory_cache_expire[key] = 0

def cache_delete(key: str):
    if key in memory_cache:
        del memory_cache[key]
    if key in memory_cache_expire:
        del memory_cache_expire[key]

def cache_cleanup():
    now = time.time()
    remove_keys = []
    for k, v in memory_cache.items():
        if memory_cache_expire[k] != 0 and memory_cache_expire[k] < now:
            remove_keys.append(k)
    for k in remove_keys:
        del memory_cache[k]
        del memory_cache_expire[k]
