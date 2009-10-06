
# base.py

"""
setup Plone site for testing and the base test case for iscorpio.plonepas
"""

from Testing import ZopeTestCase

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

from Products.Five import zcml
from Products.Five import fiveconfigure

import iscorpio.plonepas

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

@onsetup
def setup_product():
    """
    we need install the product to Zope server, since our product is outside
    of Products.* namespace.
    """

    fiveconfigure.debug_mode = True
    # load the configure file, so Zope know this package.
    zcml.load_config('configure.zcml', iscorpio.plonepas)
    ZopeTestCase.installPackage('iscorpio.plonepas')

setup_product()
# setup a plone site
PloneTestCase.setupPloneSite()

# base test case class for iscorpio.plonepas
class IscorpioPASTestCase(PloneTestCase.PloneTestCase):
    """
    the base test case for testing iscorpio plone pas.
    """

    # we need the site owner's privilege to work with PAS plugins.
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.acl_users = self.portal.acl_users
