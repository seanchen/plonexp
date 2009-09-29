# challenge.py

"""
This a testing plugin to provide challenge for un-authenticated users
"""

from Globals import InitializeClass
from Globals import DTMLFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import \
     BasePlugin
from Products.PluggableAuthService.interfaces.plugins import \
     IChallengePlugin

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# utility class to add a new RedirectChalenge instance.
def manage_addRedirectChallenge(self, id, title='', path='/', REQUEST=None):
    """
    invoked by whatever Object manager to create a Redirect challenge
    plugin.
    """

    # set object on the object manager.
    self._setObject(id, RedirectChallenge(id, title, path))

    if REQUEST:
        REQUEST['RESPONSE'].redirect("%s/manage_workspace" % self.absolute_url(),
                                     lock=1)

# the simplest form for create a new RedirectChallenge instance.
manage_addRedirectChallengeForm = DTMLFile('../zmi/redirect', globals())

# a very simple challenge plugin for testing.
class RedirectChallenge(BasePlugin):
    """
    A simple challenge plugin to redirect un-authenticated user to a
    static URL.
    """

    # meta_type will be displayed in the add dropdown list on folder
    # acl_users
    meta_type = "iScorpio PAS Simple Redirect Challenge"

    # this will help to manage the properties on Properties tab.
    _properties = (
        {"id" : "title",
         "label" : "Title",
         "type" : "string",
         "mode" : "w",
         },
        {"id" : "path",
         "label" : "Target Path",
         "type" : "string",
         "mode" : "w",
        }
        )

    # the initialize method.
    def __init__(self, id, title, path):
        """
        the constructor.
        """

        self.id = id
        self.title = title
        self.path = path

    # implements the challenge method.
    def challenge(self, request, response):
        """
        Returns True if it fired, False otherwise
        """

        response.redirect(self.path, lock=1)
        return True

# make sure it implements the IChallengePlugin
classImplements(RedirectChallenge, IChallengePlugin)

InitializeClass(RedirectChallenge)

