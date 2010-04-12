
# __init__.py

"""
the basic initialization work for a plone product.
"""

from Products.CMFCore.utils import ContentInit
from Products.CMFCore.permissions import AddPortalContent as ADD_CONTENT_PERMISSION

from Products.Archetypes import process_types
from Products.Archetypes.public import listTypes

from Products.PluggableAuthService import registerMultiPlugin

from config import PROJECTNAME
from plugins import ssouser
from plugins import proxy

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# try to register SsouserPlugins available in add plugin selection
# dropdown list.
try:
    registerMultiPlugin(ssouser.SsouserPlugins.meta_type)
    registerMultiPlugin(proxy.ProxyMultiPlugins.meta_type)
except RuntimeError:
    # ignore exceptions on re-registering the plugin
    pass

def initialize(context):

    """
    initialization ...
    """

    # initialize AT content types.
    import content
    content            # make pyflakes happy

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

    # register PAS plugin class.
    context.registerClass(
        ssouser.SsouserPlugins,
        constructors=(
            ssouser.manage_addSsouserPluginsForm,
            ssouser.manage_addSsouserPlugins,
        ),
        visibility=None
    )

    context.registerClass(
        proxy.ProxyMultiPlugins,
        constructors=(
            proxy.manage_addProxyMultiPluginsForm,
            proxy.manage_addProxyMultiPlugins,
        ),
        visibility=None
    )
