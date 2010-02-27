
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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProxyBasicTestCase))
    return suite
