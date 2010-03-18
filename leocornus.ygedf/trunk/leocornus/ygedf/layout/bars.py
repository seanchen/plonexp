
# bars.py

"""
viewlets in portal bars for the ygedf theme: personal_bar, language selector.
"""

from AccessControl import getSecurityManager
from Acquisition import aq_base

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class PersonalBarViewlet(BrowserView):

    implements(IViewlet)
    render = ViewPageTemplateFile('personalBar.pt')

    def __init__(self, context, request, view, manager):
        super(PersonalBarViewlet, self).__init__(context, request)

        self.__parent__ = view   
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

        self.tool = getToolByName(context, 'portal_languages', None)

    def update(self):

        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')

        sm = getSecurityManager()

        self.user_actions = context_state.actions().get('user', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:

            member = self.portal_state.member()
            userid = member.getId()

            if sm.checkPermission('Portlets: Manage own portlets', self.context):
                self.homelink_url = self.site_url + '/dashboard'
            else:
                if userid.startswith('http:') or userid.startswith('https:'):
                    self.homelink_url = self.site_url + '/author/?author=' + userid
                else:
                    self.homelink_url = self.site_url + '/author/' + quote_plus(userid)

            member_info = tools.membership().getMemberInfo(member.getId())
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid

    # for language selector.
    def available(self):
        if self.tool is not None:
            # Ask the language tool. Using getattr here for BBB with older
            # versions of the tool.
            showSelector = getattr(aq_base(self.tool), 'showSelector', None)
            if showSelector is not None:
                return self.tool.showSelector() # Call with aq context
            # BBB
            return bool(self.tool.use_cookie_negotiation)
        return False

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []

        bound = self.tool.getLanguageBindings()
        current = bound[0]

        def merge(lang, info):
            info["code"]=lang
            if lang == current:
                info['selected'] = True
            else:
                info['selected'] = False
            return info

        languages = [merge(lang, info) for (lang,info) in
                        self.tool.getAvailableLanguageInformation().items()
                        if info["selected"]]

        # sort supported languages by index in portal_languages tool
        supported_langs = self.tool.getSupportedLanguages()
        def index(info):
            try:
                return supported_langs.index(info["code"])
            except ValueError:
                return len(supported_langs)

        return sorted(languages, key=index)

    def showFlags(self):
        """Do we use flags?."""
        if self.tool is not None:
            return self.tool.showFlags()
        return False
