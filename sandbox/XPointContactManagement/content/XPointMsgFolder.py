# XPointMsgFolder.py

__doc__ = """XPointMsgFolder contains """
__author__ = 'Xiang(Sean) Chen <chyxiang@gmail.com>'
__docformat__ = 'plaintext'

import logging
from operator import itemgetter

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import DisplayList
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
from Products.XPointContactManagement.content.base import XPCMBase

XPointMsgFolderSchema = ATFolderSchema.copy() + Schema((

        # the unique sequence will serve contact, contact group, and contact
        # metadata.
        LinesField(
            'xpcm_emsg_senders',
            required = True,
            # hide for view mode.
            widget = LinesWidget(
                label = "Message Senders' Emails",
                description = 'Set up the senders email addresses here, you may use format like this: <firstname secondname> abc@abcd.com',
                ),
            ),
        )
    )

# Plone 3 will re-organize all fields' shemata by using this method.
finalizeATCTSchema(XPointMsgFolderSchema)

# customizing the schema: set visible and location of fields.

# here comes the class.
class XPointMsgFolder(XPCMBase, ATFolder):
    """XPointMsgFolder will be the folder for contact information.
    """

    schema = XPointMsgFolderSchema

    # type and name for plone site.
    meta_type = 'XPointMsgFolder'
    portal_type = 'XPointMsgFolder'
    archetype_name = 'XPointMsgFolder'

    _at_rename_after_creation = True

    __implements__ = (
        ATFolder.__implements__,
        IATFolder,
        )

    # unique id prefix.
    xpcm_id_prefix = "xpmf-"

    # the logger,
    log = logging.getLogger('XPointContactManagement MessagesFolder')

    # security info for methods.
    security = ClassSecurityInfo()

    # returns all contacts.
    security.declarePublic('getEMessages')
    def getEMessages(self):
        """ Return all messages in this folder.
        """
        allMsgs = self.contentValues(
            filter = {'portal_type' : ['XPointEMessage']}
            )
        allMsgs.sort(key=itemgetter('id'), reverse=True)
        return allMsgs
        # The following is the other way to get content from the
        # folder.  It actually uses the portal_catalog to do the
        # query.  So it returns the catalog object not the content
        # type itself.
        #return self.getFolderContents(
        #    contentFilter = {'portal_type' : ['XPointEMessage'],
        #                     'sort_order' : 'reverse',
        #                     'sort_on':'created'}
        #    )

    def vocabulary_allSenders(self):
        """ return all sender.
        """
        senders = [(one, one) for one in self.xpcm_emsg_senders]
        return DisplayList(senders)

# register to the product.
registerType(XPointMsgFolder, PROJECTNAME)
