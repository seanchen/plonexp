# XPointContactGroup.py

__doc__ = """XPointContactGroup defines a group for contact information"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plantext'

import logging
import transaction

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.atct import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.XPointContactManagement.config import PROJECTNAME

# contact group schema
XPointContactGroupSchema = ATCTContent.schema.copy()

finalizeATCTSchema(XPointContactGroupSchema)

class XPointContactGroup(ATCTContent):
    """ group for a contact.
    """

    schema = XPointContactGroupSchema

    meta_type = "XPointContactGroup"
    portal_type = "XPointContactGroup"
    archetype_name = "XPointContactGroup"

    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    log = logging.getLogger("XPointContactManagement XPointContactGroup")
    security = ClassSecurityInfo()

    def _renameAfterCreation(self, check_auto_id=False):
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.debug('the next value for contact group sequence: %s',
                       newId)
        self.setId('xpcg-' + newId)

registerType(XPointContactGroup, PROJECTNAME)
