# nsd_utils/logging/log_helpers.py

from aiogram.types import Message, CallbackQuery
from nsd_utils.utils.users import get_user_info, get_chat_info
from nsd_utils.logging.logger_core import log_personal_message, log_personal_error, log_personal_action, log_chat_message, log_chat_error, log_chat_action, log_global_event, log_global_error

def log_user_message(user_id, username, full_name, text):
    log_personal_message(user_id, username, full_name, text)

def log_user_action(user_id, username, full_name, action):
    log_personal_action(user_id, username, full_name, action)

def log_user_error(user_id, username, full_name, err):
    log_personal_error(user_id, username, full_name, err)

def log_chat_message_wrapper(chat_id, chat_title, text):
    log_chat_message(chat_id, chat_title, text)

def log_chat_action_wrapper(chat_id, chat_title, action):
    log_chat_action(chat_id, chat_title, action)

def log_chat_error_wrapper(chat_id, chat_title, err):
    log_chat_error(chat_id, chat_title, err)

def log_system_event(message):
    log_global_event(message)

def log_system_error(message):
    log_global_error(message)

def log_user_message_obj(obj, text):
    u = get_user_info(obj)
    log_personal_message(u["id"], u["username"], u["full_name"], text)

def log_user_action_obj(obj, action):
    u = get_user_info(obj)
    log_personal_action(u["id"], u["username"], u["full_name"], action)

def log_user_error_obj(obj, err):
    u = get_user_info(obj)
    log_personal_error(u["id"], u["username"], u["full_name"], err)

def log_chat_message_obj(obj, text):
    u = get_user_info(obj)
    c = get_chat_info(obj)
    m = f"{text}\n{u['full_name']}(@{u['username']})\n{c['title']}"
    log_chat_message(c["id"], c["title"], m)

def log_chat_action_obj(obj, action):
    u = get_user_info(obj)
    c = get_chat_info(obj)
    a = f"{action}\n{u['full_name']}(@{u['username']})\n{c['title']}"
    log_chat_action(c["id"], c["title"], a)

def log_chat_error_obj(obj, err):
    u = get_user_info(obj)
    c = get_chat_info(obj)
    e = f"{err}\n{u['full_name']}(@{u['username']})\n{c['title']}"
    log_chat_error(c["id"], c["title"], e)

def log_any_message(obj, text):
    t = obj.message.chat.type if isinstance(obj, CallbackQuery) else obj.chat.type
    if t in ("group", "supergroup"):
        log_chat_message_obj(obj, text)
    else:
        log_user_message_obj(obj, text)
