from __future__ import annotations

import os

from setuptools import find_namespace_packages, setup

# Read the content of README.md for the long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fitgirl",
    version="0.1.1",
    description=(
        "A stack of functions to help scrape the popular FitGirl Repacks website and parse game data efficiently."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Xsyncio",
    maintainer="Xsyncio",
    url="https://www.github.com/xsyncio/fitgirl",
    project_urls={
        "Bug Tracker": "https://github.com/xsyncio/fitgirl/issues",
        "Source": "https://github.com/xsyncio/fitgirl",
    },
    packages=find_namespace_packages(include=["fitgirl*"]),
    python_requires=">=3.7",
    install_requires=["httpx>=0.23.0", "beautifulsoup4>=4.9.3"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
