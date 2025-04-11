# nsd_utils/aiogram_utils/safe_send.py

from aiogram.types import Message, CallbackQuery
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")
from nsd_utils.logging.log_helpers import log_chat_error_obj, log_user_error_obj

async def safe_send_message(msg: Message, text: str, reply_markup=None):
    try:
        return await msg.answer(text, reply_markup=reply_markup)
    except Exception as e:
        if msg.chat.type in ("group", "supergroup"):
            log_chat_error_obj(msg, f"{e}")
        else:
            log_user_error_obj(msg, f"{e}")

async def safe_edit_message(call: CallbackQuery, text: str, reply_markup=None):
    try:
        return await call.message.edit_text(text, reply_markup=reply_markup)
    except Exception as e:
        if call.message.chat.type in ("group", "supergroup"):
            log_chat_error_obj(call, f"{e}")
        else:
            log_user_error_obj(call, f"{e}")
