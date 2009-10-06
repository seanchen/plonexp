
# testSquirrel.py

"""
test cases for squirrel multi plugins.
"""

import unittest

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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SquirrelTestCase))
    return suite
