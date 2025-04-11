# setup.py

import setuptools

setuptools.setup(
    name="nsd_utils",
    version="0.2.0",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiogram==3.19",
        "asyncpg>=0.27",
        "jinja2>=3.0",
        "babel>=2.9",
        "pydantic>=1.10"
    ],
    python_requires=">=3.9"
)
