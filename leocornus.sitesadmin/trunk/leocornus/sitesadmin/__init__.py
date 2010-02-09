
# __init__.py

"""
the basic initialization work for a plone product.
"""

from Products.CMFCore.utils import ContentInit
from Products.CMFCore.permissions import AddPortalContent as ADD_CONTENT_PERMISSION

from Products.Archetypes import process_types
from Products.Archetypes.public import listTypes

from config import PROJECTNAME

def initialize(context):

    """
    initialization ...
    """

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
