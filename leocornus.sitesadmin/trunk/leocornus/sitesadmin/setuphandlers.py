
# setuphandlers.py

"""
miscellaneous set up steps that are not handled by GS import/export
handlers.
"""

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
