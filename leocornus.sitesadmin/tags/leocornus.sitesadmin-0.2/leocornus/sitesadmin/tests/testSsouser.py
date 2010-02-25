
# testSsouser.py

"""
test cases for ssouser multi plugins.
"""

import unittest

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsUpdatePlugin

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin

from Products.CMFCore.utils import getToolByName

from leocornus.sitesadmin.plugins.ssouser import SsouserPlugins
from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the test case class.
class SsouserTestCase(SitesAdminTestCase):

    # test add the plugin.
    def testAddSsouser(self):

        sso = self.acl_users.manage_addProduct['leocornus.sitesadmin']
        sso.manage_addSsouserPlugins('ssouser')
        self.assertEquals(self.acl_users.\
                          objectIds([SsouserPlugins.meta_type]),
                          ['ssouser'])

    # test activate the plugins.
    def testActivateSsouser(self):
        sso = self.acl_users.manage_addProduct['leocornus.sitesadmin']
        sso.manage_addSsouserPlugins('ssouser')

        plugins = self.acl_users.plugins

        plugins.activatePlugin(IAuthenticationPlugin, 'ssouser')
        found = plugins._getPlugins(IAuthenticationPlugin)
        self.assertTrue('ssouser' in found)

        plugins.activatePlugin(IUserEnumerationPlugin, 'ssouser')
        found = plugins._getPlugins(IUserEnumerationPlugin)
        self.assertTrue('ssouser' in found)

        plugins.activatePlugin(IUserFactoryPlugin, 'ssouser')
        found = plugins._getPlugins(IUserFactoryPlugin)
        self.assertTrue('ssouser' in found)

        plugins.activatePlugin(IPropertiesPlugin, 'ssouser')
        found = plugins._getPlugins(IPropertiesPlugin)
        self.assertTrue('ssouser' in found)

        plugins.activatePlugin(IExtractionPlugin, 'ssouser')
        found = plugins._getPlugins(IExtractionPlugin)
        self.assertTrue('ssouser' in found)

        plugins.activatePlugin(ICredentialsUpdatePlugin, 'ssouser')
        found = plugins._getPlugins(ICredentialsUpdatePlugin)
        self.assertTrue('ssouser' in found)

        IMutablePropertiesPlugin.providedBy(self.acl_users.ssouser)

    # test the profile import.
    def testImportProfile(self):

        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        # make sure it is installed.
        self.assertEquals(self.acl_users.\
                          objectIds([SsouserPlugins.meta_type]),
                          ['ssouser'])

        plugins = self.acl_users.plugins
        # make sure the ssouser plugins are activated, and ssouser should be
        # the only active plugin.
        found = plugins._getPlugins(IAuthenticationPlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)
        self.assertFalse('source_users' in found)

        found = plugins._getPlugins(IUserEnumerationPlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('source_users' in found)

        found = plugins._getPlugins(IUserFactoryPlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('user_factory' in found)

        found = plugins._getPlugins(IPropertiesPlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('mutable_properties' in found)

        found = plugins._getPlugins(IExtractionPlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)
        self.assertFalse('credentials_cookie_auth' in found)
        self.assertFalse('credentials_basic_auth' in found)

        found = plugins._getPlugins(ICredentialsUpdatePlugin)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)

    # test update the property.
    def testChangeProperty(self):

        # import the generic setup profile to install the ssouser plugin.
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        defaultSiteId = self.acl_users.ssouser.userSiteId
        self.assertEquals(defaultSiteId, 'sites_admin')

        self.acl_users.ssouser.manage_changeProperties(userSiteId='unit')
        self.failIfEqual(defaultSiteId, self.acl_users.ssouser.userSiteId)

    # test authenticate credential
    def testAuthCredit(self):

        # install the ssouser plugin.
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        # preparing testing user.
        self.portal.invokeFactory('UserAccount', 'user1')
        user1 = getattr(self.portal, 'user1')
        user1.setUserName("user1test")
        user1.setPassword('user1password')
        self.portal.membrane_tool.indexObject(user1)

        # authenticate the testing user.
        credentials = {'login' : 'user1test',
                       'password' : 'user1password'}
        # using the testing plone site as the user admin site.
        self.acl_users.ssouser.manage_changeProperties(userSiteId='plone')
        credit = self.acl_users.ssouser.authenticateCredentials(credentials)

        self.failIf(credit is None)
        self.assertTrue('user1test' in credit)

    # test authenticate credential
    def testMutableProperty(self):

        # install the ssouser plugin.
        setup_tool = getattr(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        # deactivate all the plugins from membrane.
        membranePlugins = {
            'membrane_properties' : [IPropertiesPlugin],
            'membrane_user_factory' : [IUserFactoryPlugin],
            'membrane_users' : [IAuthenticationPlugin, IUserEnumerationPlugin],
            }
        self.acl_users.plugins.deactivatePlugin(IAuthenticationPlugin,
                                                'membrane_users')
        self.acl_users.plugins.deactivatePlugin(IUserEnumerationPlugin,
                                                'membrane_users')
        self.acl_users.plugins.deactivatePlugin(IPropertiesPlugin,
                                                'membrane_properties')
        self.acl_users.plugins.deactivatePlugin(IUserFactoryPlugin,
                                                'membrane_user_factory')
        # at this point, ssouer should be the only active plugin.

        # preparing testing user.
        self.portal.invokeFactory('UserAccount', 'user1')
        user1 = getattr(self.portal, 'user1')
        user1.setUserName("user1test")
        user1.setPassword('user1password')
        user1.setLocation('user1 location')
        self.portal.membrane_tool.indexObject(user1)

        # using the testing plone site as the user admin site.
        self.acl_users.ssouser.manage_changeProperties(userSiteId='plone')

        mtool = getToolByName(self.portal, 'portal_membership')
        member = mtool.getMemberById('user1test')
        self.failIf(member is None)
        self.assertEquals(member.getProperty('location'), user1.getLocation())

        newProps = {'location' : 'new location'}
        member.setMemberProperties(newProps)

        oneMore = mtool.getMemberById('user1test')
        self.assertEquals(oneMore.getProperty('location'), 'new location')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SsouserTestCase))
    return suite
