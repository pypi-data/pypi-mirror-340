from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="SG23001UNO",
    version="0.1.1",
    description="Librería sencilla para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Eduardo Salamanca Garcia",
    packages=find_packages(),
    license="MIT"
)
