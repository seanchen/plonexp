
# timesheet.py

"""
a timesheet to bill time to a story or an artifact
"""

from zope.interface import implements

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from interfaces import IPlonepmTimesheet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class AddForm(BrowserView):
    """
    The browser view for adding a form to collect billable time.
    """

    implements(IPlonepmTimesheet)

    def __init__(self, context, request, view):

        self.context = context
        self.request = request
        self.view = view

    def update(self):

        # do nothing for now.
        pass

    def render(self):

        # return the template defined in zcml.
        return self.template()

    def timesheetLog(self):

        obj = aq_inner(self.context)
        return obj.getTimesheetLog()

class BillTime(BrowserView):
    """
    This view is action view, which will perform some logic and reload
    the whole pae.
    """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        form = self.request.form
        # TODO: billable content may not just story,
        context = aq_inner(self.context)

        # get data from form.
        description = form.get('description', u'')
        duration = float(form.get('duration', -1))
        percentage = float(form.get('percentage', -1))

        # check invalid data!

        # adding the timesheet to the context.
        context.logTimesheet(description, duration, percentage)

        # re-index this context object.
        portal_catalog = getToolByName(self, 'portal_catalog')
        portal_catalog.indexObject(context)

        # redirect to current page.
        self.request.response.redirect(context.absolute_url())
