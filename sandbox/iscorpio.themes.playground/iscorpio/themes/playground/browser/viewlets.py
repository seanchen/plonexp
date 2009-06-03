from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class MyLogoViewlet(ViewletBase):

    render = ViewPageTemplateFile('templates/mylogo.pt')

    def update(self):

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.sitehome = portal_state.navigation_root_url()
