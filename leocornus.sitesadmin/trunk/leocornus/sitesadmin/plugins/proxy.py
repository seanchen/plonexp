
# proxy.py

"""
this package will provide a set of plugins and facilities to 
"""

import logging

from Globals import InitializeClass
from Globals import DTMLFile
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
                                userFolder='Plone',
                                REQUEST=None):
    """
    Id and title will come with the HTTP request. the user folder is using the
    default Plone site.
    """

    pmp = ProxyMultiPlugins(id, title, userFolder)
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
                    { 'id'    : 'userFolder'
                    , 'label' : 'User Management Folder'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    },
                  )

    def __init__(self, id, title, userFolder):

        self._setId(id)
        self.title = title
        self.userFolder = userFolder

    # query the backend authentication provider to verify user's credentials.
    security.declarePrivate('verifyCredentials')
    def verifyCredentials(self, credentials):

        login = credentials['login']
        password = credentials['password']
        ldapDomain, ldapLogin = login.split('\\')
        # verify through ldap plugin.
        userFolder = getToolByName(self, 'acl_users')
        ldapCredit = {'login' : ldapLogin,
                      'password' : password}

        pluginId = self.getProperty(ldapDomain)
        if pluginId:
            ldapUserFolder = getattr(userFolder, pluginId)
        else:
            raise KeyError, 'Could not find plugin for Domain %s' % loginId

        credit = ldapUserFolder.authenticateCredentials(ldapCredit)
        return credit
 
    # IAuthenticationPlugin
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """
        Authenticate credentials against the following.
        """

        if ('login' not in credentials) or ('password' not in credentials):
            return None

        credit = self.verifyCredentials(credentials)

        # if success, we need create the membrane user account and then
        if credit:
            # we verified it is a valid user somewhere.
            # get user properties
            # find the user management folder.
            # create UserAccount in the user management folder.
            # reindexing the new user account in membrane_tool.
            # revise the credential to use the new user id and user name.
            # new user id and user name should have the prefix.
            print '------------------'

        return credit

# implements plugins.
classImplements(ProxyMultiPlugins,
                IAuthenticationPlugin)
 
InitializeClass(ProxyMultiPlugins)
