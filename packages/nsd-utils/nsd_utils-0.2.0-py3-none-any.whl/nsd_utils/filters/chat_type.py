# filters/chat_type.py
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from typing import Union

class IsPrivateChat(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        chat = event.chat if isinstance(event, Message) else event.message.chat
        return chat.type == "private"

class IsGroupChat(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        chat = event.chat if isinstance(event, Message) else event.message.chat
        return chat.type in ("group", "supergroup")
