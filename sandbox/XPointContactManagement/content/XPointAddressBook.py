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

from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFCore.utils import getToolByName

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from ZODB.POSException import ConflictError

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

    # returns all contacts for the given groups
    security.declarePublic('getContactsForGroups')
    def getContactsForGroups(self, groups):
        """
        """
        if (not groups) or (not isinstance(groups, list)):
            return

        catalog = getToolByName(self, 'portal_catalog')
        query = self.buildContactSearchQuery(
            portal_type = 'XPointContact',
            contact_group = groups)
        return catalog.searchResults(query)

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
                           'contact_group' : 'getXpcm_contact_groups',
                           }

        query                = {}
        query['path']        = '/'.join(self.getPhysicalPath())

        for k, v in allowedCriteria.items():
            if k in criteria:
                query[v] = criteria[k]
            elif v in criteria:
                query[v] = criteria[v]

        return query

    # send email based on send email view.
    security.declareProtected('View', 'addressBookSendEmail')
    def addressBookSendEmail(self):
        """
        listening to the request from the send email view.
        """
        status = IStatusMessage(self.REQUEST)
        form = self.REQUEST.form

        # get values from http request form

        # email receivers
        to = form.get('to', None)
        self.log.info("email send to: " + str(to))
        contacts = self.getContactsForGroups(to)
        self.log.debug("Found %s contacts" % len(contacts))
        # preparing the email addresses.
        addresses = list()
        for contact in contacts:
            name = contact.Title
            emails = contact.getXpcm_contact_emails
            for email in emails:
                theEmail = '%s <%s>' % (name, email['email'])
                addresses.append(theEmail)
                self.log.debug("adding email: " + theEmail)

        # email subject and bocy.
        subject = form.get('subject', None)
        self.log.info("email subject: " + subject)
        body = form.get('body', None)

        self.sendEmail(addresses, subject, body)
        status.addStatusMessage('Sent emails to: %s' % (to), type='info')

        return self.REQUEST.RESPONSE.redirect(self.absolute_url())

    # this is the generic method for address book to send email.
    security.declareProtected('View', 'sendEmail')
    def sendEmail(self, addresses, subject, body):
        """
        send email from address book.
        """
        if not addresses:
            return

        portal_url  = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        plone_utils = getToolByName(self, 'plone_utils')
        mailHost = plone_utils.getMailHost()

        # preparing the from address.
        charset     = portal.getProperty('email_charset', None)
        if charset is None or charset == '':
            charset = plone_utils.getSiteEncoding()
        fromAddress = portal.getProperty('email_from_address', None)
        if fromAddress is None:
            self.log.error('Cannot send notification email: email sender address not set')
            return
        fromName = portal.getProperty('email_from_name', None)
        if fromName is not None:
            fromAddress = "%s <%s>" % (fromName, fromAddress)
        if isinstance(fromAddress, unicode):
            fromAddress = fromAddress.encode(charset, 'replace')
        # for testing only!
        #fromAddress = 'web master <test@example.com>'

        email = MIMEMultipart('alternative')
        email.epilogue = ''

        # preparing the email message
        if isinstance(body, unicode):
            body = body.encode(charset, 'replace')
        textPart = MIMEText(body, 'plain', charset)
        email.attach(textPart)
        # the html format.
        htmlPart = MIMEText(body, 'html', charset)
        email.attach(htmlPart)

        message = str(email)

        if isinstance(subject, unicode):
            subject = subject.encode(charset, 'replace')

        for address in addresses:
            if isinstance(address, unicode):
                address = address.encode(charset, 'replace')
            try:
                mailHost.send(message = message,
                              mto = address,
                              mfrom = 'David <david@google.com>',
                              subject = subject)
            except ConflictError:
                raise
            except:
                self.log.error('Sending email error for %s!' % (address))

# register to the product.
registerType(XPointAddressBook, PROJECTNAME)
