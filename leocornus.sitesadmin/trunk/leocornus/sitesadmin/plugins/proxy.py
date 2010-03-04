
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
        #import pdb; pdb.set_trace()
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
            prefix, theLogin = login.split(self.separator)
            # get user properties from the plugin defined in prefix_prop
            propSheet = self.getUserProperties(prefix, theLogin)
            self.createUserAccount(login, prefix, theLogin, propSheet)

            # revise the credential to use the new user id and user name.
            # new user id and user name should have the prefix.
            credit = (login, login)

        return credit

    security.declarePrivate('getUserProperties')
    def getUserProperties(self, prefix, theLogin):
        """
        returns a property sheet for the login id from the prefix plugins.
        """

        aclUsers = getToolByName(self, 'acl_users')

        pluginId = self.getProperty(prefix)
        if pluginId:
            authProvider = getattr(aclUsers, pluginId)
        else:
            raise KeyError, 'Could not find plugin for prefix %s' % prefix

        prefixPropPlugin = self.getProperty('%s_prop' % prefix)
        if prefixPropPlugin:
            propProvider = getattr(aclUsers, prefixPropPlugin)
        elif self.getProperty('prop_default'):
            propProvider = getattr(aclUsers,
                                   self.getProperty('prop_default'))
        else:
            propProvider = authProvider

        factoryPlugin = self.getProperty('%s_factory' % prefix)
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

        return propProvider.getPropertiesForUser(nativeUser)

    security.declarePrivate('createUserAccount')
    def createUserAccount(self, login, prefix, theLogin, propSheet):
        """
        
        """

        #import pdb; pdb.set_trace()
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
            if propSheet:
                # TODO: ??? need better way to set properties.
                userAccount.setFullname(propSheet.getProperty('fullname'))
                userAccount.setEmail(propSheet.getProperty('email'))
                userAccount.setLocation(propSheet.getProperty('location'))
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
