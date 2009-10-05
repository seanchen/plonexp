
# testSimplePortlet.py

"""
Here we testing the simple portlet.
"""

import unittest

from zope.component import getUtility

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider

from Products.GenericSetup.utils import _getDottedName

import iscorpio.themes.playground
from iscorpio.themes.playground.portlet import simple

from base import PlaygroundTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestSimplePortlet(PlaygroundTestCase):

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
