# XPointContact.py

__doc__ = """XPointContact defines a record of contact information"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

# need generate the id automatically,
# 
# title will be the formal name
# 
# other names will be a data grid: chinese, english, nickname, 
# 
# address will be a datagrid: home, mail addr, office addr,
# 
# email will ba a datagrid: personal, work, msn,
# 
# phone will be a datagrid: home, cell, work,
# 
# gender
# 
# memo
# 
# group select from XPointContactGroup
# 
# 
# XPointNameType
# XPointAddressType
# XPointEmailType
# XPointPhoneType
# 
# ----> XPointContactMetadata

import logging
import transaction

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import TextField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

# we are going to use DataGrid field for most fields for a contact.
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.XPointContactManagement.config import PROJECTNAME

# the XPoint Contact schema.
XPointContactSchema = ATCTContent.schema.copy() + Schema((

        # gender
        StringField(
            'xpcm_contact_gender',
            searchable = False,
            required = False,
            default = 'Unknow',
            vocabulary = 'vocabulary_genders',
            widget = SelectionWidget(
                label = "Gender",
                description = 'Select Gender for The Contact',
                format = 'select',
                ),
            ),

        # other names
        DataGridField(
            'xpcm_contact_otherNames',
            searchable = True,
            required = False,
            columns = ('name_type', 'name'),
            allow_empty_rows = False,
            widget = DataGridWidget(
                label = u'Other Names',
                auto_insert = False,
                description = "Other Names for This Person",
                columns = {
                    'name_type' : SelectColumn("Name Type", vocabulary="vocabulary_contactMetadata"),
                    'name' : Column("Other Names")
                    },
                ),
            schemata = 'Contact',
            ),

        # telephone numbers
        DataGridField(
            'xpcm_contact_phones',
            searchable = True,
            required = False,
            columns = ('phone_type', 'phone_number'),
            allow_empty_rows = False,
            widget = DataGridWidget(
                label = u'Phone Numbers',
                auto_insert = False,
                description = "All avaiable phone numbers for this person",
                columns = {
                    'phone_type' : SelectColumn("Phone Type", vocabulary="vocabulary_contactMetadata"),
                    'phone_number' : Column("Phone Number")
                    },
                ),
            schemata = 'Contact',
            ),

        # email addresses
        DataGridField(
            'xpcm_contact_emails',
            searchable = True,
            required = False,
            columns = ('email_type', 'email'),
            allow_empty_rows = False,
            widget = DataGridWidget(
                label = u'E-Mail',
                auto_insert = False,
                description = "All avaiable E-Mail addresses for this person",
                columns = {
                    'email_type' : SelectColumn("E-Mail Type", vocabulary="vocabulary_contactMetadata"),
                    'email' : Column("E-Mail")
                    },
                ),
            schemata = 'Contact',
            ),

        # addresses
        DataGridField(
            'xpcm_contact_addresses',
            searchable = True,
            required = False,
            columns = ('address_type', 'address', 'city', 'province', 'postcode', 'country'),
            allow_empty_rows = False,
            widget = DataGridWidget(
                label = u'Addresses',
                auto_insert = False,
                description = "Addresses for This Person",
                columns = {
                    'address_type' : SelectColumn("Address Type", vocabulary="vocabulary_contactMetadata"),
                    'address' : Column("Address"),
                    'city'    : Column("City/Twon"),
                    'province': Column("Province/State"),
                    'postcode': Column("Postcode"),
                    'country' : Column("Country")
                    },
                ),
            schemata = 'Contact',
            ),

        # groups for this person
        LinesField(
            'xpcm_contact_groups',
            searchable = True,
            required = False,
            vocabulary = "vocabulary_contactGroups",
            widget = InAndOutWidget(
                label = u'Groups',
                description = "Please select groups for this person",
                ),
            schemata = 'Contact',
            ),

        # memo for this contact.
        TextField(
            'xpcm_contact_memo',
            searchable = True,
            required = False,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = u'Contact Memo',
                rows = 22,
                ),
            ),

        ),
    )

# Plone 3 will re-organize all fields' shemata by using this method.
finalizeATCTSchema(XPointContactSchema)

# the class.
class XPointContact(ATCTContent):
    """ ATContentType for a Contact
    """

    schema = XPointContactSchema

    meta_type = "XPointContact"
    portal_type = "XPointContact"
    archetype_name = "XPointContact"

    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    log = logging.getLogger("XPointContactManagement XPointContact")
    security = ClassSecurityInfo()

    # override renameAfterCreation to generate the unique id for
    # contact. This method is defined in Archetypes.BaseObject.py.
    def _renameAfterCreation(self, check_auto_id=False):

        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.info('the next value for contact sequence: %s',
                      newId)
        self.setId('xpc-' + newId)

    # vocabulary for gender field.
    def vocabulary_genders(self):
        """ Return a list of selection for gender.
        """

        return DisplayList([('Male', 'Male'),
                            ('Female', 'Female'),
                            ('Unknow', 'Unkow'),
                            ]
                           )

    # vocabulary for contact metadata.
    def vocabulary_contactMetadata(self):
        """ Returns a list of metadata for types: name type, address type.
        """
        retList = []
        metadata = self.getContactMetadata()
        for aMetadata in metadata:
            retList.append((aMetadata.id, aMetadata.title))

        self.log.debug('The metadata list: %s', retList)
        return DisplayList(retList)

    # vocabulary for contact groups
    def vocabulary_contactGroups(self):
        """ Returns a list of groups for contact.
        """
        retGroups = []
        groups = self.getContactGroups()
        for group in groups:
            retGroups.append((group.id, group.title))

        self.log.debug('the group list: %s', retGroups)
        return DisplayList(retGroups)

registerType(XPointContact, PROJECTNAME)
