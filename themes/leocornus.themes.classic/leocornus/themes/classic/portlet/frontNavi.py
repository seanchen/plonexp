
# frontNavi.py

"""
a simple navigation portlet for front page only, which
just has some links.
"""

from zope.interface import implements
from zope.formlib import form

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from leocornus.themes.classic.portlet.interfaces import IFrontNaviPortlet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the separator between url and description.
TITLE_URL = '<>'

# the data for this simple navigration.
class Assignment(base.Assignment):
    """
    an assignment persist the data for a portlet.
    """

    implements(IFrontNaviPortlet)

    def __init__(self, navigationLinks):

        self.navigationLinks = navigationLinks

    @property
    def title(self):

        return "Front Page Navigation"

# the template for displaying the data.
class Renderer(base.Renderer):
    """
    The renderer will prepare the portlet HTML.
    The attribute self.data will be the wrapper class to access the
    attributes in assignment.
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

    @property
    def items(self):

        context = aq_inner(self.context)
        # self.data is wrapper to the Assignment
        # one line for each item, so we split by new line here.
        links = self.data.navigationLinks.splitlines()

        items = []
        for link in links:
            titleUrl = link.split(TITLE_URL)
            if not titleUrl[1].startswith('http'):
                titleUrl[1] = context.portal_url() + titleUrl[1]
            item = {'title' : titleUrl[0],
                    'url' : titleUrl[1]
                    }
            items.append(item)

        return items

#
class AddForm(base.AddForm):

    """
    the add form for the navigation portlet, The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IFrontNaviPortlet)

    label = u"Add Classic Navigation Portlet"
    description = u"Links specified here will show in Navigation portlet."

    def create(self, data):

        return Assignment(**data)

class EditForm(base.EditForm):

    """
    
    """

    form_fields = form.Fields(IFrontNaviPortlet)

    label = u"Edit Classic Navigation Portlet"
    description = u"Links specified here will show in Navigation portlet."
