
# testImportSteps.py

"""
testing generic setup import steps.
"""

import unittest

from Products.CMFCore.utils import getToolByName

from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class InstallationTestCase(SitesAdminTestCase):
    """
    make sure we can install sitesadmin properly.
    """

    def afterSetUp(self):

        # get an empty Plone site to test the generic setup installation
        self.emptySite = getattr(self.app, 'site1')

    def testQuickInstaller(self):
        """
        install leocornus.sitesadmin by using the quick installer.
        """

        user_folder = self.emptySite.acl_users
        self.failIf('membrane_users' in user_folder.objectIds())

        installer = getToolByName(self.emptySite, 'portal_quickinstaller')
        installer.installProduct('leocornus.sitesadmin')
        # by this point, membrane should be installed.
        self.assertTrue('membrane_users' in user_folder.objectIds())

    def testImportProfile(self):
        """
        test using setup tool to import profiles.
        """

        user_folder = self.emptySite.acl_users
        self.failIf('membrane_users' in user_folder.objectIds())

        setup_tool = getattr(self.emptySite, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:default')

        self.assertTrue('membrane_users' in user_folder.objectIds())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallationTestCase))
    return suite
