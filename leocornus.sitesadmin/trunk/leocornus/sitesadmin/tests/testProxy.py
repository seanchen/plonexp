
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

        self.assertEquals(proxy.getProperty('userFolder'), 'Plone')
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

        self.loginAsPortalOwner()

        self.emptySite = getattr(self.app, 'site1')
        self.uf = self.emptySite.acl_users

    def testVerifyCredentials(self):

        # create a testing user in admin site's source_users.
        adminUserFolder = self.portal.acl_users
        adminUserFolder.source_users.addUser('srcUser', 'srcUser',
                                             'testpassword')

        # configure the proxy to include the source_users for
        # verifying the credentials.
        proxy = adminUserFolder.sitesadmin_proxy
        # so the user id with local prefix will be verified through
        # source_users
        proxy.manage_addProperty('local', 'source_users', 'string')

        theCred = {'login' : 'local\srcUser', 'password' : 'testpassword'}

        # assert that we could find the user from the admin site.
        # the authenticate method will return a PloneUser object.
        user = adminUserFolder.authenticate(theCred['login'],
                                            theCred['password'], None)
        self.failUnless(user)
        self.assertEquals('srcUser', user.getName())

        # set up the empty site for to testing it.
        userSetupTool = self.emptySite.portal_setup
        userSetupTool.runAllImportStepsFromProfile('profile-%s' %
                                                   'leocornus.sitesadmin:ssouser')

        # update the admin site's id.
        ssouser = self.uf.ssouser
        ssouser.manage_changeProperties(userSiteId=self.portal.id)

        credit = ssouser.authenticateCredentials(theCred)
        self.failUnless(credit)
        self.assertTrue('srcUser' in credit)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProxyBasicTestCase))
    suite.addTest(unittest.makeSuite(ProxyTestCase))
    return suite
