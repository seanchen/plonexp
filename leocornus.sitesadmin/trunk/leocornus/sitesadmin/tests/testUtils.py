
# testUtils.py

"""
testing utilities.
"""

import unittest

from Products.PloneTestCase.setup import SiteSetup

from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class InstallationTestCase(SitesAdminTestCase):
    """
    make sure we can install sitesadmin properly.
    """

    def testInstallation(self):
        """
        the default Plone site for testing have everything installed
        properly, we will create a new Plone site here for testing.
        """

        # setup an empty Plone site.
        import pdb; pdb.set_trace()
        SiteSetup(id='installation',
                  policy='Default Plone',
                  products=['leocornus.sitesadmin'],
                  quiet=0,
                  with_default_memberarea=1,
                  base_profile='CMFPlone:plone',
                  extension_profiles=()).run()
        install = getattr(self.app, 'installation')
        # by this point, membrane should be installed.
        user_folder = install.acl_users
        assertTrue('membrane_users' in user_folder.objectIds())

class PropertiesTestCase(SitesAdminTestCase):

    # test setting properties in properties.xml
    def testProperties(self):

        # import the iscorpio.plonelab default profiles
        #setup_tool = getattr(self.portal, 'portal_setup')
        #setup_tool.\
        #    runAllImportStepsFromProfile('profile-%s' % \
        #                                 'leocornus.sitesadmin:default')

        # the testing properties.
        properties = self.portal.portal_properties.sitesadmin_properties
        self.assertEquals(properties.getProperty('title'),
                          'Sites Admin Properties')
        self.assertEquals(properties.getProperty('productsNotToList'),
                          ('Products.NuPlone', 'NuPlone'))

        # testing change properties.
        properties.manage_changeProperties(title='Changed Testing Property')
        self.assertEquals(properties.getProperty('title'),
                          'Changed Testing Property')

def test_suite():
    suite = unittest.TestSuite()
    # could not create another Plone site! Maybe we need create a didderent
    # layer!
    #suite.addTest(unittest.makeSuite(InstallationTestCase))
    suite.addTest(unittest.makeSuite(PropertiesTestCase))
    return suite
