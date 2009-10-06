
# setuphandlers.py

"""
the various import handlers for iscoprio.plonepas.
"""

from StringIO import StringIO

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
