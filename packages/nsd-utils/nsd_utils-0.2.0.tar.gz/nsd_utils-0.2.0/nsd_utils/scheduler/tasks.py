# nsd_utils/scheduler/tasks.py

import asyncio
import datetime

_scheduled_tasks = []

def schedule_task(coro_func, interval_seconds: int):
    _scheduled_tasks.append((coro_func, interval_seconds))

async def _runner(coro_func, interval):
    while True:
        try:
            await coro_func()
        except Exception as e:
            pass
        await asyncio.sleep(interval)

async def init_scheduler():
    for func, interval in _scheduled_tasks:
        asyncio.create_task(_runner(func, interval))

async def example_task():
    print(datetime.datetime.now())
