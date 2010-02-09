
# useridprovider.py

"""
"""

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IUserRelated

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class UserIdProvider(object):
    """
    Adapts from UserAccount to IUserRelated.  Uses a massaged path to
    the member object instead of the UID.
    """
    implements(IUserRelated)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        purl = getToolByName(self.context, 'portal_url')
        rel_url = purl.getRelativeUrl(self.context)
        return rel_url.replace('/', '-')
