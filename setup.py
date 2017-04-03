#!/usr/bin/env python

from setuptools import setup


setup(
    name="SMTK",
    version='0.0.1',
    description="Make social media collection & network mapping process as simple as possible for researchers.",
    url="https://github.com/Data4Democracy",
    platforms="Posix; MacOS X; Windows",
    entry_points = {
        "console_scripts": ['smtk = smtk.main:main']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Data science",
    ],
    packages=[
        "smtk",
        "smtk.utils",
        "smtk.examples"
    ],
    install_requires=[]
)
