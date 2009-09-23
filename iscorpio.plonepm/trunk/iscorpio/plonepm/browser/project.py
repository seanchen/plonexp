
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

    # returns the whole estimated hour for this project.
    def getProjectEstimatedHours(self):
        """
        returns the amount of hours estimated for this project.
        """

        context = aq_inner(self.context)
        stories = context.getAllStories()
        hours = 0
        for story in stories:
            hours = hours + \
                    story.getObject().xppm_story_estimated_hours

        return hours

    # progress percent
    def getProjectProgressPercent(self):
        """
        returns the progress status as a percentage for this project. 
        """

        context = aq_inner(self.context)
        stories = context.getAllStories()
        progressPercent = 0
        if len(stories) > 0:
            progress = 0
            for story in stories:
                progress = progress + \
                           story.getObject().xppm_story_progress_percent

            progressPercent = progress / len(stories)

        return progressPercent
