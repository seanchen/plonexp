
# tests.py

"""
The unit test cases for iscorpio thems playground
"""

import unittest

from Products.PloneTestCase import PloneTestCase as ptc

from zope.component import getUtility

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider

from Products.GenericSetup.utils import _getDottedName

import iscorpio.themes.playground
from iscorpio.themes.playground.portlet import simple

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

ptc.setupPloneSite()

class PlaygroundTestCase(ptc.PloneTestCase):
    """
    base for test cases.
    """

class TestSimplePortlet(PlaygroundTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.manage_addFolder('portlets', 'Testing Portlets')
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % 'iscorpio.themes.playground:default')

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='iscorpio.themes.playground.portlet.Simple')
        self.assertEquals(portlet.addview, 'iscorpio.themes.playground.portlet.Simple')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='iscorpio.themes.playground.portlet.Simple')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
                           'plone.app.portlets.interfaces.IDashboard'],
                          registered_interfaces)

    def testInterfaces(self):
        portlet = simple.SimpleAssignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet))

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSimplePortlet))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
