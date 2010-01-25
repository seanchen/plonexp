
# base.py

"""
Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.
"""

from zope.component import getUtility
from zope.component import getMultiAdapter

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

#
# When ZopeTestCase configures Zope, it will *not* auto-load products in 
# Products/. Instead, we have to use a statement such as:
# 
#   ztc.installProduct('SimpleAttachment')
# 
# This does *not* apply to products in eggs and Python packages (i.e. not in
# the Products.*) namespace. For that, see below.
# 
# All of Plone's products are already set up by PloneTestCase.
# 

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    
    # Load the ZCML configuration for the iscorpio.plonerm package.
    # This can of course use <include /> to include other packages.
    
    fiveconfigure.debug_mode = True
    import leocornus.themes.classic
    zcml.load_config('configure.zcml', leocornus.themes.classic)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage() instead
    # of installProduct().
    # 
    # This is *only* necessary for packages outside the Products.* namespace
    # which are also declared as Zope 2 products, using 
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    # 
    #   ztc.installPackage('borg.localrole')
    # 
    ztc.installPackage('leocornus.themes.classic')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for this product. Then, we let PloneTestCase 
# set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['leocornus.themes.classic'])

class ClassicThemeTestCase(ptc.PloneTestCase):
    """
    We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

    portal_type = ""
    title = ""

class ClassicPortletTestCase(ClassicThemeTestCase):
    """
    base test case for testing leocornus classic Portlet.
    """

    def afterSetUp(self):

        self.loginAsPortalOwner()

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):

        if not assignment:
            raise AttributeError('assignment is required!')

        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

