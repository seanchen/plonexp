
# testImportSteps.py

"""
testing generic setup import steps.
"""

import unittest

from Products.CMFCore.utils import getToolByName

from base import YgedfTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class InstallationTestCase(YgedfTestCase):
    """
    make sure we can install sitesadmin properly.
    """

    def afterSetUp(self):

        # get an empty Plone site to test the generic setup installation
        pass

    def testQuickInstaller(self):
        """
        install leocornus.ygedf by using the quick installer.
        """

        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.installProduct('leocornus.ygedf')
        # by this point, membrane should be installed.

    def testImportProfile(self):
        """
        test using setup tool to import profiles.
        """

        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.ygedf:default')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallationTestCase))
    return suite
