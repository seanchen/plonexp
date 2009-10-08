
# testProjectPortlets.py

"""
Unit testing the portlets binding to PPMProject.
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

from iscorpio.plonepm.portlets import projectSimpleNav

from base import PlonepmTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocron.com"

class TestProjectSimpleNavPortlet(PlonepmTestCase):

    def testRenderer(self):

        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = projectSimpleNav.Assignment()
        renderer = getMultiAdapter((context, request, view, manager,
                                    assignment),
                                   IPortletRenderer)
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, projectSimpleNav.Renderer))

class TestProjectSimpleNavRenderer(PlonepmTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):

        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = projectSimpleNav.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def testAvailable(self):

        self.loginAsPortalOwner()

        # renderer in root should not available
        renderer = self.renderer()
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project)
        self.failUnless(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata)
        self.failUnless(renderer.available)

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestProjectSimpleNavPortlet))
    suite.addTest(unittest.makeSuite(TestProjectSimpleNavRenderer))

    return suite
