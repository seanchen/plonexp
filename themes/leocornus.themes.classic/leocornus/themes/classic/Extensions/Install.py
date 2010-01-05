
# Install.py

from Products.CMFCore.utils import getToolByName

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def uninstall(portal):
    """
    we are using generic setup profiles here.
    """

    setup_tool = getToolByName(portal, 'portal_setup')
    # execute the profiles defined in profiles.zcml
    setup_tool.runAllImportStepsFromProfile('profile-leocornus.themes.classic:uninstall')
    return "Ran all uninstall steps."
