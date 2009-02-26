# XPointBuildJournal.py

__doc__ = """XPointBuildJournal Product for Plone to record build
journal."""
__author__ = 'iScorpio'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# Import modules and functions, etc. used in the following codes. 
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from Products.XPointProjectManagement.config import *

# the XPointBuildJournal Schema.
XPointBuildJournalSchema = ATCTContent.schema.copy() + Schema((

        # The body of the build journal.
        TextField(
            'buildJournalBody',
            searchable = True,
            required = True,
            allowable_content_types = ('text/plain',
                                       'text/structured',
                                       'text/html',),
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(label = 'Build Journal Body',
                                rows = 28),
            ),
        ),
    )

# Decide to use the build in plone keywording as the projects selection.
# Plone Keywording field is defined as subject in class
# Archetypes.ExtensibleMetadata.ExtensibleMetadata
# by default this LinesField is located in propertie tab (metadata),
# we need move it to the default tab and set it to required.
XPointBuildJournalSchema['subject'].schemata = 'default' # used to 'metadata'
XPointBuildJournalSchema['subject'].required = True
XPointBuildJournalSchema['subject'].widget.label = 'Projects'
XPointBuildJournalSchema['subject'].widget.size = 6
XPointBuildJournalSchema.moveField('subject', after='description')

XPointBuildJournalSchema['relatedItems'].widget.visible = True
XPointBuildJournalSchema.moveField('relatedItems', pos='bottom')

# this is for folder type.
#finalizeATCTSchema(XPointBuildJournalSchema)

# the XPointBuildJournal class.
class XPointBuildJournal(ATCTContent, HistoryAwareMixin):

    schema = XPointBuildJournalSchema

    meta_type = 'BuildJournal'
    archetype_name = 'BuildJournal'
    portal_type = 'BuildJournal'

    content_icon = 'document_icon.gif'

    _at_rename_after_creation = True

    default_view = 'base_view'
    # allow 
    global_allow = True

    #actions = ({
    #        'id': 'view',
    #        'name': 'View',
    #        'action': 'string:${object_url}/base_view',
    #        'permissions': (CMFCorePermissions.View,)
    #        },{
    #        'id': 'edit',
    #        'name': 'Edit',
    #        'action': 'string:${object_url}/base_edit',
    #        'permissions': (CMFCorePermissions.ViewManagementScreens,)
    #        },{
    #        'id': 'metadata',
    #        'name': 'Properties',
    #        'action': 'string:${object_url}/base_metadata',
    #        'permissions': (CMFCorePermissions.ViewManagementScreens,)
    #        },
    #    )

    security = ClassSecurityInfo()

registerType(XPointBuildJournal, PROJECTNAME)
