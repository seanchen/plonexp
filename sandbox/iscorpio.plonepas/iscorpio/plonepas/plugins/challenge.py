# challenge.py

"""
This a testing plugin to provide challenge for un-authenticated users
"""

from Globals import InitializeClass
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import \
     BasePlugin
from Products.PluggableAuthService.interfaces.plugins import \
     IChallengePlugin

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# utility class to add a new RedirectChalenge instance.
def manage_addRedirectChallenge(self, id, REQUEST=None):
    """
    invoked by whatever Object manager to create a Redirect challenge
    plugin.
    """

    # set object on the object manager.
    self._setObject(id, RedirectChallenge(id))

    if REQUEST:
        REQUEST['RESPONSE'].redirect("%s/manage_workspace" % self.absolute_url(),
                                     lock=1)

# the simplest form for create a new RedirectChallenge instance.
def manage_addRedirectChallengeForm(self):
    """
    We only need an id to create the redirect challenge plugin for now.
    """

    return """
    <html><body>
      <h3>Create RedirectChallenge Plugin</h3>
      <form name='createRC' action='manage_addRedirectChallenge'>
        ID: <input name='id', type='text'/> <br/>
        <input type='submit', value='Add'/>
      </form>
    </body></html>
    """

# a very simple challenge plugin for testing.
class RedirectChallenge(BasePlugin):
    """
    A simple challenge plugin to redirect un-authenticated user to a
    static URL.
    """

    # meta_type will be displayed in the add dropdown list on folder
    # acl_users
    meta_type = "iScorpio PAS Simple Redirect Challenge"

    # the initialize method.
    def __init__(self, id):
        """
        the constructor.
        """

        self.id = id

    # implements the challenge method.
    def challenge(self, request, response):
        """
        Returns True if it fired, False otherwise
        """

        response.redirect("http://www.google.com", lock=1)
        return True

# make sure it implements the IChallengePlugin
classImplements(RedirectChallenge, IChallengePlugin)

InitializeClass(RedirectChallenge)

