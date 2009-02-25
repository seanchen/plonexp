"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from iscorpio.plonerm.tests.base import PlonermTestCase

from Products.CMFCore.utils import getToolByName

class TestCreation(PlonermTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        self.workflow = getToolByName(self.portal, 'portal_workflow')

    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """

    def testPortalTitle(self):
        
        # This is a simple test. The method needs to start with the name
        # 'test'. 

        # Look at the Python unittest documentation to learn more about hte
        # kinds of assertion methods which are available.

        # PloneTestCase has some methods and attributes to help with Plone.
        # Look at the PloneTestCase documentation, but briefly:
        # 
        #   - self.portal is the portal root
        #   - self.folder is the current user's folder
        #   - self.logout() "logs out" so that the user is Anonymous
        #   - self.setRoles(['Manager', 'Member']) adjusts the roles of the current user
        
        self.assertEquals("Plone site", self.portal.getProperty('title'))

    def testAddPRMResources(self):
        # create a resources by using the invokeFactory.
        new_id = self.folder.invokeFactory('PRMResources', 'my-page',
                                           prmUniqueSequence=102)
        # get the resources object.
        resources = getattr(self.folder, new_id)

        self.assertEquals('my-page', new_id)
        self.assertEquals(102, resources.prmUniqueSequence)

        nextSequence = resources.getNextUniqueId()
        self.assertEquals(103, resources.prmUniqueSequence)
        
    # Keep adding methods here, or break it into multiple classes or
    # multiple files as appropriate. Having tests in multiple files makes
    # it possible to run tests from just one package:
    #
    #   ./bin/instance test -s example.tests -t test_integration_unit


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreation))
    return suite
