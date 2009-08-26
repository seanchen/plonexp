# squirrel.py

"""
A simple and small PAS plugin. Give it name squirrel means small but
full function.
"""

from Globals import InitializeClass
from Globals import DTMLFile
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the form to add a squirrel plugin.
manage_addSquirrelPluginsForm = DTMLFile('../zmi/squirrelAdd', globals())

# the factory method to add a squirrel plugin.
def manage_addSquirrelPlugins(self, id, title='', REQUEST=None):
    """
    Id and title will come with the HTTP request.
    """

    sp = SquirrelPlugins(id, title)
    self._setObject(sp.getId(), sp)

    if REQUEST:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
                                     '?manage_tags_message=iScoprio+PlonePAS+Squirrel+Plugins+Added' %
                                     self.absolute_url())

class SquirrelPlugins(BasePlugin):
    """
    a small and full function PAS plugin.
    """

    # meta type will show on the dropdown selection list.
    meta_type = "iScorpio PlonePAS Squirrel Plugins"

    security = ClassSecurityInfo()

    def __init__(self, id, title):

        self._setId(id)
        self.title = title

    # IAuthenticationPlugin
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """
        Authenticate credentials against the following.
        """

        if ('login' not in credentials) or ('password' not in credentials):
            return None

        # the fake 
        users = {'abc' : 'bbc',
                 '123' : 'c567'
                 }

        login = credentials['login']
        password = credentials['password']

        if users.get(login, None) != password:
            return None

        # using default PAS to store the credential.
        self._getPAS().updateCredentials(self.REQUEST,
                                         self.REQUEST.RESPONSE,
                                         login, password)
        return (login, login)

    # IUserEnumerationPlugin
    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        """
        Return a list of valid users identified by this plugin.
        """

        key = id or login
        if (not key) or (key not in ['abc', '123']):
            return None;

        return [{'id' : 'abc',
                 'login' : 'abc',
                 'fullname' : 'My Name',
                 'email' : 'myemail@email.com',
                 'pluginid' : self.getId()
                 },
                {'id' : '123',
                 'login' : '123',
                 'fullname' : '123 Name',
                 'email' : 'email@123.com',
                 'pluginid' : self.getId()
                 }
               ]

# implements plugins.
classImplements(SquirrelPlugins,
                IAuthenticationPlugin,
                IUserEnumerationPlugin)

InitializeClass(SquirrelPlugins)