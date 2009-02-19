# proposal.py

__doc__ = """XPointMemo records proposal for a XPoint Project."""
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
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.configuration import zconf

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import View

from Products.XPointProjectManagement.config import *

# the XPointProposal schema.
XPointProposalSchema = ATContentTypeSchema.copy() + Schema((

        # the proposal details description.
        TextField(
            'proposal_text',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Proposal Body',
                description = 'Provide the detail description for your proposal',
                rows = 18,
                ),
            ),

        # the status for this proposal.
        StringField(
            'xpoint_tracking_status',
            searchable = False,
            required = True,
            default = 'draft',
            vocabulary = (
                ('draft', 'Draft'),
                ('pending', 'Pending'),
                ('accepted', 'Accepted'),
                ),
            widget = SelectionWidget(
                label = 'Proposal Status',
                descrpiton = 'Set status for this proposal.',
                format = 'select',
                ),
            ),

        )
    )

# make description invisible.
XPointProposalSchema['description'].widget.visible = False

# move the related items to the buttom.
XPointProposalSchema['relatedItems'].widget.visible = True
XPointProposalSchema['relatedItems'].widget.description = \
    "Select related tasks"
XPointProposalSchema.moveField('relatedItems', pos='bottom')

# the class.
class XPointProposal(ATCTContent):
    """ XPointProposal records a proposal for a XPoint Project.
    """

    schema = XPointProposalSchema

    # type and name
    meta_type = 'XPointProposal'
    portal_type = 'XPointProposal'
    archetype_name = "XP Proposal"

    content_icon = 'XPProposal_icon.gif'
    immediate_view = 'xpointproposal_view'
    default_view = 'xpointproposal_view'

    _at_rename_after_creation = True
    global_allow = False
    filter_content_types = False
    allowed_content_types = []

    # allow discuss on proposal.
    allow_discussion = True

    actions = ({
        'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/xpointproposal_view',
        'permissions': (CMFCorePermissions.View,)
        },{
        'id': 'edit',
        'name': 'Edit',
        'action': 'string:${object_url}/base_edit',
        'permissions': (CMFCorePermissions.ModifyPortalContent,)
        },)

    security = ClassSecurityInfo()

# register this type to plone add-on product.
registerType(XPointProposal, PROJECTNAME)
