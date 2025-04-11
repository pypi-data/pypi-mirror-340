# nsd_utils/security/rbac.py

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from typing import Union

async def get_user_role(user_id: int):
    if user_id == 1005695473:
        return "owner"
    return "user"

ROLES_PRIORITY = {
    "user": 1,
    "admin": 2,
    "owner": 3
}

class RoleFilter(Filter):
    def __init__(self, required_role: str):
        self.required_role = required_role
    async def __call__(self, event: Message|CallbackQuery) -> bool:
        uid = event.from_user.id
        role = await get_user_role(uid)
        if ROLES_PRIORITY.get(role, 0) >= ROLES_PRIORITY.get(self.required_role, 0):
            return True
        return False
