
# project.py

# view adapter for project view.

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

# the default project View
class ProjectView(BrowserView):

    """ the default view for a project.
    """

    # we need adapt Request too.
    def __init__(self, context, request):

        self.context = context
        self.request = request

    # 
