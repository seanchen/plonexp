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
        testing = config.product_config['testing']
        self.site_id = testing.get('id')

    # returns a list of product names
    def getNonInstallableProducts(self):

        app = getSiteManager().getPhysicalRoot()
        portal_props = getToolByName(app.UserAdmin, 'portal_properties')
        navtree_props = portal_props.navtree_properties
        props = navtree_props.getProperty('metaTypesNotToList')

        return ['iscorpio.zopelab.dove',
                'LDAPUserFolder', 'Products.LDAPUserFolder',
                'SimpleAttachment', 'Products.SimpleAttachment',
                'simplon.plone.ldap',
                'Marshall', 'Products.Marshall',
                'plone.app.openid',
                'NuPlone', 'Products.NuPlone']

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
