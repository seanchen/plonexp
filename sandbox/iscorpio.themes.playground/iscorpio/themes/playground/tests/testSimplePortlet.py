
# testSimplePortlet.py

"""
Here we testing the simple portlet.
"""

import unittest

from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletDataProvider

from Products.GenericSetup.utils import _getDottedName

import iscorpio.themes.playground
from iscorpio.themes.playground.portlet import simple

from base import PlaygroundTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestSimplePortlet(PlaygroundTestCase):

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType,
                             name='iscorpio.themes.playground.portlet.Simple')
        self.assertEquals(portlet.addview,
                          'iscorpio.themes.playground.portlet.Simple')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType,
                             name='iscorpio.themes.playground.portlet.Simple')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
                           'plone.app.portlets.interfaces.IDashboard'],
                          registered_interfaces)

    def testInterfaces(self):
        portlet = simple.SimpleAssignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = simple.SimpleAssignment()

        renderer = getMultiAdapter((context, request, view, manager,
                                    assignment),
                                   IPortletRenderer)
        self.failUnless(renderer.available is False)
        self.failUnless(isinstance(renderer, simple.SimpleRenderer))

class TestRenderer(PlaygroundTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = simple.SimpleAssignment()

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def testAvailable4News(self):

        self.portal.invokeFactory('News Item', 'news1')
        newsItem = getattr(self.portal, 'news1')
        r = self.renderer(context=newsItem)
        self.failUnless(r.available is True)

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSimplePortlet))
    suite.addTest(unittest.makeSuite(TestRenderer))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
