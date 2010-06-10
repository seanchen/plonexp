
# XPointEMessage.py

__doc__ = """XPointEMessage defines a record of Email Message"""
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging
import time

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

from Products.MaildropHost.MaildropHost import Email

from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import registerType

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

from Products.statusmessages.interfaces import IStatusMessage

from Products.XPointContactManagement.config import PROJECTNAME
from Products.XPointContactManagement.content.base import XPCMBase

# the XPoint Contact schema.
XPointEMessageSchema = ATCTContent.schema.copy() + Schema((

        # sender for this message:
        StringField(
            'xpcm_emessage_from',
            required = True,
            vocabulary = 'vocabulary_allSenders',
            widget = SelectionWidget(
                label = u'Sender',
                description = 'Set the sender for this email message',
                format = 'select',
                ),
            ),

        # memo for this contact.
        TextField(
            'xpcm_emessage_body',
            searchable = True,
            required = False,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = u'Email Body',
                description = u'Please edit your email message here!',
                rows = 22,
                ),
            ),

        # the file attachement.
        FileField(
            'xpcm_emessage_attachment',
            required = False,
            searchable = False,
            storage = AnnotationStorage(migrate = True),
            widget = FileWidget(
                label = 'Attachment',
                description = 'You may add one attachment into you email.',
                ),
            ),

        # the view only sending log.
        StringField(
            'xpcm_emessage_sendinglog',
            widget = StringWidget(
                visible = {'edit':'invisible'},
                label = 'Sending Log',
                description = 'Sending log for this message',
                ),
            ),
        ),
    )

# Plone 3 will re-organize all fields' shemata by using this method.
finalizeATCTSchema(XPointEMessageSchema)

# the class.
class XPointEMessage(XPCMBase, ATCTContent):
    """ ATContentType for a email message
    """

    schema = XPointEMessageSchema

    meta_type = "XPointEMessage"
    portal_type = "XPointEMessage"
    archetype_name = "XPointEMessage"

    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    # set the unique id prefix.
    xpcm_id_prefix = "xpem-"

    log = logging.getLogger("XPointContactManagement XPointEMessage")
    security = ClassSecurityInfo()

    # send email based on send email view.
    security.declareProtected('View', 'emessageSendEmail')
    def emessageSendEmail(self):
        """
        listening to the request from the send email view.
        """
        status = IStatusMessage(self.REQUEST)
        form = self.REQUEST.form

        # get values from http request form, form is a dictionary object.

        if form.has_key('form.button.cancel'):
            # clicked cancel.
            status.addStatusMessage('Canceled Sending!', type='info')
            return self.REQUEST.RESPONSE.redirect(self.absolute_url());

        # email receivers
        to = form.get('to', None)
        self.log.info("email send to: %s" % to)
        # preparing the email addresses.
        addresses = set(to.split(','))
        addresses.discard('')
        addresses.discard(' ')

        fromAddress = self.xpcm_emessage_from
        # email subject and bocy.
        subject = self.title
        self.log.debug("email subject: %s", subject)
        body = '<html><body>%s</body></html>' % self.xpcm_emessage_body
        self.log.debug("email body: %s", body)

        self.dropEmail(fromAddress, addresses, subject, body)
        status.addStatusMessage('Sent email to %s recipients' % len(addresses), type='info')

        return self.REQUEST.RESPONSE.redirect(self.absolute_url())

    security.declareProtected('View', 'dropEmail')
    def dropEmail(self, fromAddress, addresses, subject, body):
        """
        drop emails to the DropmailHost pool.
        """
        if not addresses:
            return

        portal_url  = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        charset = portal.getProperty('email_charset', None)
        if charset is None or charset == '':
            charset = plone_utils.getSiteEncoding()

        # using MIMEMultipart for the message.
        email = MIMEMultipart('mixed')
        email.epilogue = ''

        # from, to, subject
        email['From'] = fromAddress
        if isinstance(subject, unicode):
            subject = subject.encode(charset, 'replace')
        email['Subject'] = subject
        email['To'] = ''

        # adding this to make both plain text and html available, using the same boundary
        textMessage = MIMEMultipart('alternative')

        # preparing the email message
        if isinstance(body, unicode):
            body = body.encode(charset, 'replace')
        textPart = MIMEText(body, 'plain', charset)
        textMessage.attach(textPart)
        # the html format.
        htmlPart = MIMEText(body, 'html', charset)
        textMessage.attach(htmlPart)

        email.attach(textMessage)

        ## the attachment.
        fileField = self.getField('xpcm_emessage_attachment')
        filename = fileField.getFilename(self)
        if (filename != None) & (filename != ''):
            self.log.debug("trying to attach the attachment: %s ..." % filename)
            attachment = MIMEBase('application', 'octet-stream', name=filename)
            attachment.set_payload(fileField.get(self, raw=True).data)
            Encoders.encode_base64(attachment)
            # set up the header.
            attachment.add_header('Content-Disposition',
                                  'attachment; filename="%s"' % filename)
            email.attach(attachment)

        for address in addresses:
            if isinstance(address, unicode):
                address = address.encode(charset, 'replace')
            try:
                email._headers.pop()
                email['To'] = address
                msg = Email(fromAddress, address, email.as_string())
                msg.send()
            except:
                self.log.error('Sending email error for %s!' % (address))
                raise

        self.setSendingLog(len(addresses))

    def setSendingLog(self, amount):
        """
        sending log.
        """
        logMsg = "%s - Sent to %d receiver(s)" % (time.strftime('%Y-%m-%d %H:%M:%S'), amount)

        if self.xpcm_emessage_sendinglog:
            self.xpcm_emessage_sendinglog = \
                self.xpcm_emessage_sendinglog + ',' + logMsg
        else:
            self.xpcm_emessage_sendinglog = logMsg

    security.declareProtected('View', 'getSendingLog')
    def getSendingLog(self):
        """
        return sending log as a list.
        """
        if self.xpcm_emessage_sendinglog:
            theLog = self.xpcm_emessage_sendinglog.split(',')
            theLog.reverse()
            return theLog
        else:
            return []

registerType(XPointEMessage, PROJECTNAME)
