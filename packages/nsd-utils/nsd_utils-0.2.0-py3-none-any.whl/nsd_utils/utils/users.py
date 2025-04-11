# nsd_utils/utils/users.py

from aiogram.types import Message, CallbackQuery

def get_user_info(obj):
    if isinstance(obj, Message):
        u = obj.from_user
    else:
        u = obj.from_user
    i = u.id
    un = u.username or f"id_{i}"
    fn = (u.first_name or "") + " " + (u.last_name or "")
    return {
        "id": i,
        "username": un.strip(),
        "full_name": fn.strip(),
        "first_name": u.first_name or "",
        "last_name": u.last_name or ""
    }

def get_chat_info(obj):
    if isinstance(obj, Message):
        c = obj.chat
    else:
        c = obj.message.chat
    return {
        "id": c.id,
        "title": c.title or f"chat_{c.id}",
        "type": c.type
    }
