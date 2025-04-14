#! /usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="canonicalwebteam.directory-parser",
    version="1.2.0",
    author="Canonical webteam",
    author_email="webteam@canonical.com",
    url="https://github.com/canonical/canonicalwebteam.directory-parser",
    description=(
        "Flask extension to parse websites and extract structured data to "
        "build sitemaps."
    ),
    packages=find_packages(where="canonicalwebteam"),
    package_dir={"": "canonicalwebteam"},
    package_data={
      "directory_parser": ["templates/*.xml"]
    },
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "Flask>=1.0.2",
        "beautifulsoup4",
        "humanize",
        "lxml",
        "requests",
        "python-dateutil",
        "validators",
        "python-slugify",
    ],
)
