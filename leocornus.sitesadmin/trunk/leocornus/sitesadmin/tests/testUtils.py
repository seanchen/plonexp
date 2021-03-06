
# testUtils.py

"""
testing utilities.
"""

import unittest

from Products.PloneTestCase.setup import SiteSetup

from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class PropertiesTestCase(SitesAdminTestCase):

    # test setting properties in properties.xml
    def testProperties(self):

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
