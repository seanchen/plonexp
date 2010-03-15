
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

    def afterSetUp(self):

        self.loginAsPortalOwner()

        self.emptySite = getattr(self.app, 'site1')
        self.uf = self.emptySite.acl_users

    # test add the plugin.
    def testAddSsouser(self):

        sso = self.uf.manage_addProduct['leocornus.sitesadmin']
        sso.manage_addSsouserPlugins('ssouser')
        self.assertEquals(self.uf.\
                          objectIds([SsouserPlugins.meta_type]),
                          ['ssouser'])

    # test activate the plugins.
    def testActivateSsouser(self):
        sso = self.uf.manage_addProduct['leocornus.sitesadmin']
        sso.manage_addSsouserPlugins('ssouser')

        plugins = self.uf.plugins

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

        self.failUnless(IMutablePropertiesPlugin.providedBy(self.uf.ssouser))

    # test the profile import.
    def testImportProfile(self):

        setup_tool = getattr(self.emptySite, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        # make sure it is installed.
        self.assertEquals(self.uf.\
                          objectIds([SsouserPlugins.meta_type]),
                          ['ssouser'])

        plugins = self.uf.plugins
        # make sure the ssouser plugins are activated, and ssouser should be
        # the only active plugin.
        found = plugins._getPlugins(IAuthenticationPlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)
        self.assertFalse('source_users' in found)

        found = plugins._getPlugins(IUserEnumerationPlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('source_users' in found)
        self.assertFalse('mutable_properties' in found)

        found = plugins._getPlugins(IUserFactoryPlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('user_factory' in found)

        found = plugins._getPlugins(IPropertiesPlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('mutable_properties' in found)

        found = plugins._getPlugins(IExtractionPlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)
        self.assertFalse('credentials_cookie_auth' in found)
        self.assertFalse('credentials_basic_auth' in found)

        found = plugins._getPlugins(ICredentialsUpdatePlugin)
        self.assertTrue(len(found) == 1)
        self.assertTrue('ssouser' in found)
        self.assertFalse('session' in found)

    # test update the property.
    def testChangeProperty(self):

        # import the generic setup profile to install the ssouser plugin.
        setup_tool = getattr(self.emptySite, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        defaultSiteId = self.uf.ssouser.userSiteId
        self.assertEquals(defaultSiteId, 'sites_admin')

        self.uf.ssouser.manage_changeProperties(userSiteId='unit')
        self.failIfEqual(defaultSiteId, self.uf.ssouser.userSiteId)

    def prepareTestingSite(self, site):

        # install the ssouser plugin.
        setup_tool = getattr(site, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-%s' % \
                                                'leocornus.sitesadmin:ssouser')

        # using the testing plone site as the user admin site.
        site.acl_users.ssouser.manage_changeProperties(userSiteId=self.portal.id)

    def createTestingUser(self, site, userId='user1',
                          userName='user1test',
                          password='user1password',
                          location='user1 location'):

        # create testing user in the give site.
        site.invokeFactory('UserAccount', userId)
        user1 = getattr(self.portal, userId)
        user1.setUserName(userName)
        user1.setPassword(password)
        user1.setLocation(location)
        site.membrane_tool.indexObject(user1)

        return user1

    # test authenticate credential
    def testAuthCredit(self):

        self.prepareTestingSite(self.emptySite)
        self.createTestingUser(self.portal)

        # authenticate the testing user.
        credentials = {'login' : 'user1test',
                       'password' : 'user1password'}
        credit = self.uf.ssouser.authenticateCredentials(credentials)

        self.failIf(credit is None)
        self.assertTrue('user1test' in credit)

    # test authenticate credential
    def testMutableProperty(self):

        self.prepareTestingSite(self.emptySite)
        user1 = self.createTestingUser(self.portal)

        mtool = getToolByName(self.emptySite, 'portal_membership')
        member = mtool.getMemberById('user1test')
        self.failIf(member is None)
        self.assertEquals(member.getProperty('location'), user1.getLocation())

        newProps = {'location' : 'new location'}
        member.setMemberProperties(newProps)

        oneMore = mtool.getMemberById('user1test')
        self.assertEquals(oneMore.getProperty('location'), 'new location')
        self.assertEquals(user1.getLocation(), 'new location')

    def testGetUsers(self):

        self.prepareTestingSite(self.emptySite)
        user1 = self.createTestingUser(self.portal)
        user2 = self.createTestingUser(self.portal, userId='user2',
                                       userName="user2test")

        userFolder = self.emptySite.acl_users

        self.failIf(len(userFolder.getUsers()) > 0)

        userFolder.portal_role_manager.assignRoleToPrincipal('Member', 'user1test')
        self.failUnless(len(userFolder.getUsers()) == 1)

        userFolder.portal_role_manager.assignRoleToPrincipal('Manager', 'user2test')
        self.failUnless(len(userFolder.getUsers()) == 2)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SsouserTestCase))
    return suite
