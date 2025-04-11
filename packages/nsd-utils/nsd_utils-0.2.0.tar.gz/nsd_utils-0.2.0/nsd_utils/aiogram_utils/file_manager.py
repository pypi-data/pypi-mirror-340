# nsd_utils/aiogram_utils/file_manager.py

import os
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

def download_file_path(bot: Bot, file_id: str, save_dir: str = "downloads"):
    return os.path.join(save_dir, file_id)

async def download_file(bot: Bot, file_id: str, save_dir: str = "downloads"):
    path = download_file_path(bot, file_id, save_dir)
    os.makedirs(save_dir, exist_ok=True)
    info = await bot.get_file(file_id)
    await bot.download_file(info.file_path, path)
    return path

def local_photo(path: str):
    return FSInputFile(path)
