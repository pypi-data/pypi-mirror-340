from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')


setup(
    name="bootcamp_for_python_basic_data_structures",
    version="0.0.1",
    description="A collection of basic data structures in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abenezer Angamo",
    author_email="aben.jacob3@gmail.com",
    url="https://abenezerkb.github.io/basic-python-data-structure/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
