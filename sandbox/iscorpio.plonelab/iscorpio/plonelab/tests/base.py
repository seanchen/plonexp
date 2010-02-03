
# base.py

"""
The base unit test cases for plonelab package.
"""

from Testing import ZopeTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

import iscorpio.plonelab

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# 

@onsetup
def setup_product():
    """
    we need install our product so the testing zope server know it.
    """

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', iscorpio.plonelab)
    ZopeTestCase.installPackage('iscorpio.plonelab')

setup_product()
# we need a Plone site for some of the module.
PloneTestCase.setupPloneSite()

# base test case for our product.
class IscorpioPlonelabTestCase(PloneTestCase.PloneTestCase):
    """
    General steps for all test cases.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()
