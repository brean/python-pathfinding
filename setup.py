#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="pathfinding",
    description="Pathfinding algorithms (based on Pathfinding.JS)",
    url="https://github.com/brean/python-pathfinding",
    version="0.0.2",
    license="MIT",
    author="Andreas Bresser",
    packages=find_packages(),
    tests_require=["numpy", "pandas"],
    include_package_data=True,
    install_requires=[],
)
