# nsd_utils/aiogram_utils/text_templates.py

import os
from jinja2 import Environment, FileSystemLoader
from aiogram import __version__ as AIOGRAM_VERSION
if AIOGRAM_VERSION != "3.19":
    raise RuntimeError("Requires aiogram==3.19")

def create_jinja_env(templates_dir: str = "templates"):
    loader = FileSystemLoader(templates_dir)
    return Environment(loader=loader, autoescape=True)

def render_template(env: Environment, template_name: str, context: dict):
    tmpl = env.get_template(template_name)
    return tmpl.render(**context)
