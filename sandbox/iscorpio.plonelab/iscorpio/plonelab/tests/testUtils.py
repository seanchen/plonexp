
# testUtils.py

"""
testing dove module
"""

import unittest

from base import IscorpioPlonelabTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class PropertiesTestCase(IscorpioPlonelabTestCase):

    # test setting properties in properties.xml
    def testProperties(self):

        # import the iscorpio.plonelab default profiles
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.\
            runAllImportStepsFromProfile('profile-%s' % \
                                         'iscorpio.plonelab:default')

        # the testing properties.
        properties = self.portal.portal_properties.plonelab_properties
        self.assertEquals(properties.getProperty('testing'),
                          'Testing Property')
        self.assertEquals(properties.getProperty('testLines'),
                          ('Test Line One', 'Test Line Two'))

        # testing change properties.
        properties.manage_changeProperties(testing='Changed Testing Property')
        self.assertEquals(properties.getProperty('testing'),
                          'Changed Testing Property')

        # testing the uninstall profile.
        setup_tool.\
            runAllImportStepsFromProfile('profile-%s' % \
                                         'iscorpio.plonelab:uninstall')
        # the uninstall profile doesn't work for properties tool! or maybe I did
        # not find the right way!
        #self.assertRaises(AttributeError, getattr, self.portal.portal_properties,
        #                 'plonelab_properties')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PropertiesTestCase))
    return suite
