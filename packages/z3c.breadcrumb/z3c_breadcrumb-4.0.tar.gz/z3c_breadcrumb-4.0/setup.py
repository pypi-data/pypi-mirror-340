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
"""Setup"""

import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="z3c.breadcrumb",
    version="4.0",
    author="Roger Ineichen, Stephan Richter and the Zope Community",
    author_email="zope-dev@zope.dev",
    description="A pluggable breadcrumbs implementation based on adapters.",
    long_description=(
        read("README.rst") + "\n\n" + "Detailed Documentation\n"
        "**********************\n"
        + "\n"
        + read("src", "z3c", "breadcrumb", "README.rst")
        + "\n\n"
        + read("CHANGES.rst")
    ),
    license="ZPL-2.1",
    keywords="zope3 breadcrumb adapter",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Zope :: 3",
    ],
    url="https://github.com/zopefoundation/z3c.breadcrumb",
    python_requires=">=3.9",
    extras_require=dict(
        test=[
            "zope.container",
            "zope.site",
            "zope.testing",
        ],
    ),
    install_requires=[
        "setuptools",
        "zope.component",
        "zope.interface",
        "zope.location",
        "zope.publisher",
        "zope.schema",
        "zope.traversing",
    ],
    include_package_data=True,
    zip_safe=False,
)
