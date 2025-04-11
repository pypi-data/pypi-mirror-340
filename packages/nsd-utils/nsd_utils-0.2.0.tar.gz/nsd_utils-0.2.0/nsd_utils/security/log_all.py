# nsd_utils/security/log_all.py

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
from nsd_utils.logging.log_helpers import log_chat_message_obj, log_user_message_obj, log_chat_action_obj, log_user_action_obj

class LogAllMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message|CallbackQuery, Dict[str,Any]], Awaitable[Any]], event: Message|CallbackQuery, data: Dict[str,Any]):
        try:
            if isinstance(event, Message):
                if event.chat.type in ("group","supergroup"):
                    log_chat_message_obj(event, event.text or "")
                else:
                    log_user_message_obj(event, event.text or "")
            elif isinstance(event, CallbackQuery):
                if event.message.chat.type in ("group","supergroup"):
                    log_chat_action_obj(event, event.data or "")
                else:
                    log_user_action_obj(event, event.data or "")
        except:
            pass
        return await handler(event, data)
