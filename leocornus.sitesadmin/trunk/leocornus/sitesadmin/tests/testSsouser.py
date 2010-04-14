
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
from Products.PluggableAuthService.interfaces.plugins import ICredentialsResetPlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin

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

        found = plugins._getPlugins(ICredentialsResetPlugin)
        self.assertTrue(len(found) == 1)
        self.failUnless('ssouser' in found)
        self.failIf('credentials_cookie_auth' in found)
        self.failIf('session' in found)

        found = plugins._getPlugins(IChallengePlugin)
        self.assertTrue(len(found) == 1)
        self.failUnless('credentials_cookie_auth' in found)
        self.failIf('credentials_basic_auth' in found)
        self.failIf('ssouser' in found)
        self.failIf('session' in found)

    # test update the property.
    def testChangeProperty(self):

        self.setupSsoSite(self.emptySite, self.portal.id)

        self.uf.ssouser.manage_changeProperties(userSiteId='unit')
        self.failIfEqual('sites_admin', self.uf.ssouser.userSiteId)
        self.assertEquals('unit', self.uf.ssouser.userSiteId)

    # test authenticate credential
    def testAuthCredit(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        self.createMembraneTestUser(self.portal)

        # authenticate the testing user.
        credentials = {'login' : 'user1test',
                       'password' : 'user1password'}
        credit = self.uf.ssouser.authenticateCredentials(credentials)

        self.failIf(credit is None)
        self.assertTrue('user1test' in credit)

        # authenticate the testing user with upper case.
        credentials = {'login' : 'user1Test',
                       'password' : 'user1password'}
        credit = self.uf.ssouser.authenticateCredentials(credentials)

        self.failIf(credit is None)
        self.assertTrue('user1test' in credit)

    # test authenticate credential
    def testMutableProperty(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        user1 = self.createMembraneTestUser(self.portal)

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

        self.setupSsoSite(self.emptySite, self.portal.id)
        user1 = self.createMembraneTestUser(self.portal)
        user2 = self.createMembraneTestUser(self.portal, userId='user2',
                                       userName="user2test")

        userFolder = self.emptySite.acl_users

        self.failIf(len(userFolder.getUsers()) > 0)

        userFolder.portal_role_manager.assignRoleToPrincipal('Member', 'user1test')
        self.failUnless(len(userFolder.getUsers()) == 1)

        userFolder.portal_role_manager.assignRoleToPrincipal('Manager', 'user2test')
        self.failUnless(len(userFolder.getUsers()) == 2)

    def testEnumerateUsers(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        user1 = self.createMembraneTestUser(self.portal, userId='user1',
                                       userName='user1test',
                                       fullname='Full Name One')
        user2 = self.createMembraneTestUser(self.portal, userId='user2',
                                       userName="user2test",
                                       fullname='Full Name Two')
        user3 = self.createMembraneTestUser(self.portal, userId='user3',
                                       userName="user3test",
                                       fullname='Full Name Three')

        userFolder = self.emptySite.acl_users
        ssouser = userFolder.ssouser
        ssouser.manage_changeProperties(restrictSearch=True)
        roleManager = userFolder.portal_role_manager

        self.failIf(len(ssouser.enumerateUsers()) > 0)
        users = ssouser.enumerateUsers(fullname='one')
        self.failIf(len(users) > 0)

        roleManager.assignRoleToPrincipal('Member', 'user1test')
        self.failUnless(len(ssouser.enumerateUsers()) == 1)
        users = ssouser.enumerateUsers(fullname='one')
        self.failUnless(len(users) == 1)
        self.assertEquals(users[0]['id'], 'user1test')

        roleManager.assignRoleToPrincipal('Member', 'user2test')
        roleManager.assignRoleToPrincipal('Manager', 'user2test')
        self.failUnless(len(ssouser.enumerateUsers()) == 2)

    def testGetRolesForUser(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        user1 = self.createMembraneTestUser(self.portal, userId='user1',
                                       userName='user1test',
                                       fullname='Full Name One')

        userFolder = self.emptySite.acl_users
        ssouser = userFolder.ssouser
        roleManager = userFolder.portal_role_manager

        self.failIf(ssouser.getRolesForUser('user1test'))

        roleManager.assignRoleToPrincipal('Member', 'user1test')
        self.failUnless(ssouser.getRolesForUser('user1test'))

    def testRestrictSearch(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        user1 = self.createMembraneTestUser(self.portal, userId='user1',
                                       userName='user1test',
                                       fullname='Full Name One')
        user2 = self.createMembraneTestUser(self.portal, userId='user2',
                                       userName="user2test",
                                       fullname='Full Name Two')
        user3 = self.createMembraneTestUser(self.portal, userId='user3',
                                       userName="user3test",
                                       fullname='Full Name Three')

        userFolder = self.emptySite.acl_users
        ssouser = userFolder.ssouser
        roleManager = userFolder.portal_role_manager

        ssouser.manage_changeProperties(restrictSearch='False')
        self.failIf(ssouser.getProperty('restrictSearch'))

        self.assertEquals(len(userFolder.searchUsers(fullname='Full name')), 3)

        ssouser.manage_changeProperties(restrictSearch='True')
        self.failUnless(ssouser.getProperty('restrictSearch'))

        self.failIf(len(userFolder.searchUsers(fullname='Full name')) > 0)

        roleManager.assignRoleToPrincipal('Member', 'user1test')
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name')), 1)

        roleManager.assignRoleToPrincipal('Manager', 'user2test')
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name')), 2)

    def testMegaSearch(self):

        self.setupSsoSite(self.emptySite, self.portal.id)
        # creat user account in admin site.
        user1 = self.createMembraneTestUser(self.portal, userId='user1',
                                       userName='user1test',
                                       fullname='Full Name One')
        user2 = self.createMembraneTestUser(self.portal, userId='user2',
                                       userName="user2test",
                                       fullname='Full Name Two')
        user3 = self.createMembraneTestUser(self.portal, userId='user3',
                                       userName="user3test",
                                       fullname='Full Name Three')

        userFolder = self.emptySite.acl_users
        ssouser = userFolder.ssouser
        roleManager = userFolder.portal_role_manager

        ssouser.manage_changeProperties(restrictSearch='True')
        self.failUnless(ssouser.getProperty('restrictSearch'))

        self.assertEquals(len(userFolder.searchUsers(fullname='Full name')), 0)
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name',
                                                     sso_megasearch=True)),
                          3)
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name',
                                                     sso_megasearch=True,
                                                     sso_excludemember=True)),
                          3)

        roleManager.assignRoleToPrincipal('Manager', 'user2test')
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name')), 1)
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name',
                                                     sso_megasearch=True)),
                          3)
        self.assertEquals(len(userFolder.searchUsers(fullname='Full name',
                                                     sso_megasearch=True,
                                                     sso_excludemember=True)),
                          2)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SsouserTestCase))
    return suite
