# nest.py

"""
a simple Zope product trying to use GenericSetup to do some initialization
work.
"""

from App.config import getConfiguration
from OFS.Folder import Folder
from Globals import InitializeClass
from zope.interface import implements
from zope.component import getSiteManager

from Products.CMFCore.utils import getToolByName
from Products.CMFQuickInstallerTool.interfaces import INonInstallable

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# hide the profile from quicke installer.
class HiddenProducts(object):

    implements(INonInstallable)

    def __init__(self):

        config = getConfiguration()
        try:
            # try the zope configuration file first.
            sitesAdmin = config.product_config['sites_admin']
            self.adminSiteId = sitesAdmin.get('id')
        except KeyError:
            # using the default site id.
            self.adminSiteId = 'sites_admin'

    # returns a list of product names
    def getNonInstallableProducts(self):

        app = getSiteManager().getPhysicalRoot()
        try:
            # trying to looking for the admin site!
            adminSite = getattr(app, self.adminSiteId)
        except AttributeError:
            # no admin site return a empty list.
            return []

        # using the site_properties for now, we may create a dedicate one
        # later.
        site_props = adminSite.portal_properties.site_properties
        props = site_props.getProperty('productsNotList')

        if props:
            return list(props)
        else:
            return []

# CMFDove product class. Extends from SimpleItem to get some basic
# behavior for work with ZMI
class CMFDove(Folder):
    """
    A simple Zope product leverage on GenericSetup.
    """

    # specify the meta type to show up on the add drop down for a Zope
    # instance.
    meta_type = "iScorpio ZopeLab Dove"

    # __init__
    def __init__(self, id, title=''):
        """
        the initialization.
        """

        self.id = id
        self.title = title

    # the default home page for this produce.
    def index_html(self):
        """
        Just try to say something here.
        """

        return """<html><body>Welcome to %s</body></html>
        """ % self.title

InitializeClass(CMFDove)
