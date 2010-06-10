#XPointContactMetadata.py

__doc__ = """XPointContactMetadata defines a metadata for contact infomation"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging
import transaction

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.atct import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.XPointContactManagement.config import PROJECTNAME

# The schema for contact metadata.
XPointContactMetadataSchema = ATCTContent.schema.copy()

finalizeATCTSchema(XPointContactMetadataSchema)

class XPointContactMetadata(ATCTContent):
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

    log = logging.getLogger("XPointContactManagement XPointContactMetadata")
    security = ClassSecurityInfo()

    # override Archetypes.BaseObject to generate the id automatically.
    def _renameAfterCreation(self, check_auto_id=False):
        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.debug('The Next value for contact metadata sequence is: %s',
                       newId)
        self.setId('xpcm-' + newId)

registerType(XPointContactMetadata, PROJECTNAME)
