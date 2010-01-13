
# frontNavi.py

"""
a simple navigation portlet for front page only, which
just has some links.
"""

from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from leocornus.themes.classic.portlet.interfaces import IFrontNaviPortlet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the data for this simple navigration.
class Assignment(base.Assignment):
    """
    an assignment persist the data for a portlet.
    """

    implements(IFrontNaviPortlet)

    def __init__(self):
        pass

    @property
    def title(self):

        return "Front Page Navigation"

# the template for displaying the data.
class Renderer(base.Renderer):
    """
    The renderer will prepare the portlet HTML.
    """

    _template = ViewPageTemplateFile('frontNavi.pt')

    def __init__(self, *args):

        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)

    def render(self):

        return self._template()

    @property
    def available(self):
        """
        this portlet is always available.
        """

        return True

#
class AddForm(base.NullAddForm):

    def create(self):

        return Assignment()
