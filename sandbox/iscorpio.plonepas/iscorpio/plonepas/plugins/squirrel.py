# squirrel.py

"""
A simple and small PAS plugin. Give it name squirrel means small but
full function.
"""

import logging

from Acquisition import aq_inner, aq_parent

from Globals import InitializeClass
from Globals import DTMLFile
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsUpdatePlugin

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the form to add a squirrel plugin.
manage_addSquirrelPluginsForm = DTMLFile('../zmi/squirrelAdd', globals())

# the factory method to add a squirrel pluginb.
def manage_addSquirrelPlugins(self, id, title='', userSiteId='Plone', REQUEST=None):
    """
    Id and title will come with the HTTP request.
    """

    sp = SquirrelPlugins(id, title, userSiteId)
    self._setObject(sp.getId(), sp)

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
                                     '?manage_tags_message=iScoprio+PlonePAS+Squirrel+Plugins+Added' %
                                     self.absolute_url())

class SquirrelPlugins(BasePlugin):
    """
    a small and full function PAS plugin.
    We are trying to forward all request to an admin product under Zope root.
    Typically the following request:
    - IAuthenticationPlugin.authenticateCredentials
    - IUserEnumerationPlugin.enumerateUsers
    If we are using cookie to save the credentials, we don't have to forward
    the IExtractionPlugin and ICredentialsUpdatePlugin.  We can easily make
    all sites to use the same cookie name, so all sites will extract and
    update the same cookie.
    """

    log = logging.getLogger("Squirrel Plugins")
    # meta type will show on the dropdown selection list.
    meta_type = "iScorpio PlonePAS Squirrel Plugins"

    userSiteId = "Plone"

    _properties = ( { 'id'    : 'title'
                    , 'label' : 'Title'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'userSiteId'
                    , 'label' : 'User Admin Site Id'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  )


    security = ClassSecurityInfo()

    def __init__(self, id, title, userSiteId):

        self._setId(id)
        self.title = title
        self.userSiteId = userSiteId

    # IAuthenticationPlugin
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """
        Authenticate credentials against the following.
        """

        if ('login' not in credentials) or ('password' not in credentials):
            return None

        login = credentials['login']
        password = credentials['password']

        credit = self.getUserAdmin().source_users.authenticateCredentials(credentials)

        if credit is None:
            credit = self.getUserAdmin().ldap.authenticateCredentials(credentials)

        return credit

    # IUserEnumerationPlugin
    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        """
        Return a list of valid users identified by this plugin.
        """

        users = self.getUserAdmin().source_users.enumerateUsers(id, login, exact_match,
                                                                    sort_by, max_results, **kw)

        if (users is None) or (len(users) <= 0):
            users = self.getUserAdmin().mutable_properties.enumerateUsers(id, login, exact_match,
                                                                              **kw)

        ldapUsers = self.getUserAdmin().ldap.enumerateUsers(id, login, exact_match,
                                                                sort_by, max_results, **kw)
        return (users + ldapUsers)

    # IExtractionPlugin
    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """
        forward to user admin to do the 
        """
        app = self.getZopeApp()
        credit = self.getUserAdmin().credentials_cookie_auth.extractCredentials(request)
        self.log.debug('extract credentials: %s', credit)
        return credit

    # ICredentialsUpdatePlugin
    security.declarePrivate('updateCredentials')
    def updateCredentials(self, request, response, login, new_password):
        """
        again forward to the useradmin
        """
        app = self.getZopeApp()
        return self.getUserAdmin().credentials_cookie_auth.updateCredentials(request, response,
                                                                 login, new_password)

    # returns user properties for the given user.
    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """
        get user properties from useradmin.
        """
        app = self.getZopeApp()
        properties = self.getUserAdmin().mutable_properties.getPropertiesForUser(user, request)

        if properties.getProperty('fullname') == '':
            properties = self.getUserAdmin().ldap.getPropertiesForUser(user, request)

        return properties

    # return the zope root object.
    security.declarePrivate('getZopeApp')
    def getZopeApp(self):
        """
        returns the root Zope object, which should be the zope application
        server.
        """
        return self.getPhysicalRoot()

    security.declarePrivate('getUserAdmin')
    def getUserAdmin(self):
        """
        return the user admin site's acl_users object.
        """
        return getattr(self.getPhysicalRoot(), self.userSiteId).acl_users

# implements plugins.
classImplements(SquirrelPlugins,
                IAuthenticationPlugin,
                IUserEnumerationPlugin,
                IExtractionPlugin,
                ICredentialsUpdatePlugin,
                IPropertiesPlugin)

InitializeClass(SquirrelPlugins)
