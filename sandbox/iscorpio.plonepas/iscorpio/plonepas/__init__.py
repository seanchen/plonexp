# __init__.py

"""
Zope server will load this file when starts up. Initialization work
happens here.
"""

from Products.PluggableAuthService import registerMultiPlugin

from plugins import challenge
from plugins import squirrel

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# try to register RedirectChallenge available in add plugin selection
# dropdown list.
try:
    registerMultiPlugin(challenge.RedirectChallenge.meta_type)
    registerMultiPlugin(squirrel.SquirrelPlugins.meta_type)
except RuntimeError:
    # ignore exceptions on re-registering the plugin
    pass

# Zope server will load this method when starts up.
def initialize(context):
    """
    Initializer called when used as a Zope 2 product.
    """

    context.registerClass(
        challenge.RedirectChallenge,
        constructors=(
            challenge.manage_addRedirectChallengeForm,
            challenge.manage_addRedirectChallenge,
        ),
        visibility=None
    )

    context.registerClass(
        squirrel.SquirrelPlugins,
        constructors=(
            squirrel.manage_addSquirrelPluginsForm,
            squirrel.manage_addSquirrelPlugins,
        ),
        visibility=None
    )
