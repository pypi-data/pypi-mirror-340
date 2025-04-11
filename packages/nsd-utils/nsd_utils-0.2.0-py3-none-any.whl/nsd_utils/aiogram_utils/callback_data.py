# nsd_utils/aiogram_utils/callback_data.py

from aiogram.filters.callback_data import CallbackData
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

class MenuCallback(CallbackData, prefix="menu"):
    action: str
    page: int = 1
