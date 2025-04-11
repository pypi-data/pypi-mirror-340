# nsd_utils/logging/logger_core.py

import os
import logging
from datetime import datetime

LOGS_DIR = "logs"
GENERAL_LOGS_DIR = os.path.join(LOGS_DIR, "general")
PERSONAL_LOGS_DIR = os.path.join(LOGS_DIR, "personal")
CHATS_LOGS_DIR = os.path.join(LOGS_DIR, "chats")
EVENTS_LOG = os.path.join(GENERAL_LOGS_DIR, "events.log")
ERRORS_LOG = os.path.join(GENERAL_LOGS_DIR, "errors.log")

def time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def init_logger():
    os.makedirs(GENERAL_LOGS_DIR, exist_ok=True)
    os.makedirs(PERSONAL_LOGS_DIR, exist_ok=True)
    os.makedirs(CHATS_LOGS_DIR, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", handlers=[logging.FileHandler(EVENTS_LOG, encoding="utf-8"), logging.StreamHandler()])
    e = logging.FileHandler(ERRORS_LOG, encoding="utf-8")
    e.setLevel(logging.ERROR)
    logging.getLogger().addHandler(e)
    logging.info("Logger initialized")

def sanitize_filename(n):
    return "".join(c for c in n if c.isalnum() or c in ("_", "-")).strip()

def personal_dir(uid, username=None, fullname=None):
    s = str(uid)
    if username:
        s += f"_{sanitize_filename(username)}"
    elif fullname:
        s += f"_{sanitize_filename(fullname)}"
    p = os.path.join(PERSONAL_LOGS_DIR, s)
    os.makedirs(p, exist_ok=True)
    return p

def chat_dir(cid, title):
    s = f"{cid}_{sanitize_filename(title)}"
    p = os.path.join(CHATS_LOGS_DIR, s)
    os.makedirs(p, exist_ok=True)
    return p

def log_personal_message(uid, un, fn, text):
    m = f"{time_str()} [PERSONAL_MSG] {text}"
    print(m)
    d = personal_dir(uid, un, fn)
    with open(os.path.join(d, "messages.log"), "a", encoding="utf-8") as f:
        f.write(m+"\n")

def log_personal_error(uid, un, fn, err):
    e = f"{time_str()} [PERSONAL_ERR] {err}"
    logging.error(e)
    d = personal_dir(uid, un, fn)
    with open(os.path.join(d, "errors.log"), "a", encoding="utf-8") as f:
        f.write(e+"\n")

def log_personal_action(uid, un, fn, action):
    a = f"{time_str()} [PERSONAL_ACT] {action}"
    print(a)
    d = personal_dir(uid, un, fn)
    with open(os.path.join(d, "actions.log"), "a", encoding="utf-8") as f:
        f.write(a+"\n")

def log_chat_message(cid, ct, text):
    m = f"{time_str()} [CHAT_MSG] {text}"
    print(m)
    d = chat_dir(cid, ct)
    with open(os.path.join(d, "messages.log"), "a", encoding="utf-8") as f:
        f.write(m+"\n")

def log_chat_error(cid, ct, err):
    e = f"{time_str()} [CHAT_ERR] {err}"
    logging.error(e)
    d = chat_dir(cid, ct)
    with open(os.path.join(d, "errors.log"), "a", encoding="utf-8") as f:
        f.write(e+"\n")

def log_chat_action(cid, ct, action):
    a = f"{time_str()} [CHAT_ACT] {action}"
    print(a)
    d = chat_dir(cid, ct)
    with open(os.path.join(d, "actions.log"), "a", encoding="utf-8") as f:
        f.write(a+"\n")

def log_global_event(msg):
    logging.info(msg)

def log_global_error(msg):
    logging.error(msg)
