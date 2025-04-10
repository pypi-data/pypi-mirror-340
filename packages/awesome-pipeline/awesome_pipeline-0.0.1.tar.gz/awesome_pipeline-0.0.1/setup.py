#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

setup(
    name="awesome_pipeline",
    version="0.0.1",
    author="Andy Yang",
    author_email="yong.yang@health.nsw.gov.au",
    description="A framework for data standardised pipeline  platform",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    packages=find_packages(),
    license="private",
    keywords="None",
    install_requires=[
        # "requests",
        "pandas",
        "numpy",
        "xmltodict",
        "sqlalchemy",
        "pyyaml",
        "beautifulsoup4",
        "ydata-profiling",
        "pandasql",
    ],
    python_requires=">3.6",
)
