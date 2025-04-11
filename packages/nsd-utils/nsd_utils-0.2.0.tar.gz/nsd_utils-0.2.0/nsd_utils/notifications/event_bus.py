# nsd_utils/notifications/event_bus.py

import asyncio
_subscribers = {}

def on(event_name: str):
    def decorator(func):
        if event_name not in _subscribers:
            _subscribers[event_name] = []
        _subscribers[event_name].append(func)
        return func
    return decorator

async def emit_async(event_name: str, **kwargs):
    if event_name not in _subscribers:
        return
    tasks = []
    for f in _subscribers[event_name]:
        t = asyncio.create_task(f(**kwargs))
        tasks.append(t)
    await asyncio.gather(*tasks)

def emit_sync(event_name: str, **kwargs):
    if event_name not in _subscribers:
        return
    for f in _subscribers[event_name]:
        f(**kwargs)
