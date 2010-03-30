
# base.py

"""
The base unit test cases for sites admin
"""

from Testing import ZopeTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

import leocornus.sitesadmin

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', leocornus.sitesadmin)

    # we need use installProduct instead of installPackage for membrane
    # version 1.1bx.  version 2.0 will be different.
    ZopeTestCase.installProduct('membrane')
    ZopeTestCase.installPackage('leocornus.sitesadmin')

setup_product()
# we need a Plone site for some of the module.
PloneTestCase.setupPloneSite(products=['leocornus.sitesadmin'],
                             extension_profiles=["membrane:default"])

# try to setup one more plone site for testing.
PloneTestCase.setupPloneSite(id='site1')

# base test case for our product.
class SitesAdminTestCase(PloneTestCase.PloneTestCase):
    """
    General steps for all test cases.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
        self.acl_users = self.portal.acl_users

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

    def createMembraneTestUser(self, site, userId='user1',
                               userName='user1test',
                               password='user1password',
                               fullname="Full Name",
                               email="email@mail.com",
                               location='user1 location'):

        # create testing user in the give site.
        site.invokeFactory('UserAccount', userId)
        user1 = getattr(self.portal, userId)
        user1.setUserName(userName)
        user1.setPassword(password)
        user1.setFullname(fullname)
        user1.setEmail(email)
        user1.setLocation(location)
        site.membrane_tool.indexObject(user1)

        return user1

class SitesAdminFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """
    base test case class for functional test case.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
