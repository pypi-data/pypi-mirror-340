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
"""Tests"""

import doctest
import unittest

import zope.location
import zope.site.testing
import zope.traversing.testing
from zope.interface.verify import verifyObject
from zope.publisher.browser import TestRequest


def doctest_Breadcrumbs_interface():
    """Test that Breadcrumbs matches the interface

    >>> from z3c.breadcrumb import browser, interfaces
    >>> breadcrumbs = browser.Breadcrumbs(None, None)
    >>> verifyObject(interfaces.IBreadcrumbs, breadcrumbs)
    True

    """


def doctest_GenericBreadcrumb_interface():
    """Test that GenericBreadcrumb matches the interface

    >>> from z3c.breadcrumb import browser, interfaces
    >>> breadcrumb = browser.GenericBreadcrumb(rootFolder, TestRequest())
    >>> verifyObject(interfaces.IBreadcrumb, breadcrumb)
    True

    """


def setUp(test):
    site = zope.site.testing.siteSetUp(True)
    zope.traversing.testing.setUp()
    test.globs["rootFolder"] = site


def tearDown(test):
    zope.site.testing.siteTearDown()


def test_suite():
    return unittest.TestSuite(
        [
            doctest.DocFileSuite(
                "README.rst",
                setUp=setUp,
                tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            ),
            doctest.DocTestSuite(setUp=setUp, tearDown=tearDown),
        ]
    )
