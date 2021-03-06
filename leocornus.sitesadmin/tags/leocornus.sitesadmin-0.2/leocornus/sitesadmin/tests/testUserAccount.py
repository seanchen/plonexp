
# testUserAccount.py

"""
unit test cases for new content type UserAccount
"""

import unittest

from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase

from Products.CMFCore.utils import getToolByName

from leocornus.sitesadmin.content.user import UserAccount
from base import SitesAdminTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# test cases list
tests = []

class UserAccountBasicTest(ATCTTypeTestCase):

    klass = UserAccount
    portal_type = 'UserAccount'
    title = 'User Account'
    meta_type = 'UserAccount'
    icon = 'user.gif'

tests.append(UserAccountBasicTest)

class UserAccountTest(SitesAdminTestCase):
    """
    testing the membrane user account.
    """

    def testCreateUser(self):

        self.portal.invokeFactory('UserAccount', 'user1')
        user1 = getattr(self.portal, 'user1')
        user1.setUserName("user1test")
        user1.setFullname("User Full Name")
        user1.setPassword('user1password')
        user1.setLocation('a location')
        user1.setEmail('sean.chen@ontario.ca')
        sites = ("{'id':'gsdc/sso_test', 'roles':['Member','Reviewer'], 'groups':['testing','contributor']}",
                 "{'id':'gsdc/cts', 'roles':['Reviewer'], 'groups':['contributor']}")
        user1.setSites(sites)
        self.portal.membrane_tool.indexObject(user1)

        credentials = {'login' : 'user1test',
                       'password' : 'user1password'}
        credit = self.portal.acl_users.membrane_users.authenticateCredentials(credentials)
        self.failIf(credit is None)
        self.assertTrue('user1test' in credit)

        # testing the membership info.
        mTool = getToolByName(self.portal, 'portal_membership')
        theMember = mTool.getMemberById('user1test')
        self.assertEquals('User Full Name', theMember.getProperty('fullname'))
        self.assertEquals('sean.chen@ontario.ca', theMember.getProperty('email'))
        self.assertEquals('a location', theMember.getProperty('location'))
        self.assertEquals(sites, theMember.getProperty("sites"))

tests.append(UserAccountTest)

# making test suite.
def test_suite():
    """
    This sets up a test suite that actually runs the tests in the class
    above
    """

    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    return suite
