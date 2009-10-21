
# base.py

"""
The base unit test cases for zopelab package.
"""

from Testing import ZopeTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

import iscorpio.zopelab

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# 

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', iscorpio.zopelab)
    ZopeTestCase.installPackage('iscorpio.zopelab')

setup_product()
# we need a Plone site for some of the module.
PloneTestCase.setupPloneSite()

# base test case for our product.
class IscorpioZopelabTestCase(PloneTestCase.PloneTestCase):
    """
    General steps for all test cases.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
