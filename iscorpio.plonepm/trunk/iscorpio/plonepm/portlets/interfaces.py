
# interfaces.py

"""
defines the marker interfaces for portlets.  All portlet should implement
interface IPortletDataProvider.
"""

from plone.portlets.interfaces import IPortletDataProvider

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# This portlet is trying to provide a simple navigation for a project.
class IProjectSimpleNavPortlet(IPortletDataProvider):
    """
    The marker interface for project simple navigation portlet.
    """

    pass
