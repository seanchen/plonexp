
# interfaces.py

"""
Define interfaces for browser views.
"""

from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewletManager
from zope.contentprovider.interfaces import ITALNamespaceData

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class IPlonepmTimesheet(IViewletManager):
    """
    Marker interface for the PlonePM timesheet viewlet manager
    """

# directly provides ... ???
directlyProvides(IPlonepmTimesheet, ITALNamespaceData)
