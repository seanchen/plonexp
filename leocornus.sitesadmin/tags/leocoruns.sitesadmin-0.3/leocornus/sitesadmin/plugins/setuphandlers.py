
# setuphandlers.py

"""
the various import handlers for sitesadmin single sign on plugin.
"""

from StringIO import StringIO

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsUpdatePlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from ssouser import SsouserPlugins

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# triger the setup process.
def setupSsouser(context):
    """
    Setup sitesadmin single sign on plugin.
    """

    # skip if there is no flag file.
    if context.readDataFile('sitesadmin.ssouser.setup.txt') is None:
        return

    out = StringIO()
    site = context.getSite()
    setupSsouserPlugins(site, out)

# install plugins and the basic setup.
def setupSsouserPlugins(portal, out):
    """
    install plugin products and activate the plugins.
    """

    userFolder = portal.acl_users
    print >> out, "sitesadmin single sign on Plugin Setup ..."

    # add the plugin if it's not exist.
    found = userFolder.objectIds([SsouserPlugins.meta_type])
    if not found:
        sso = userFolder.manage_addProduct['leocornus.sitesadmin']
        sso.manage_addSsouserPlugins('ssouser')
        print >> out, "Added sitesadmin single sign on user Plugin"

    # activate plugin interfaces for the specified plugins.
    activatePluginInterfaces(portal, 'ssouser', out)

    # deactivate other plugin interfaces' implementation.
    # suppose we are working on a Plone site with default acl_users setting.
    userFolder.plugins.deactivatePlugin(IAuthenticationPlugin, 'session')
    userFolder.plugins.deactivatePlugin(IAuthenticationPlugin, 'source_users')

    userFolder.plugins.deactivatePlugin(IUserEnumerationPlugin, 'source_users')
    userFolder.plugins.deactivatePlugin(IUserEnumerationPlugin, 'mutable_properties')
    userFolder.plugins.deactivatePlugin(IUserFactoryPlugin, 'user_factory')

    userFolder.plugins.deactivatePlugin(IPropertiesPlugin, 'mutable_properties')

    userFolder.plugins.deactivatePlugin(IExtractionPlugin, 'session')
    userFolder.plugins.deactivatePlugin(IExtractionPlugin,
                                        'credentials_cookie_auth')
    userFolder.plugins.deactivatePlugin(IExtractionPlugin,
                                        'credentials_basic_auth')

    userFolder.plugins.deactivatePlugin(ICredentialsUpdatePlugin, 'session')
