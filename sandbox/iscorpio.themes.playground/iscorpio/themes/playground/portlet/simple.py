
# simple.py

"""
The most simple porlet for a plone site.
"""

import time

from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets.base import Assignment
from plone.app.portlets.portlets.base import Renderer
from plone.app.portlets.portlets.base import NullAddForm

from iscorpio.themes.playground.portlet.interfaces import ISimplePortlet

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the data for this simple portlet.
class SimpleAssignment(Assignment):
    """
    an assignment persist the data for a portlet.
    """

    implements(ISimplePortlet)

    def __init__(self):
        pass

    @property
    def title(self):

        return "Simple Portlet"

# the template for displaying the data.
class SimpleRenderer(Renderer):
    """
    The renderer will prepare the portlet HTML.
    """

    _template = ViewPageTemplateFile('simple.pt')

    def __init__(self, *args):

        Renderer.__init__(self, *args)

        context = aq_inner(self.context)

    def render(self):

        return self._template()

    @property
    def available(self):
        """
        this portlet is always available.
        """

        return True

    def words(self):

        return ['Hello World', 'Morning World']

    def time(self):

        return time.time()

#
class SimpleAddForm(NullAddForm):

    def create(self):

        return SimpleAssignment()
