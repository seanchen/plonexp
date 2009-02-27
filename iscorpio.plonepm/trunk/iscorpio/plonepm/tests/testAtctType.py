"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest

from Interface.Verify import verifyObject

from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase
from Products.CMFCore.utils import getToolByName

# for Zope 3.
from Products.ATContentTypes.interface import IATFolder as Z3IATFolder
from zope.interface.verify import verifyObject as Z3verifyObject

from iscorpio.plonepm.content.PPMProject import PPMProject
from iscorpio.plonepm.tests.base import PlonepmTestCase

class TestPPMProject(ATCTTypeTestCase):
    """ Testing basics about the AT Content Types within this product.
    """

    klass = PPMProject
    portal_type = "PPMProject"
    # the title in the types xml file.
    title = 'XP Project'
    meta_type = 'PPMProject'
    icon = 'XPProject_icon.gif'

    def test_implementsATFolder(self):
        iface = IATFolder
        self.failUnless(iface.isImplementedBy(self._ATCT))
        self.failUnless(verifyObject(iface, self._ATCT))

    def test_Z3implementsATFolder(self):
        iface = Z3IATFolder
        self.failUnless(Z3verifyObject(iface, self._ATCT))

# making test suite.
def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPPMProject))
    return suite
