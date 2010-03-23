
# ssouser.py

"""
single signon user PAS plugins
"""

import logging

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
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
from Products.PlonePAS.interfaces.plugins import IUserIntrospection

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the form to add a ssouser plugin.
manage_addSsouserPluginsForm = DTMLFile('ssouserAdd', globals())

# the factory method to add a ssouser plugin.
def manage_addSsouserPlugins(self, id, title='', userSiteId='sites_admin',
                             restrictSearch=False, REQUEST=None):
    """
    Id and title will come with the HTTP request.
    """

    sp = SsouserPlugins(id, title, userSiteId, restrictSearch)
    self._setObject(sp.getId(), sp)

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
                                     '?manage_tags_message=SitesAdmin+Ssouser+Plugins+Added' %
                                     self.absolute_url())

class SsouserPlugins(BasePlugin):
    """
    We are trying to forward all request to an admin product under Zope root.
    Typically the following request:
    - IAuthenticationPlugin.authenticateCredentials
    - IUserEnumerationPlugin.enumerateUsers
    """

    log = logging.getLogger("Ssouser Plugins")
    # meta type will show on the dropdown selection list.
    meta_type = "SitesAdmin Single Sign On User Plugins"

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
                  , { 'id'    : 'restrictSearch'
                    , 'label' : 'Restrict User Search to Site Level'
                    , 'type'  : 'boolean'
                    , 'mode'  : 'w'
                    }
                  )

    security = ClassSecurityInfo()

    def __init__(self, id, title, userSiteId, restrictSearch):

        self._setId(id)
        self.title = title
        self.userSiteId = userSiteId
        self.restrictSearch = restrictSearch

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

        credit = self.getUserAdmin().membrane_users.authenticateCredentials(credentials)
        if not credit:
            credit = self.getUserAdmin().sitesadmin_proxy.authenticateCredentials(credentials)

        return credit

    # IUserEnumerationPlugin
    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        """
        Return a list of valid users identified by this plugin.
        """

        users = []
        if (id == None and login == None and kw == {}) and self.restrictSearch:
            # search for all users.
            for user in self.getUsers():
                userMap = {'id' : user.getId(),
                           'login' : user.getId(),
                           'pluginid' : self.id}
                users.append(userMap)
        else:
            userAdmin = self.getUserAdmin().membrane_users
            rets = userAdmin.enumerateUsers(id, login, exact_match, sort_by,
                                            max_results, **kw)

            if self.restrictSearch:
                for user in rets:
                    if self.getRolesForUser(user['id']):
                        users.append(user)
            else:
                users.extend(rets)

        self.log.debug('enumerateUsers(id=%s, login=%s, kw=%s): %s' % (id, login, kw, users))

        return users

    # IExtractionPlugin
    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """
        forward to user admin to do the 
        """

        credit = self.getUserAdmin().credentials_cookie_auth.extractCredentials(request)

        return credit

    # ICredentialsUpdatePlugin
    security.declarePrivate('updateCredentials')
    def updateCredentials(self, request, response, login, new_password):
        """
        again forward to the useradmin
        """

        return self.getUserAdmin().credentials_cookie_auth.updateCredentials(request, response,
                                                                 login, new_password)

    # IUserFactoryPlugin
    security.declarePrivate('createUser')
    def createUser(self, user_id, name):
        """
        create a new IPropertiedUser object.
        """
        user = self.getUserAdmin().membrane_user_factory.createUser(user_id, name)

        return user

    # returns user properties for the given user.
    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """
        get user properties from useradmin.
        """

        properties = self.getUserAdmin().membrane_properties.getPropertiesForUser(user, request)
        properties._id = self.id

        return properties

    # set properties for user
    security.declarePrivate('setPropertiesForUser')
    def setPropertiesForUser(self, user, propertysheet):

        self.getUserAdmin().membrane_properties.setPropertiesForUser(user,
                                                                     propertysheet)

    # delete user
    security.declarePrivate('deleteUser')
    def deleteUser(self, user_id):

        # XXX: Not now
        pass

    security.declarePrivate('getUsers')
    def getUsers(self):
        """
        Return a list of users within this site.
        """

        userFolder = self.acl_users
        users = set()
        for userId in self.getPrincipalIds():
            user = userFolder.getUserById(userId, None)
            # it will be None for groups and stall ids.
            if user:
                # this is not a group.
                users.add(user)

        return users

    security.declarePrivate('getPrincipalIds')
    def getPrincipalIds(self):
        """
        return a set of user ids within this site, who has been assigned at lest
        one role.
        """

        userFolder = self.acl_users
        roleManager = userFolder.portal_role_manager

        ids = set()
        for role in roleManager.listRoleIds():
            principals = roleManager.listAssignedPrincipals(role)
            ids.update(principals)

        return ids

    security.declarePrivate('getRolesForUser')
    def getRolesForUser(self, userId, default=None):
        """
        return a tuple of roles for the given userid.
        """

        userFolder = self.acl_users
        roleManager = userFolder.portal_role_manager

        return roleManager._principal_roles.get(userId, default)

    security.declarePrivate('getUserIds')
    def getUserIds(self):
        """
        return a list of user ids.
        """

        pass

    security.declarePrivate('getUserNames')
    def getUserNames(self):
        """
        retrun a list of user names.
        """

        pass

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
classImplements(SsouserPlugins,
                IAuthenticationPlugin,
                IUserEnumerationPlugin,
                IUserFactoryPlugin,
                IExtractionPlugin,
                ICredentialsUpdatePlugin,
                IPropertiesPlugin,
                IUserIntrospection,
                IMutablePropertiesPlugin)

InitializeClass(SsouserPlugins)
