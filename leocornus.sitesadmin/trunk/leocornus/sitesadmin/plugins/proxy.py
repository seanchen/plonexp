
# proxy.py

"""
this package will provide a set of plugins and facilities to 
"""

import logging

from Globals import InitializeClass
from Globals import DTMLFile

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityInfo import ClassSecurityInfo


from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from Products.CMFCore.utils import getToolByName

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"



# the form to add a proxy multi plugin.
manage_addProxyMultiPluginsForm = DTMLFile('proxyAddForm', globals())

# the factory method to add a ssouser plugin.
def manage_addProxyMultiPlugins(self, id, title='Proxy Multi Plugins',
                                separator='\\',
                                userFolder='plone',
                                REQUEST=None):
    """
    Id and title will come with the HTTP request. the user folder is using the
    default Plone site.
    """

    pmp = ProxyMultiPlugins(id, title, separator, userFolder)
    self._setObject(pmp.getId(), pmp)

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
                                     '?manage_tags_message=SitesAdmin+Proxy+Plugins+Added' %
                                     self.absolute_url())

class ProxyMultiPlugins(BasePlugin):
    """
    the ProxyMultiPlugins will provide a facade to let active PAS plugin to
    access the backend PAS services.
    """

    logger = logging.getLogger("Sitesadmin Proxy Plugins")

    meta_type = "SitesAdmin Proxy Mutli Plugins"

    security = ClassSecurityInfo()

    _properties = ( { 'id'    : 'title'
                    , 'label' : 'Title'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    },
                    { 'id'    : 'separator'
                    , 'label' : 'Domain Separator'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    },
                    { 'id'    : 'userFolder'
                    , 'label' : 'User Management Folder'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    },
                  )

    def __init__(self, id, title, separator, userFolder):

        self._setId(id)
        self.title = title
        self.separator = separator
        self.userFolder = userFolder
        self.defaultSuffix = '_default'
        self.propertiesSuffix = '_prop'
        self.factorySuffix = '_factory'
        self.enumrationSuffix = '_enum'

        # add default property provider and default user factory.
        # the priority is like
        # property provider: prefix_prop, prop_default, prefix itself.
        # factory provider: prefix_factory, factory_default, prefix itself.
        self._setProperty('prop_default', 'mutable_properties', 'string')
        self._setProperty('factory_default', 'user_factory', 'string')

    # query the backend authentication provider to verify user's credentials.
    security.declarePrivate('verifyCredentials')
    def verifyCredentials(self, credentials):

        login = credentials['login']
        password = credentials['password']
        if login.find(self.separator) >= 0:
            prefix, theLogin = login.split(self.separator)
        else:
            # it is not for proxy, skip it
            return False

        # verify through 3rd party plugin.
        aclUsers = getToolByName(self, 'acl_users')
        credentials = {'login' : theLogin,
                       'password' : password}

        pluginId = self.getProperty(prefix)
        if pluginId:
            authProvider = getattr(aclUsers, pluginId)
        else:
            raise KeyError, 'Could not find plugin for prefix %s' % prefix

        valid = False
        credit = authProvider.authenticateCredentials(credentials)
        if credit:
            login, name = credit
            if (login != None) & (name != None):
                valid = True

        return valid

    # IAuthenticationPlugin
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """
        Authenticate credentials against the following.
        """

        if ('login' not in credentials) or ('password' not in credentials):
            return None

        valid = self.verifyCredentials(credentials)
        credit = None

        # if success, we need create the membrane user account and then
        if valid:
            # we verified it is a valid user somewhere.
            login = credentials['login']
            if self.setUpMembraneUser(login):
                # revise the credential to use the new user id and user name.
                # new user id and user name should have the prefix.
                credit = (login, login)

        return credit

    # perform search on all 3rd party plugins.
    security.declarePrivate('ssoEnumerateUsers')
    def ssoEnumerateUsers(self, id=None, login=None, exact_match=False,
                          sort_by=None, max_results=None, **kw):
        """
        perform the user search on all 3rd party plugins, it will create the
        membrane user account if it is not exist!
        """

        users = []
        membraneTool = getToolByName(self, 'membrane_tool')
        for prefix, plugin in self.get3rdEnumPlugins():

            # enumerate user for each plugin.
            rets = plugin.enumerateUsers(**kw)
            theRets = []
            for user in rets:
                # try to create membrane user account for each user.
                theLogin = user['id'].lower()
                membraneUserId = "%s%s%s" % (prefix, self.separator, theLogin)

                self.logger.debug('ssoEnumerateUsers - membrane user id=%s' % membraneUserId)
                # we need the exact match for the user id.
                query = {'exact_getUserId' : membraneUserId}
                if not membraneTool.unrestrictedSearchResults(**query):
                    # no membrane user yet! create one.
                    if self.setUpMembraneUser(membraneUserId):
                        # this is a valid user!
                        # should use the new id now. most likely, plugins are
                        # using cache for this search.
                        buf = user.copy()
                        buf['id'] = membraneUserId
                        buf['login'] = membraneUserId
                        theRets.append(buf)
                    else:
                        # this is not a valid user! skip it
                        continue

            users.extend(theRets)

        self.logger.debug('ssoEnumerateUsers(id=%s, login=%s, kw=%s): %s' %
                          (id, login, kw, users))
        return users

    security.declarePrivate('get3rdPlugins')
    def get3rdEnumPlugins(self):
        """
        returns all 3rd party plugins as a list of tuple (prefix, plugin)
        """

        plugins = []
        aclUsers = getToolByName(self, 'acl_users')
        for propery in self._properties:
            prefix = propery['id']
            # do some filter, there maybe some better way.
            if prefix in ['title', 'separator', 'userFolder']:
                continue
            if prefix.endswith(self.defaultSuffix) or \
               prefix.endswith(self.propertiesSuffix) or \
               prefix.endswith(self.factorySuffix) or \
               prefix.endswith(self.enumrationSuffix):
                continue

            enumPluginId = self.getProperty('%s%s' % (prefix, self.enumrationSuffix)
                                            , None)
            if enumPluginId:
                try:
                    enumPlugin = getattr(aclUsers, enumPluginId)
                    plugins.append((prefix, enumPlugin))
                    continue
                except AttributeError:
                    self.logger.debug('get3rdEnumPlugins - Can not find prop provider %s' % enumPluginId)

            pluginId = self.getProperty(prefix)
            try:
                plugin = getattr(aclUsers, pluginId)
                plugins.append((prefix, plugin))
            except AttributeError:
                # just skip
                continue

        return plugins

    security.declarePrivate('setUpMembraneUser')
    def setUpMembraneUser(self, membraneUserId):
        """
        Try to set up a membrame user account for the given membrane user id.
        """

        prefix, theLogin = membraneUserId.split(self.separator)
        props = self.getUserProperties(prefix, theLogin)
        if not props['email']:
            # skip users who don't have an email address
            return False

        self.createUserAccount(membraneUserId, prefix, theLogin, props)
        return True

    security.declarePrivate('getUserProperties')
    def getUserProperties(self, prefix, theLogin):
        """
        returns a property dict for the login id from the prefix plugins.
        it is easier to use dict instead of property sheet.  Since some
        plugins, such as PloneLDAP, are return the user properties as a dict.
        """

        aclUsers = getToolByName(self, 'acl_users')

        pluginId = self.getProperty(prefix)
        if pluginId:
            authProvider = getattr(aclUsers, pluginId)
        else:
            raise KeyError, 'Could not find plugin for prefix %s' % prefix

        prefixPropPlugin = self.getProperty('%s%s' % (prefix,
                                                      self.propertiesSuffix))
        if prefixPropPlugin:
            propProvider = getattr(aclUsers, prefixPropPlugin)
        elif self.getProperty('prop_default'):
            propProvider = getattr(aclUsers,
                                   self.getProperty('prop_default'))
        else:
            propProvider = authProvider

        factoryPlugin = self.getProperty('%s%s' % (prefix, self.factorySuffix))
        if factoryPlugin:
            factory = getattr(aclUsers, factoryPlugin)
        elif self.getProperty('factory_default'):
            factory = getattr(aclUsers,
                              self.getProperty('factory_default'))
        else:
            factory = authProvider

        # try to get a PloneUser object.
        # At the point, we already verified credentials...
        nativeUser = factory.createUser(theLogin, theLogin)
        # specificly for PloneLDAP plugins.
        nativeUser.acl_users = aclUsers

        props = propProvider.getPropertiesForUser(nativeUser)
        if not isinstance(props, dict):
            # suppose it is a instance of property sheet. Might be wrong!
            props = props._properties

        return props

    security.declarePrivate('createUserAccount')
    def createUserAccount(self, login, prefix, theLogin, properties):
        """
        create a user account for the given login id and user properties.
        the user properties should be a dict.
        """

        admin = UnrestrictedUser('manager', '', ['Manager'], '')
        admin = admin.__of__(self.acl_users)
        # save current security manager.
        current_sm = getSecurityManager()
        try:
            # execute the following by using manager permission.
            # ...
            newSecurityManager(None, admin)

            # find the user management folder.
            # create UserAccount in the user management folder.
            uniqueId = '%s-%s' % (prefix, theLogin)
            self.getUserFolder().invokeFactory('UserAccount', uniqueId)
            userAccount = getattr(self.getUserFolder(), uniqueId)

            userAccount.setUserName(login)
            if properties:
                # TODO: ??? need better way to set properties.
                if properties.has_key('fullname'):
                    userAccount.setTitle(properties['fullname'])
                    userAccount.setFullname(properties['fullname'])
                if properties.has_key('email'):
                    userAccount.setEmail(properties['email'])
                if properties.has_key('location'):
                    userAccount.setLocation(properties['location'])
                # XXX more are comming! should leverage the
                # portal_memberdata tool
            else:
                userAccount.setFullname(theLogin)

            # reindexing the new user account in membrane_tool.
            membraneTool = getToolByName(self, 'membrane_tool')
            membraneTool.indexObject(userAccount)
        finally:
            # restore the current security manager.
            setSecurityManager(current_sm)

    # return admin site's membrane user folder, so you can create user account.
    security.declarePrivate('getUserFolder')
    def getUserFolder(self):
        """
        a regular Plone folder as the user management folder.
        """

        app = self.getPhysicalRoot()
        return app.unrestrictedTraverse(self.userFolder)

# implements plugins.
classImplements(ProxyMultiPlugins,
                IAuthenticationPlugin)

InitializeClass(ProxyMultiPlugins)
