
# header.py

"""
viewlets in portal header for the ygedf theme.
"""

from zope.component import getMultiAdapter

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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

class GlobalSectionsViewlet(ViewletBase):

    index = ViewPageTemplateFile('global.pt')

    def update(self):

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name=u'portal_tabs_view')
        selectedTabs = self.context.restrictedTraverse('selectedTabs')

        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)
        self.selected_tabs = selectedTabs('index_html', self.context, self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

class SiteActionsViewlet(ViewletBase):

    index = ViewPageTemplateFile('siteActions.pt')

    def update(self):

        super(SiteActionsViewlet, self).update()
