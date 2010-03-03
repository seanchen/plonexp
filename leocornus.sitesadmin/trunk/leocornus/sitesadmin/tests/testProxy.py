
# testProxy.py

"""
testing the proxy multiple plugin
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

from leocornus.sitesadmin.plugins.proxy import ProxyMultiPlugins
from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the test case class.
class ProxyBasicTestCase(SitesAdminTestCase):

    def afterSetUp(self):

        self.loginAsPortalOwner()

        self.emptySite = getattr(self.app, 'site1')
        self.uf = self.emptySite.acl_users

    def testAddProxyPlugin(self):

        # proxy should be installed when we install the site admin product.
        # verify here.
        product = self.uf.manage_addProduct['leocornus.sitesadmin']
        product.manage_addProxyMultiPlugins('proxy')

        ufId = self.uf.objectIds([ProxyMultiPlugins.meta_type])
        self.assertEquals(ufId, ['proxy'])

        # testing write and read properties from the plugin.
        proxy = getattr(self.uf, 'proxy')
        proxy.manage_addProperty('abc', '123', 'string')
        proxy.manage_addProperty('bcd', '234', 'string')
        self.assertEquals(proxy.getProperty('abc'), '123')
        self.assertEquals(proxy.getProperty('bcd'), '234')

        self.assertEquals(proxy.getProperty('userFolder'), 'plone')
        proxy.manage_changeProperties(userFolder='another/site')
        self.assertEquals(proxy.getProperty('userFolder'), 'another/site')

# testing proxy multi plugins in more complex cases.
class ProxyTestCase(SitesAdminTestCase):

    # we well use source_users plugin to prepare the testing user.
    # 1. create some users in Plone site's source_users
    # 2. testing in Plone site to login by using these users
    # 3. testing in an empty site with ssouser plugin for these
    #    users.
    # 4. it should create a UserAccount in membrane automatically.

    def afterSetUp(self):

        #self.loginAsPortalOwner()

        self.emptySite = getattr(self.app, 'site1')
        self.uf = self.emptySite.acl_users

    def createDefaultPloneTestUser(self, aclUsers,
                                   userId='testuser',
                                   loginName='testuser',
                                   password='password',
                                   fullname='Full Name',
                                   email='full.name@mail.com',
                                   location='Home'):
        """
        create a test user by using the default plone pas services:
        source_users, user_factory, mutable_properties.
        """

        aclUsers.source_users.addUser(userId, loginName, password)
        testUser = aclUsers.user_factory.createUser(userId, loginName)

        propPlugin = aclUsers.mutable_properties
        testUserPropSheet = propPlugin.getPropertiesForUser(testUser)
        testUserPropSheet.setProperties(testUser,
                                        {'fullname' : fullname,
                                         'email' : email,
                                         'location' : location,
                                        })
        propPlugin.setPropertiesForUser(testUser, testUserPropSheet)

    def setupTestingProxy(self, aclUsers):

        # configure the proxy to include the source_users for
        # verifying the credentials.
        proxy = aclUsers.sitesadmin_proxy
        proxy.manage_changeProperties(userFolder=self.portal.id)
        # so the user id with local prefix will be verified through
        # source_users
        proxy.manage_addProperty('local', 'source_users', 'string')
        proxy.manage_addProperty('local_prop', 'mutable_properties', 'string')
        proxy.manage_addProperty('local_factory', 'user_factory', 'string')

    def setupRemoteSite(self, remoteSite):

        # set up the empty site for to testing it.
        userSetupTool = remoteSite.portal_setup
        userSetupTool.runAllImportStepsFromProfile('profile-%s' %
                                                   'leocornus.sitesadmin:ssouser')

        # update the admin site's id.
        ssouser = remoteSite.acl_users.ssouser
        ssouser.manage_changeProperties(userSiteId=self.portal.id)

        return ssouser

    def testVerifyCredentials(self):

        # create a testing user in admin site's source_users.
        adminUserFolder = self.portal.acl_users
        self.createDefaultPloneTestUser(adminUserFolder, 'srcUser',
                                        'srcUser', 'testpassword')

        self.setupTestingProxy(adminUserFolder)

        theCred = {'login' : 'local\\srcUser', 'password' : 'testpassword'}

        # assert that we could find the user from the admin site.
        # the authenticate method will return a PloneUser object.
        user = adminUserFolder.authenticate(theCred['login'],
                                            theCred['password'], None)
        self.failUnless(user)
        self.assertEquals('local\\srcUser', user.getName())

        ssouser = self.setupRemoteSite(self.emptySite)
        credit = ssouser.authenticateCredentials(theCred)
        self.failUnless(credit)
        self.assertTrue('local\\srcUser' in credit)

    def testCreateUserLocal(self):

        # create a testing user in admin site's source_users.
        adminUserFolder = self.portal.acl_users
        fullName='test user full name'
        eMail='test.user@testing.com'
        self.createDefaultPloneTestUser(adminUserFolder,
                                        'testuser',
                                        'testuser',
                                        'testpassword',
                                        fullName,
                                        eMail)

        self.setupTestingProxy(adminUserFolder)

        theCred = {'login' : 'local\\testuser', 'password' : 'testpassword'}

        user = adminUserFolder.authenticate(theCred['login'],
                                            theCred['password'], None)
        self.failUnless(user)
        self.assertEquals('local\\testuser', user.getName())
        self.assertEquals(fullName, user.getProperty('fullname'))
        self.assertEquals(eMail, user.getProperty('email'))

        # get back the user from membership tool.
        mtool = getToolByName(self.portal, 'portal_membership')
        getBack = mtool.getMemberById('local\\testuser')
        self.assertEquals(getBack.getProperty('fullname'), fullName)
        self.assertEquals(getBack.getProperty('email'), eMail)

        # get back the user from membrane user folder.
        membraneUser = getattr(self.portal, 'local-testuser')
        self.assertEquals(membraneUser.getFullname(), fullName)
        self.assertEquals(membraneUser.getEmail(), eMail)

    def testCreateUserRemote(self):

        # create a testing user in admin site's source_users.
        adminUserFolder = self.portal.acl_users
        fullName='test user from remote'
        eMail='test.remote@testing.com'
        self.createDefaultPloneTestUser(adminUserFolder,
                                        'testremote',
                                        'testremote',
                                        'testpassword',
                                        fullName,
                                        eMail)

        self.setupTestingProxy(adminUserFolder)

        theCred = {'login' : 'local\\testremote', 'password' : 'testpassword'}

        self.setupRemoteSite(self.emptySite)
        remoteUserFolder = self.uf

        user = remoteUserFolder.authenticate(theCred['login'],
                                             theCred['password'], None)
        self.failUnless(user)
        self.assertEquals('local\\testremote', user.getName())
        self.assertEquals(fullName, user.getProperty('fullname'))
        self.assertEquals(eMail, user.getProperty('email'))

        # get back the user from membership tool.
        mtool = getToolByName(self.emptySite, 'portal_membership')
        getBack = mtool.getMemberById('local\\testremote')
        self.assertEquals(getBack.getProperty('fullname'), fullName)
        self.assertEquals(getBack.getProperty('email'), eMail)

        # get back the user from membrane user folder.
        membraneUser = getattr(self.portal, 'local-testremote')
        self.assertEquals(membraneUser.getFullname(), fullName)
        self.assertEquals(membraneUser.getEmail(), eMail)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProxyBasicTestCase))
    suite.addTest(unittest.makeSuite(ProxyTestCase))
    return suite
