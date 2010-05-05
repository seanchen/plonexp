
# header.py

"""
viewlets in portal header for the Leocornus classic theme.
"""

from DateTime.DateTime import DateTime

from zope.component import getMultiAdapter

from Acquisition import aq_inner

from plone.memoize.instance import memoize

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class LogoViewlet(ViewletBase):

    index = ViewPageTemplateFile('logo.pt')

    def update(self):

        super(LogoViewlet, self).update()

        portal = self.portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName

        self.logo_tag = portal.restrictedTraverse(logoName).tag()
        self.navigation_root_url = self.portal_state.navigation_root_url()

class GlobalSectionViewlet(ViewletBase):

    index = ViewPageTemplateFile('global.pt')

    def update(self):

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.classic_site_actions = context_state.actions().get('classic_site_actions', None)

    @memoize
    def latestEvent(self):

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = 1
        # TODO: this should be configurable some where!
        state = 'published'
        return catalog(portal_type='Event',                                                            
                       review_state=state,
                       end={'query': DateTime(),                                                       
                            'range': 'min'},                                                           
                       sort_on='start',
                       sort_limit=limit)[:limit]
