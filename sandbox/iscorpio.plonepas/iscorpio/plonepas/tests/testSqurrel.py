
# testSquirrel.py

"""
test cases for squirrel multi plugins.
"""

import unittest

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsUpdatePlugin

from base import IscorpioPASTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the test case class.
class SquirrelTestCase(IscorpioPASTestCase):

    # test add the plugin.
    def testAddSquirrel(self):

        iscorpio = self.acl_users.manage_addProduct['iscorpio.plonepas']
        iscorpio.manage_addSquirrelPlugins('squirrel')
        self.assertEquals(self.acl_users.\
                          objectIds(['iScorpio PlonePAS Squirrel Plugins']),
                          ['squirrel'])

    # test activate the plugins.
    def testActivateSquirrel(self):
        iscorpio = self.acl_users.manage_addProduct['iscorpio.plonepas']
        iscorpio.manage_addSquirrelPlugins('squirrel')

        plugins = self.acl_users.plugins

        plugins.activatePlugin(IAuthenticationPlugin, 'squirrel')
        found = plugins._getPlugins(IAuthenticationPlugin)
        self.assertTrue('squirrel' in found)

        plugins.activatePlugin(IUserEnumerationPlugin, 'squirrel')
        found = plugins._getPlugins(IUserEnumerationPlugin)
        self.assertTrue('squirrel' in found)

        plugins.activatePlugin(IPropertiesPlugin, 'squirrel')
        found = plugins._getPlugins(IPropertiesPlugin)
        self.assertTrue('squirrel' in found)

        plugins.activatePlugin(IExtractionPlugin, 'squirrel')
        found = plugins._getPlugins(IExtractionPlugin)
        self.assertTrue('squirrel' in found)

        plugins.activatePlugin(ICredentialsUpdatePlugin, 'squirrel')
        found = plugins._getPlugins(ICredentialsUpdatePlugin)
        self.assertTrue('squirrel' in found)

    # test the profile import.
    def testImportProfile(self):

        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'iscorpio.plonepas:default')

        # make sure it is installed.
        self.assertEquals(self.acl_users.\
                          objectIds(['iScorpio PlonePAS Squirrel Plugins']),
                          ['squirrel'])

        plugins = self.acl_users.plugins
        # make sure the plugins are activated.
        found = plugins._getPlugins(IAuthenticationPlugin)
        self.assertTrue('squirrel' in found)
        self.assertFalse('session' in found)
        self.assertFalse('source_users' in found)

        found = plugins._getPlugins(IUserEnumerationPlugin)
        self.assertTrue('squirrel' in found)
        self.assertFalse('source_users' in found)

        found = plugins._getPlugins(IPropertiesPlugin)
        self.assertTrue('squirrel' in found)
        self.assertFalse('mutable_properties' in found)

        found = plugins._getPlugins(IExtractionPlugin)
        self.assertTrue('squirrel' in found)
        self.assertFalse('session' in found)
        self.assertFalse('credentials_cookie_auth' in found)
        self.assertFalse('credentials_basic_auth' in found)

        found = plugins._getPlugins(ICredentialsUpdatePlugin)
        self.assertTrue('squirrel' in found)
        self.assertFalse('session' in found)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SquirrelTestCase))
    return suite
