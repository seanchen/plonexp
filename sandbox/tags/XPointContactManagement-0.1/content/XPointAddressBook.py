# XPointAddressBook.py

__doc__ = """XPointAddressBook contains """
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import registerType
# from ATContenttypes
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.utils import getToolByName

from Products.XPointContactManagement.config import PROJECTNAME

XPointAddressBookSchema = ATFolderSchema.copy() + Schema((

        # the unique sequence will serve contact, contact group, and contact
        # metadata.
        IntegerField(
            'xpcm_unique_sequence',
            default = 0,
            # hide for view mode.
            widget = IntegerWidget(
                label = 'Unique Sequence',
                description = 'This sequence will generate unique ids for this address book',
                ),
            ),
        )
    )

# Plone 3 will re-organize all fields' shemata by using this method.
finalizeATCTSchema(XPointAddressBookSchema)

# customizing the schema: set visible and location of fields.

# here comes the class.
class XPointAddressBook(ATFolder):
    """XPointAddressBook will be the folder for contact information.
    """

    schema = XPointAddressBookSchema

    # type and name for plone site.
    meta_type = 'XPointAddressBook'
    portal_type = 'XPointAddressBook'
    archetype_name = 'XPointAddressBook'

    _at_rename_after_creation = True

    __implements__ = (
        ATFolder.__implements__,
        IATFolder,
        )

    # the logger,
    log = logging.getLogger('XPointContactManagement AddressBook')

    # security info for methods.
    security = ClassSecurityInfo()

    # returns all contacts.
    security.declarePublic('getContancts')
    def getContacts(self):
        """ Return all contacts in this address book.
        """
        return self.contentValues(
            filter = {'portal_type' : ['XPointContact']}
            )

    security.declarePublic('getContactMetadata')
    def getContactMetadata(self):
        """ Returns all metadata defined in this address book.
        """
        return self.contentValues(
            filter = {'portal_type' : ['XPointContactMetadata']}
            )

    security.declarePublic('getContactMetadatum')
    def getContactMetadatum(self, metadatumId):
        """ Returns a metadatum for the given metadatumId.
        """
        catalog = getToolByName(self, 'portal_catalog')
        query = self.buildContactSearchQuery(id=metadatumId,
                                             portal_type='XPointContactMetadata')
        result = catalog.searchResults(query)
        # the result should be only one.
        return result[0]

    security.declarePublic('getContactGroups')
    def getContactGroups(self):
        """ Return all groups defined in this address book.
        """
        return self.contentValues(
            filter = {'portal_type': ['XPointContactGroup']}
            )

    security.declarePublic('getContactGroup')
    def getContactGroup(self, groupId):
        """ Returns a group for the given gourpId.
        """
        catalog = getToolByName(self, 'portal_catalog')
        query = self.buildContactSearchQuery(id=groupId,
                                             portal_type='XPointContactGroup')
        result = catalog.searchResults(query)
        # the result should be only one.
        return result[0]

    security.declarePublic('getNextUniqueId')
    def getNextUniqueId(self):
        """ Return the next value from the unique sequence, and
            update the sequence itself.
        """
        newId = self.xpcm_unique_sequence + 1
        self.setXpcm_unique_sequence(newId)
        return newId

    # facility method to build query for searching portal_catalog.
    def buildContactSearchQuery(self, criteria=None, **kwargs):
        """
        Build canonical query for contact search
        """

        if criteria is None:
            criteria = kwargs
        else:
            criteria = dict(criteria)

        allowedCriteria = {'tags'          : 'Subject',
                           'text'          : 'SearchableText',
                           'id'            : 'getId',
                           'portal_type'   : 'portal_type',
                           }

        query                = {}
        query['path']        = '/'.join(self.getPhysicalPath())

        for k, v in allowedCriteria.items():
            if k in criteria:
                query[v] = criteria[k]
            elif v in criteria:
                query[v] = criteria[v]

        return query

# register to the product.
registerType(XPointAddressBook, PROJECTNAME)
