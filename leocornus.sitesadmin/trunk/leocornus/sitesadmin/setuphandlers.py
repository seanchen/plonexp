
# setuphandlers.py

"""
miscellaneous set up steps that are not handled by GS import/export
handlers.
"""

from StringIO import StringIO

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from Products.CMFCore.utils import getToolByName

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def setupMembrane(context):
    """
    make sure we have membrane installed.
    """

    if context.readDataFile('sitesadmin-membrane-required.txt') is None:
        # 
        return

    portal = context.getSite()
    user_folder = getToolByName(portal, 'acl_users')
    # this is dirty check! we have better way...
    if 'membrane_users' not in user_folder.objectIds():
        installer = getToolByName(portal, 'portal_quickinstaller')
        # TODO: membrane version 1.1bx has a bit wired profile and version
        # 2.0 will fix it.
        installer.installProduct('membrane')

def setupProxyMultiPlugins(context):
    """
    install the Proxy Multi Plugins and activate the PAS services.
    """

    if context.readDataFile('sitesadmin-proxy-required.txt') is None:
        return

    out = StringIO()
    portal = context.getSite()
    userFolder = getToolByName(portal, 'acl_users')
    if 'sitesadmin_proxy' not in userFolder.objectIds():
        product = userFolder.manage_addProduct['leocornus.sitesadmin']
        product.manage_addProxyMultiPlugins('sitesadmin_proxy')
        print >> out, "Added SitesAdmin Proxy Mutli Plugins"

        # activate the plugin and
        activatePluginInterfaces(portal, 'sitesadmin_proxy', out)

        # the proxy plugin should be the last choice!
        plugins = userFolder.plugins
        plugins.movePluginsDown(IAuthenticationPlugin, ['sitesadmin_proxy'])
