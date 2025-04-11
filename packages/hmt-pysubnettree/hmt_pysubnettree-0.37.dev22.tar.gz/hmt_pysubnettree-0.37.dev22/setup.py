#! /usr/bin/env python3

import os

cflags = os.environ.get("CFLAGS", "")
os.environ["CFLAGS"] = cflags + " -fno-strict-aliasing"

from setuptools import setup, Extension


with open('README') as file:
    long_description = file.read()

setup(name="hmt-pysubnettree",
    version="0.37dev22",
    license="BSD",
    description="The PySubnetTree package provides a Python data structure SubnetTree",
    description_content_type="text/markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['SubnetTree'],
    url="https://github.com/zeek/pysubnettree",
    ext_modules=[
        Extension(
            "_SubnetTree",
            sources=["SubnetTree.cc", "patricia.c", "SubnetTree_wrap.cc"],
            depends=["include/SubnetTree.h", "include/patricia.h"],
            include_dirs=["include/"],
        )
    ],
)
