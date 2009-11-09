
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

# a portlet to list recent updates for this project.
class IRecentArtifactsPortlet(IPortletDataProvider):
    """
    the marker interface for a portlet to list recent changed artifacts.
    """
