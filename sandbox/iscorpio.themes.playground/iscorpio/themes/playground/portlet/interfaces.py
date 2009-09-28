
# interfaces.py

"""
defines the marker interfaces for portlets.  I portlet should
implements IPortletDataProvider.
"""

from plone.portlets.interfaces import IPortletDataProvider

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the simplest portlet.
class ISimplePortlet(IPortletDataProvider):

    pass
