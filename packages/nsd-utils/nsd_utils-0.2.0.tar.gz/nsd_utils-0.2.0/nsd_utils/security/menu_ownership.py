# nsd_utils/security/menu_ownership.py

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery
from typing import Callable, Awaitable, Dict, Any

menu_owners = {}

def set_menu_owner(msg_id: tuple, user_id: int):
    menu_owners[msg_id] = user_id

def get_menu_owner(msg_id: tuple):
    return menu_owners.get(msg_id)

class MenuOwnershipMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery, Dict[str,Any]], Awaitable[Any]], event: CallbackQuery, data: Dict[str,Any]):
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)
        key = (event.message.chat.id, event.message.message_id)
        owner = get_menu_owner(key)
        if owner and owner != event.from_user.id:
            await event.answer("Это не ваше меню", show_alert=True)
            return
        return await handler(event, data)
