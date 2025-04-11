# nsd_utils/utils/handlers_loader.py

import importlib
import os
from aiogram import Dispatcher, Router
from typing import List

def load_routers_from_directory(directory: str) -> List[Router]:
    routers = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                p = os.path.join(root, file)
                rel = os.path.relpath(p, directory)
                mod_name = rel.replace(os.sep, ".")[:-3]
                full = f"{directory}.{mod_name}"
                try:
                    m = importlib.import_module(full)
                    if hasattr(m, "router"):
                        r = getattr(m, "router")
                        if isinstance(r, Router):
                            routers.append(r)
                except:
                    pass
    return routers

def include_all_handlers(dp: Dispatcher, directory: str = "handlers"):
    rs = load_routers_from_directory(directory)
    for r in rs:
        dp.include_router(r)
