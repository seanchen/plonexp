
# interfaces.py

"""
defines the marker interfaces for portlets. A portlet should implements
IPortletDataProvider
"""

from zope.schema import Text

from plone.portlets.interfaces import IPortletDataProvider

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the left navigation for homepage.
class IFrontNaviPortlet(IPortletDataProvider):

    """
    The front navigation bar only for the homepage.
    """

    navigationLinks = Text (
        title = u"Links for your navigation portlet",
        description = u"Please Select Navigation Links for Your Portlet",
        required = True
        )
