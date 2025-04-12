#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" setup.py for pypi """

import setuptools
from ix_notifiers import constants

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ix-notifiers",
    version=f"{constants.VERSION}.{constants.BUILD}",
    author="ix.ai",
    author_email="notifiers@egos.tech",
    description="A python library for notifiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url="https://gitlab.com/egos-tech/notifiers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests==2.32.3',
    ],
)
