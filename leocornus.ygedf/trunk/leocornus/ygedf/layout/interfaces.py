
# interfaces.py

"""
Marker interfaces for page, viewlet, theme, etc.
"""

from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class IYGEDFTheme(IDefaultPloneLayer):
    """
    Marker Interface that defines a Zope 3 skin layer bound to a skin
    selection in portal_skins.
    """

class IYGEDFPortalHeader(IViewletManager):
    """
    A viewlet manager that sits above the content area
    """

class IYGEDFPortalFooter(IViewletManager):
    """
    viewlet manager for footer
    """
