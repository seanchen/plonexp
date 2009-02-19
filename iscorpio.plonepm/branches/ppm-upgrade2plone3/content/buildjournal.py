# buildjournal.py

__doc__ = """XPointBuildJournal Product for Plone to record build
journal."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# Import modules and functions, etc. used in the following codes. 
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.permissions import View

# the configruation info for this project.
from Products.XPointProjectManagement.config import *

# the XPointBuildJournal Schema.
XPointBuildJournalSchema = ATCTContent.schema.copy() + Schema((

        # The body of the build journal.
        TextField(
            'buildJournalBody',
            searchable = True,
            required = True,
            allowable_content_types = zconf.ATDocument.allowed_content_types,
            default_content_type = zconf.ATDocument.default_content_type,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Build Journal Body',
                description = "The content of this build journal",
                rows = 22
                ),
            ),
        ),
    )

finalizeATCTSchema(XPointBuildJournalSchema)

# Decide to use the build in plone keywording as the projects selection.
# Plone Keywording field is defined as subject in class
# Archetypes.ExtensibleMetadata.ExtensibleMetadata
# by default this LinesField is located in propertie tab (metadata),
# we need move it to the default tab and set it to required.
XPointBuildJournalSchema['subject'].schemata = 'default' # used to 'metadata'
XPointBuildJournalSchema['subject'].required = True
XPointBuildJournalSchema['subject'].widget.label = 'Projects'
XPointBuildJournalSchema['subject'].widget.description = \
    "Select projects for this build journal, holding CTRL key to select more than one project"
XPointBuildJournalSchema['subject'].widget.size = 6
XPointBuildJournalSchema.moveField('subject', after='description')

XPointBuildJournalSchema['relatedItems'].widget.visible = True
XPointBuildJournalSchema['relatedItems'].widget.description = \
    "Select related items"
XPointBuildJournalSchema['relatedItems'].schemata = 'default'
XPointBuildJournalSchema.moveField('relatedItems', pos='bottom')

# the XPointBuildJournal class.
class XPointBuildJournal(ATCTContent, HistoryAwareMixin):

    schema = XPointBuildJournalSchema

    meta_type = 'XPointBuildJournal'
    portal_type = 'XPointBuildJournal'
    archetype_name = 'Build Journal'

    content_icon = 'XPBuildJournal_icon.gif'

    __implements__ = (ATCTContent.__implements__,
                      IATDocument,
                      HistoryAwareMixin.__implements__,
                     )

    _at_rename_after_creation = True

    default_view = 'base_view'
    # allow 
    global_allow = True

    security = ClassSecurityInfo()

registerType(XPointBuildJournal, PROJECTNAME)
