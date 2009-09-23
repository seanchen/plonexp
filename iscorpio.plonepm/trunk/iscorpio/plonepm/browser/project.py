
# project.py

"""
view adapter for project view.
"""

from Acquisition import aq_inner
from Products.Five.browser import BrowserView

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the default project View
class ProjectView(BrowserView):
    """
    the default view for a project.
    """

    # we need adapt Request too.
    def __init__(self, context, request):

        self.context = context
        self.request = request

    # return all metata data definition as a dict
    def getMetadata(self):

        context = aq_inner(self.context)
        return context.getMetadata()
