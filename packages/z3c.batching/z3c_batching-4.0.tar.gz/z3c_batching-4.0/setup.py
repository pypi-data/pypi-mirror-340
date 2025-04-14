##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for z3c.batching package"""

import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="z3c.batching",
    version="4.0",
    author="Zope Foundation and Contributors",
    author_email="zope-dev@zope.dev",
    description="List batching support",
    long_description="".join(
        [
            read("README.rst"),
            "\n\n",
            "======================\n",
            "Detailed Documentation\n",
            "======================\n",
            "\n\n",
            read("src", "z3c", "batching", "README.rst"),
            "\n\n",
            read("src", "z3c", "batching", "subset.rst"),
            "\n\n",
            read("CHANGES.rst"),
        ]
    ),
    keywords="zope3 batching",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Zope",
        "Framework :: Zope :: 3",
    ],
    url="https://github.com/zopefoundation/z3c.batching",
    license="ZPL-2.1",
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        "zope.interface",
        "zope.schema",
    ],
    include_package_data=True,
    zip_safe=False,
)
