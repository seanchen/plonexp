
# utility.py

"""
some utilities for sites admin
"""

from App.config import getConfiguration
from zope.interface import implements
from zope.component import getSiteManager

from Products.CMFQuickInstallerTool.interfaces import INonInstallable

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# hide the profile from quicke installer.
class HiddenProducts(object):
    """
    This will be defined as an utility in zcml file, so it will be
    loaded when Zope Server start up.  You don't have to install
    this product in your Plone site.
    here are some list:
        NuPlone
        Products.NuPlone
        Marshall
        Products.Marshall
        LDAPUserFolder
        Products.LDAPUserFolder
        plone.app.openid
        simplon.plone.ldap
        SimpleAttachment
        Products.SimpleAttachment
    """

    implements(INonInstallable)

    def __init__(self):

        # this object will represent the configuration ites in
        # file zope.conf
        config = getConfiguration()
        try:
            # try the zope configuration file first, the configuration
            # should be something like this:
            # <product-config sites_admin>
            #   id UserAdmin
            # </product-config>
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

        try:
            site_props = adminSite.portal_properties.sitesadmin_properties
        except AttributeError:
            return []

        props = site_props.getProperty('productsNotToList')

        if props:
            return list(props)
        else:
            return []
