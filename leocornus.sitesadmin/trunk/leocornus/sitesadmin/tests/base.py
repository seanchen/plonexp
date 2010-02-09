
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

# 

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', leocornus.sitesadmin)

    ZopeTestCase.installPackage('leocornus.sitesadmin')

setup_product()
# we need a Plone site for some of the module.
PloneTestCase.setupPloneSite(products=['leocornus.sitesadmin'])

# base test case for our product.
class SitesAdminTestCase(PloneTestCase.PloneTestCase):
    """
    General steps for all test cases.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()

class SitesAdminFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """
    base test case class for functional test case.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
