# release.py

__doc__ = """XPointRelease defines the release note for a XPoint Project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import registerType

from Products.XPointProjectManagement.content.xpointdoc import XPointDocument
# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME

# define the schema for XPointRelease
XPointReleaseSchema = XPointDocument.schema.copy()

# XPointRelease class.
class XPointRelease(XPointDocument):
    """ XPointRelease will hold a release note for a XPoint Project.
    """

    schema = XPointReleaseSchema

    # define type and name.
    meta_type = 'XPointRelease'
    portal_type = 'XPointRelease'
    archetype_name = 'XP Release'

    content_icon = 'XPRelease_icon.gif'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on release note.
    # comment out for Plone 3, it is just doesn't work.  Need figure
    # out the new approach for Plone 3.
    #allow_discussion = True

    security = ClassSecurityInfo()

# register this type to plone add-on product.
registerType(XPointRelease, PROJECTNAME)
