
# XPointResponse.py

__doc__ = """XPointResponse defines a """
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

# the configruation info for this project.
from Products.XPointProjectManagement.config import PROJECTNAME
from Products.XPointProjectManagement.content.base import XPPMBase

# define the schema for the metadata.
XPointMetadataSchema = ATCTContent.schema.copy() + Schema((

        # the type of this metadata.
        StringField(
            'xppm_metadata_type',
            vocabulary = 'vocabulary_metadataTypes',
            widget = SelectionWidget(
                label = 'Metadata Type',
                description = 'Set up the type for your metadata',
                format = 'select',
                ),
            ),
        )
    )

finalizeATCTSchema(XPointMetadataSchema)

class XPointMetadata(XPPMBase, ATCTContent, HistoryAwareMixin):

    """ a metadata for XPoint Project.
    """

    schema = XPointMetadataSchema

    meta_type = "XPointMetadata"
    portal_type = "XPointMetadata"
    archetypes_type = "XPointMetadata"

    __implements__ = (ATCTContent.__implements__,
                      HistoryAwareMixin.__implements__,
                      )

    # the prefix for the auto generated ids.
    xppm_id_prefix = 'xpm'
    # log.
    log = logging.getLogger("XPointProjectManagement XPointMetadata")

    security = ClassSecurityInfo()

    def vocabulary_metadataTypes(self):
        """ return all metadata types as a vocabulary.
        """

        return DisplayList([('priority', 'Artifact Priority'),
                            ('category', 'Artifact Category'),
                            ('status', 'Artifact Status'),
                            ])

# register to the plone add-on product.
registerType(XPointMetadata, PROJECTNAME)
