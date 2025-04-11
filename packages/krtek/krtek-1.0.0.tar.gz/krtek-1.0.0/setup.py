"Setup script for package"
import pathlib
from setuptools import setup, find_packages

short_description = "Package for mining association rules using GUHA and Redescription mining."

setup(
    name="krtek",
    version="1.0.0",
    license="MIT",
    author="Marek Brodacký",
    author_email="brodackym@gmail.com",
    url="https://github.com/slunimara",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
    ],
    description=short_description,
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords="GUHA, Redescription mining, Association rules, Data mining",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
)
