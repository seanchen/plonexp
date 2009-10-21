
# testDove.py

"""
testing dove module
"""

import unittest

from base import IscorpioZopelabTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class DoveTestCase(IscorpioZopelabTestCase):

    # test setting properties in properties.xml
    def testProperties(self):

        # import the iscorpio.zopelab.dove profiles
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.\
            runAllImportStepsFromProfile('profile-%s' % \
                                         'iscorpio.zopelab.dove:dove')

        properties = self.portal.portal_properties.navtree_properties
        self.assertEquals(properties.getProperty('name'), 'navtree')
        self.assertTrue(properties.getProperty('something_new'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DoveTestCase))
    return suite
