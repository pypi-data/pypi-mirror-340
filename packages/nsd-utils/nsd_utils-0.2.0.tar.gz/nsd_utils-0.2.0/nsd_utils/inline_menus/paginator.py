# nsd_utils/inline_menus/paginator.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

def build_pagination_keyboard(prefix, current_page, total_pages):
    kb = []
    row = []
    if current_page > 1:
        row.append(InlineKeyboardButton("⬅️", callback_data=f"{prefix}|page={current_page-1}"))
    else:
        row.append(InlineKeyboardButton(" ", callback_data="none"))
    row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="none"))
    if current_page < total_pages:
        row.append(InlineKeyboardButton("➡️", callback_data=f"{prefix}|page={current_page+1}"))
    else:
        row.append(InlineKeyboardButton(" ", callback_data="none"))
    kb.append(row)
    return InlineKeyboardMarkup(inline_keyboard=kb)

def paginate_list(items, page=1, per_page=5):
    total = len(items)
    start = (page-1)*per_page
    end = start+per_page
    return items[start:end], total
