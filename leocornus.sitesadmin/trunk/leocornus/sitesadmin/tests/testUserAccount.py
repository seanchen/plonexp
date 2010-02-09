
# testUserAccount.py

"""
unit test cases for new content type UserAccount
"""

import unittest

from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase

from leocornus.sitesadmin.content.user import UserAccount

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
