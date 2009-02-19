# issue.py

__doc__ = """XPointMemo records issue for a XPoint Project."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import registerType
# from ATContentType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.configuration import zconf

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View

from Products.XPointProjectManagement.config import *

# the XPointIssue schema.
XPointIssueSchema = ATContentTypeSchema.copy() + Schema((

        # the issue details description.
        TextField(
            'issue_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Issue Body',
                description = 'Provide the detail description for your issue',
                rows = 18,
                ),
            ),

        # the status for this issue.
        StringField(
            'xpoint_tracking_status',
            searchable = False,
            required = True,
            default = 'open',
            vocabulary = (
                ('open', 'Open'),
                ('pending', 'Pending'),
                ('close', 'Close'),
                ),
            widget = SelectionWidget(
                label = 'Issue Status',
                descrpiton = 'Set status for this issue.',
                format = 'select',
                ),
            ),

        )
    )

# make description invisible.
XPointIssueSchema['description'].widget.visible = False

# move the related items to the buttom.
XPointIssueSchema['relatedItems'].widget.visible = True
XPointIssueSchema['relatedItems'].widget.description = \
    "Select related tasks"
XPointIssueSchema.moveField('relatedItems', pos='bottom')

finalizeATCTSchema(XPointIssueSchema)

# the class.
class XPointIssue(ATCTContent):
    """ XPointIssue records a issue for a XPoint Project.
    """

    schema = XPointIssueSchema

    # type and name
    meta_type = 'XPointIssue'
    portal_type = 'XPointIssue'
    archetype_name = "XP Issue"

    content_icon = 'XPIssue_icon.gif'
    immediate_view = 'xpointissue_view'
    default_view = 'xpointissue_view'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on issue.
    # comment out for Plone 3, it is just doesn't work.  Need figure
    # out the new approach for Plone 3.
    #allow_discussion = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        HistoryAwareMixin.__implements__,
        )

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointissue_view',
        'permissions': (CMFCorePermissions.View,)
        },{
        'id': 'edit',
        'name': 'Edit',
        'action': 'string:${object_url}/base_edit',
        'permissions': (CMFCorePermissions.ModifyPortalContent,)
        },)

    security = ClassSecurityInfo()

    def initializeArchetype(self, **kwargs):
        ATCTContent.initializeArchetype(self, **kwargs)

# register this type to plone add-on product.
registerType(XPointIssue, PROJECTNAME)
