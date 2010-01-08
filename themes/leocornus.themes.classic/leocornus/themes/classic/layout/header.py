
# header.py

"""
viewlets in portal header for the Leocornus classic theme.
"""

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

class GlobalSectionViewlet(ViewletBase):

    index = ViewPageTemplateFile('global.pt')

    def update(self):

        super(GlobalSectionViewlet, self).update()
