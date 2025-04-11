# nsd_utils/inline_menus/menu_builder.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

class InlineMenuBuilder:
    def __init__(self, prefix="menu"):
        self.prefix = prefix
        self.rows = [[]]
    def add_button(self, text, callback):
        c = f"{self.prefix}:{callback}"
        b = InlineKeyboardButton(text=text, callback_data=c)
        self.rows[-1].append(b)
        return self
    def new_row(self):
        self.rows.append([])
        return self
    def build(self):
        return InlineKeyboardMarkup(inline_keyboard=self.rows)
