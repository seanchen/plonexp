
# interfaces.py

"""
Marker interfaces for page, viewlet, theme, etc.
"""

from plone.theme.interfaces import IDefaultPloneLayer

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class IIscorpioThemesRedmaple(IDefaultPloneLayer):
  """
  Marker Interface that defines a Zope 3 skin layer bound to a skin
  selection in portal_skins.
  """
