
# testDoctest.py

"""
The first step to use doctest for unit testing.
"""

import unittest
import doctest

import zope.testing

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def test_suite():

    return unittest.TestSuite([

        zope.testing.doctest.DocFileSuite('README.txt',
                                          package='iscorpio.plonepm'),
                           
        zope.testing.doctest.DocFileSuite('tests/README.txt',
                                          package='iscorpio.plonepm'),

        # other text files.
        ])
