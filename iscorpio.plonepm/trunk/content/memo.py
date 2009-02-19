# memo.py

__doc__ = """XPointMemo defines the memo for a XPoint Project."""
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

# define the schem for XPointMemo.
XPointMemoSchema = ATContentTypeSchema.copy() + Schema((

        # we need rich content for this memo.
        TextField(
            'memo_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Memo Body',
                description = 'Provide the detail description for your memo',
                rows = 18,
                ),
            ),

        # do we need a status field?

        # do we need a type field?
        )
    )

# we don't need descrpiton field for a memo.
XPointMemoSchema['description'].widget.visible = False

# move the related items field to the bottom.
XPointMemoSchema['relatedItems'].widget.visible = True
XPointMemoSchema['relatedItems'].widget.description = \
    "Select related tasks"
XPointMemoSchema.moveField('relatedItems', pos='bottom')

# XPointMemo class.
class XPointMemo(ATCTContent):
    """ XPointMemo defines the note for a XPoint Project.
    """

    schema = XPointMemoSchema

    # type, name.
    meta_type = 'XPointMemo'
    portal_type = 'XPointMemo'
    archetype_name = 'XP Memo'

    content_icon = 'XPMemo_icon.gif'
    immediate_view = 'xpointmemo_view'
    default_fiew = 'xpointmemo_view'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointmemo_view',
        'permissions': (CMFCorePermissions.View,)
        },{
        'id': 'edit',
        'name': 'Edit',
        'action': 'string:${object_url}/base_edit',
        'permissions': (CMFCorePermissions.ModifyPortalContent,)
        },)

    security = ClassSecurityInfo()

# register this type to plone add-on product.
registerType(XPointMemo, PROJECTNAME)
