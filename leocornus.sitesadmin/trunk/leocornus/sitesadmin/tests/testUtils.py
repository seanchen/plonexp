
# testUtils.py

"""
testing utilities.
"""

import unittest

from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

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
    suite.addTest(unittest.makeSuite(PropertiesTestCase))
    return suite
