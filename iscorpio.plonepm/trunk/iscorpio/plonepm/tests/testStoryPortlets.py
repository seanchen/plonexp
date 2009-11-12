
# testStoryPortlets.py

"""
testing the portlets for PPMStory
"""

import unittest

from iscorpio.plonepm.portlets import storyFacts

from base import PlonepmPortletTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestStoryPortlets(PlonepmPortletTestCase):

    def testRenderer(self):

        renderer = self.renderer(context=self.folder,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, storyFacts.Renderer))

class TestStoryFactsRenderer(PlonepmPortletTestCase):

    def testAvailable(self):

        # renderer in root should not available
        renderer = self.renderer(assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a story
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        renderer = self.renderer(context=story1,
                                 assignment=storyFacts.Assignment())
        self.failUnless(renderer.available)

        # renderer in a story response

    def testStoryInfo(self):

        self.portal.invokeFactory('PPMProject', 'project1')
        project1 = getattr(self.portal, 'project1')

        project1.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project1, 'story1')
        renderer = self.renderer(context=story1,
                                 assignment=storyFacts.Assignment())
        info = renderer.storyInfo()
        self.assertEquals(info['url'], story1.absolute_url())

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStoryPortlets))
    suite.addTest(unittest.makeSuite(TestStoryFactsRenderer))

    return suite
