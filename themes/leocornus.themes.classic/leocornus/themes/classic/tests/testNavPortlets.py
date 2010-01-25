
# testNavPortlets.py

"""
Unit testing the portlets for navigation.
"""

import unittest

from leocornus.themes.classic.portlet import frontNavi

from base import ClassicPortletTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestNavigationPortlets(ClassicPortletTestCase):

    def testRenderer(self):

        links = "testing"

        renderer = self.renderer(context=self.folder,
                                 assignment=frontNavi.Assignment(links))
        self.failUnless(renderer.available)
        self.failUnless(isinstance(renderer, frontNavi.Renderer))

class TestFrontNavigationRenderer(ClassicPortletTestCase):

    def testLinks(self):

        inputs = "abc<>http://www.abc.com\ncde<>http://www.ncd.com\nefg<>/abc/nefg\n"

        renderer = self.renderer(context=self.folder,
                                 assignment=frontNavi.Assignment(inputs))
        links = renderer.items
        self.assertEquals(links[0]['title'], 'abc')
        self.assertEquals(links[1]['title'], 'cde')
        self.assertEquals(links[2]['title'], 'efg')

        self.assertEquals(links[0]['url'], 'http://www.abc.com')
        self.assertEquals(links[1]['url'], 'http://www.ncd.com')
        self.assertEquals(links[2]['url'],
                          self.portal.portal_url() + '/abc/nefg')

        inputs = ""
        renderer = self.renderer(context=self.folder,
                                 assignment=frontNavi.Assignment(inputs))
        self.assertEquals(len(renderer.items), 0)

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNavigationPortlets))
    suite.addTest(unittest.makeSuite(TestFrontNavigationRenderer))

    return suite


