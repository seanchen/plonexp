# xpointdoc.py

__doc__ = """XPointDocument is the super class of XPointProjectManagement general
documents, such as memo, buildjounal, proposal, and issue."""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# Import modules and functions, etc. used in the following codes. 
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.permissions import View

# the configruation info for this project.
from Products.XPointProjectManagement.config import *

# the XPointBuildJournal Schema.
XPointDocumentSchema = ATCTContent.schema.copy() + Schema((

        # The body of the build journal.
        TextField(
            'xpproject_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = u'Body Text',
                rows = 22
                ),
            ),
        ),
    )

finalizeATCTSchema(XPointDocumentSchema)

# the XPointBuildJournal class.
class XPointDocument(ATCTContent, HistoryAwareMixin):

    schema = XPointDocumentSchema

    #meta_type = 'XPointBuildJournal'
    #portal_type = 'XPointBuildJournal'
    #archetype_name = 'Build Journal'
    #
    #content_icon = 'XPBuildJournal_icon.gif'

    __implements__ = (ATCTContent.__implements__,
                      IATDocument,
                      HistoryAwareMixin.__implements__,
                     )

    _at_rename_after_creation = True

    default_view = 'xpointdoc_view'
    # allow 
    global_allow = True

    security = ClassSecurityInfo()

    security.declareProtected(View, 'CookedBody')
    def CookedBody(self, stx_level = 'ignored'):
        """CMF compatibility method
        """
        return self.getXpproject_text()
