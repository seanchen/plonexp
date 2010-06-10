
# XPointContactGroup.py

__doc__ = """XPointContactGroup defines a group for contact information"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plantext'

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.atct import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.XPointContactManagement.config import PROJECTNAME
from Products.XPointContactManagement.content.base import XPCMBase

# contact group schema
XPointContactGroupSchema = ATCTContent.schema.copy()

finalizeATCTSchema(XPointContactGroupSchema)

class XPointContactGroup(XPCMBase, ATCTContent):
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

    xpcm_id_prefix ="xpg-"

registerType(XPointContactGroup, PROJECTNAME)
