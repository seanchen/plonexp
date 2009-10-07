
# setuphandlers.py

"""
the various import handlers for iscoprio.plonepas.
"""

from StringIO import StringIO

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsUpdatePlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# triger the setup process.
def setupIscorpioPAS(context):
    """
    Setup iScorpio Plone PAS plugins
    """

    # skip if there is no flag file.
    if context.readDataFile('iscorpio.plonepas.txt') is None:
        return

    out = StringIO()
    site = context.getSite()
    setupIscorpioPlugins(site, out)

# install plugins and the basic setup.
def setupIscorpioPlugins(portal, out):
    """
    install plugin products and activate the plugins.
    """

    userFolder = portal.acl_users
    print >> out, "iScorpio Plugin Setup ..."

    # install the iscorpio.plonepas product to the user folder.
    iscorpio = userFolder.manage_addProduct['iscorpio.plonepas']

    # add the plugin if it's not exist.
    found = userFolder.objectIds(['iScorpio PlonePAS Squirrel Plugin'])
    if not found:
        iscorpio.manage_addSquirrelPlugins('squirrel')
        print >> out, "Added iScorpio PlonePAS Squirrel Plugin"

    # activate plugin interfaces for the specified plugins.
    activatePluginInterfaces(portal, 'squirrel', out)

    # deactivate other plugin interfaces' implementation.
    # suppose we are working on a Plone site with default acl_users setting.
    userFolder.plugins.deactivatePlugin(IAuthenticationPlugin, 'session')
    userFolder.plugins.deactivatePlugin(IAuthenticationPlugin, 'source_users')

    userFolder.plugins.deactivatePlugin(IUserEnumerationPlugin, 'source_users')

    userFolder.plugins.deactivatePlugin(IPropertiesPlugin, 'mutable_properties')

    userFolder.plugins.deactivatePlugin(IExtractionPlugin, 'session')
    userFolder.plugins.deactivatePlugin(IExtractionPlugin,
                                        'credentials_cookie_auth')
    userFolder.plugins.deactivatePlugin(IExtractionPlugin,
                                        'credentials_basic_auth')

    userFolder.plugins.deactivatePlugin(ICredentialsUpdatePlugin, 'session')
