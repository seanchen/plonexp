
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
from iscorpio.plonepm.portlets import recentArtifacts

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

    def testProjectInfo(self):

        self.loginAsPortalOwner()

        # get project info on a project context.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project)
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')

        # get project info on a metadata context
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata)
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')

    def testInterationsInfo(self):

        self.loginAsPortalOwner()

        # preparing the dummy data.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        # preparing iteration.
        project.invokeFactory('PPMIteration', 'iter1')
        iteration1 = getattr(project, 'iter1')
        project.invokeFactory('PPMIteration', 'iter2')
        iteration2 = getattr(project, 'iter2')

        renderer = self.renderer(context=project)
        iterations = renderer.iterations()
        self.assertEquals(len(iterations), 2)
        self.assertEquals(iterations[0]['url'], iteration2.absolute_url())
        self.assertEquals(iterations[0]['title'], 'iter2')
        self.assertEquals(iterations[1]['url'], iteration1.absolute_url())
        self.assertEquals(iterations[1]['title'], 'iter1')

        renderer = self.renderer(context=metadata)
        iterations = renderer.iterations()
        self.assertEquals(len(iterations), 2)
        self.assertEquals(iterations[0]['url'], iteration2.absolute_url())
        self.assertEquals(iterations[0]['title'], 'iter2')
        self.assertEquals(iterations[1]['url'], iteration1.absolute_url())
        self.assertEquals(iterations[1]['title'], 'iter1')

    def testStoriesInfo(self):

        self.loginAsPortalOwner()

        # preparing the dummy data.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        # preparing stories
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        #self.portal.portal_catalog.indexObject(story1)
        project.invokeFactory('PPMStory', 'story2')
        story2 = getattr(project, 'story2')
        #self.portal.portal_catalog.indexObject(story2)
        project.invokeFactory('PPMStory', 'story3')
        story3 = getattr(project, 'story3')
        #self.portal.portal_catalog.indexObject(story3)

        renderer = self.renderer(context=project)
        stories = renderer.stories()
        self.assertEquals(len(stories), 3)
        self.assertEquals(stories[0]['url'], story3.absolute_url())
        self.assertEquals(stories[0]['title'], 'story3')
        self.assertEquals(stories[1]['url'], story2.absolute_url())
        self.assertEquals(stories[1]['title'], 'story2')
        self.assertEquals(stories[2]['url'], story1.absolute_url())
        self.assertEquals(stories[2]['title'], 'story1')

class TestRecentArtifactsPortlet(PlonepmTestCase):

    def testRenderer(self):

        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = recentArtifacts.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment),
                                   IPortletRenderer)
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, recentArtifacts.Renderer))

class TestRecentArtifactsRenderer(PlonepmTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):

        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = recentArtifacts.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def testArtifacts(self):

        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        project.invokeFactory('PPMFuncReq', 'funcReq1')
        funcReq1 = getattr(project, 'funcReq1')
        project.invokeFactory('PPMIteration', 'iter1')
        iter1 = getattr(project, 'iter1')
        project.invokeFactory('PPMSysReq', 'sysReq1')
        sysReq1 = getattr(project, 'sysReq1')

        renderer = self.renderer(context=project)
        artifacts = renderer.artifacts()
        self.assertEquals(len(artifacts), 4)
        self.assertEquals(artifacts[0]['url'], sysReq1.absolute_url())
        self.assertEquals(artifacts[0]['title'], 'sysReq1')
        self.assertEquals(artifacts[2]['url'], funcReq1.absolute_url())
        self.assertEquals(artifacts[2]['title'], 'funcReq1')

        renderer = self.renderer(context=story1)
        artifacts = renderer.artifacts()
        self.assertEquals(len(artifacts), 4)
        self.assertEquals(artifacts[1]['url'], iter1.absolute_url())
        self.assertEquals(artifacts[1]['title'], 'iter1')
        self.assertEquals(artifacts[3]['url'], story1.absolute_url())
        self.assertEquals(artifacts[3]['title'], 'story1')

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestProjectSimpleNavPortlet))
    suite.addTest(unittest.makeSuite(TestProjectSimpleNavRenderer))
    suite.addTest(unittest.makeSuite(TestRecentArtifactsPortlet))

    return suite
