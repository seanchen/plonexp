
# storyFacts.py

"""
Story facts portlet will show the summary, iterations plan,
dependence storie, etc about a story.
"""

from zope.interface import implements
from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from interfaces import IStoryFactsPortlet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class Assignment(base.Assignment):
    """
    persist the properties for this portlet.
    """

    # implements the marker interface.
    implements(IStoryFactsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):

        return 'Story Facts'

class Renderer(base.Renderer):
    """
    returns all needs for render the portlet on page.
    """

    _template = ViewPageTemplateFile('storyFacts.pt')

    def __init__(self, *args):

        base.Renderer.__init__(self, *args)
        try:
            self.story = aq_inner(self.context).getStoryRoot()
        except AttributeError:
            self.story = None

    def render(self):

        return self._template()

    @property
    def available(self):
        """
        Only available for story and its contents
        """

        if not self.story:
            return False
        else:
            return True

    # Basic info for a story
    def storyInfo(self):
        """
        returns story title, url, hour usage, status, etc.
        """

        return {'url' : self.story.absolute_url(),
               }

# the form for add this portlet.
class AddForm(base.NullAddForm):

    def create(self):

        return Assignment()
