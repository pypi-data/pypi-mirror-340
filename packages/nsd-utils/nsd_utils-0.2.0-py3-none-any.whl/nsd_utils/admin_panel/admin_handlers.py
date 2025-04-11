# admin_panel/admin_handlers.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
# Исправляем import:
# Было: from security.rbac import RoleFilter
# Становится: from nsd_utils.security.rbac import RoleFilter
from nsd_utils.security.rbac import RoleFilter

router = Router()

@router.message(RoleFilter("admin"), F.text == "/admin")
async def admin_menu(msg: Message):
    # Вывести inline-кнопки /admin
    await msg.answer("Админ-меню: \n1) Список пользователей\n2) ...")

@router.message(RoleFilter("admin"), F.text == "/users")
async def show_users(msg: Message):
    # Логика, которая показывает список...
    pass

# и так далее...
