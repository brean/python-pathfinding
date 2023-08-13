#!/usr/bin/env python
from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pathfinding",
    description="Pathfinding algorithms (based on Pathfinding.JS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brean/python-pathfinding",
    version="1.0.3",
    license="MIT",
    author="Andreas Bresser",
    packages=find_packages(),
    tests_require=["numpy", "pandas"],
    include_package_data=True,
    install_requires=[],
)
