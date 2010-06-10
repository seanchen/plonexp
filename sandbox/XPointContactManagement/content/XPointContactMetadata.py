
# XPointContactMetadata.py

__doc__ = """XPointContactMetadata defines a metadata for contact infomation"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.atct import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.XPointContactManagement.config import PROJECTNAME
from Products.XPointContactManagement.content.base import XPCMBase

# The schema for contact metadata.
XPointContactMetadataSchema = ATCTContent.schema.copy()

finalizeATCTSchema(XPointContactMetadataSchema)

class XPointContactMetadata(XPCMBase, ATCTContent):
    """ metadata for a contact.
    """

    schema = XPointContactMetadataSchema

    meta_type = "XPointContactMetadata"
    portal_type = "XPointContactMetadata"
    archetype_name = "XPointContactMetadata"

    # This property will be checked by method _renameAfterCreation
    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    xpcm_id_prefix = "xpcm-"

registerType(XPointContactMetadata, PROJECTNAME)
