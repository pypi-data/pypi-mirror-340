from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SDK", "readme.md")

with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pythonweblog_client_ws",
    version="0.3.0",
    author="Lucas Bueno",
    author_email="asuma312@gmail.com",
    description="Cliente Python para o serviço pythonweblog em websocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asuma312/python-weblogging",
    packages=find_packages(),
    package_data={
        'SDK': ['readme.md'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-socketio",
        "websocket-client"
    ],
)