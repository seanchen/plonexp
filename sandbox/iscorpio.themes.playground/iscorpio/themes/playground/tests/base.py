
# base.py

"""
The basic and general staff for playgroun unit testing.
"""

import unittest

from Products.PloneTestCase import PloneTestCase as ptc

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

ptc.setupPloneSite()

class PlaygroundTestCase(ptc.PloneTestCase):
    """
    base for test cases.
    """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.manage_addFolder('portlets', 'Testing Portlets')
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % 'iscorpio.themes.playground:default')
