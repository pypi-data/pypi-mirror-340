# nsd_utils/security/rate_limit.py

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
import time

user_requests = {}

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int, interval: float):
        super().__init__()
        self.limit = limit
        self.interval = interval
    async def __call__(self, handler: Callable[[Message|CallbackQuery, Dict[str,Any]], Awaitable[Any]], event: Message|CallbackQuery, data: Dict[str,Any]):
        uid = event.from_user.id
        now = time.time()
        if uid not in user_requests:
            user_requests[uid] = []
        user_requests[uid] = [t for t in user_requests[uid] if now - t < self.interval]
        if len(user_requests[uid]) >= self.limit:
            if isinstance(event, Message):
                await event.answer("Слишком часто")
            else:
                await event.answer("Слишком часто", show_alert=True)
            return
        user_requests[uid].append(now)
        return await handler(event, data)
