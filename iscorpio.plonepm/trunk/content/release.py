# release.py

__doc__ = """XPointRelease defines the release note for a XPoint Project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType
# from ATContentType
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.configuration import zconf

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View

from Products.XPointProjectManagement.config import *

# define the schema for XPointRelease
XPointReleaseSchema = ATContentTypeSchema.copy() + Schema ((

        # the body of this release note
        TextField(
            'release_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Release Note',
                description = 'Provide the detail explanation for this release',
                rows = 18,
                ),
            ),
        )
    )

# move the related items field to the bottom.
XPointReleaseSchema['relatedItems'].widget.visible = True,
XPointReleaseSchema['relatedItems'].widget.description = 'Select releated tasks'
XPointReleaseSchema.moveField('relatedItems', pos='bottom')

# XPointRelease class.
class XPointRelease(ATCTContent):
    """ XPointRelease will hold a release note for a XPoint Project.
    """

    schema = XPointReleaseSchema

    # define type and name.
    meta_type = 'XPointRelease'
    portal_type = 'XPointRelease'
    archetype_name = 'XP Release'

    content_icon = 'XPRelease_icon.gif'
    immediate_view = 'xpointrelease_view'
    default_view = 'xpointrelease_view'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on release note.
    allow_discussion = True

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointrelease_view',
        'permissions': (CMFCorePermissions.View,)
        },{
        'id': 'edit',
        'name': 'Edit',
        'action': 'string:${object_url}/base_edit',
        'permissions': (CMFCorePermissions.ModifyPortalContent,)
        },)

    security = ClassSecurityInfo()

# register this type to plone add-on product.
registerType(XPointRelease, PROJECTNAME)
