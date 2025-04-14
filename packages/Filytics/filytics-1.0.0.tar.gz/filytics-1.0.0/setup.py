import os
from setuptools import setup, find_packages


def read_long_description(filename: str = "README.md") -> str:
    """
    Reads the long description from the specified file.
    Fails fast if the file is not found.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Long description file '{filename}' not found.")
    with open(filename, encoding="utf-8") as f:
        return f.read()


setup(
    name="Filytics",
    version="1.0.0",
    author="oaslananka",
    author_email="admin@oaslananka.dev",
    description="File and folder statistics analyzer CLI tool",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/oaslananka/Filytics",
    packages=find_packages(),
    install_requires=[
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "filytics = Filytics.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
