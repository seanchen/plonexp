# PSCWorklog.py

__doc__ = """PSCWorklog is a Plone document to save the log for a job"""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

# PSCWorkplace is a folder in Plone, which suppose to provide a centralized place
# a set of similar remote job.  It also tracks all logging message around the
# remote jobs.

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

from Products.statusmessages.interfaces import IStatusMessage

from Products.PloneShellConsole.config import PROJECTNAME

PSCWorklogSchema = ATCTContent.schema.copy() + Schema((

        # user name who perform this work.
        StringField(
            'psc_log_username',
            widget = StringWidget(
                label = 'User Name',
                description = 'The user, who performed this work',
                ),
            #mode = 'r',
            ),

        # time stamp for this work.
        StringField(
            'psc_log_timestamp',
            widget = StringWidget(
                label = 'Time Stamp',
                description = 'Time stamp for this work',
                ),
            #mode = 'r',
            ),

        # log subject, a brief message which 
        StringField(
            'psc_log_subject',
            default_output_type = 'text/x-html-safe',
            widget = StringWidget(
                label = 'Log Subject',
                description = 'This message may include all artifaces info',
                ),
            #mode = 'r',
            ),

        # log message, may have certain format. and we are going to parse it
        # within in a certain method and show it on the view...
        StringField(
            'psc_log_message',
            default_output_type = 'text/x-html-safe',
            widget = StringWidget(
                label = 'Log Message',
                description = 'This message may include all artifaces info',
                ),
            #mode = 'r',
            ),
        ),
    )

finalizeATCTSchema(PSCWorklogSchema)

# set the title to read only.
#PSCWorklogSchema['title'].mode = 'r'

class PSCWorklog(ATCTContent):
    """
    the ATContentType for a work log, we should never edit it.
    """

    schema = PSCWorklogSchema

    meta_type = 'PSCWorklog'
    portal_type = 'PSCWorklog'
    archetype_name = 'PSCWorklog'

    _at_rename_after_creation = True

    __implements__ = (
        ATCTContent.__implements__,
        IATDocument,
        )

    log = logging.getLogger("PloneShellConsole PSCWorklog")
    security = ClassSecurityInfo()

registerType(PSCWorklog, PROJECTNAME)
# End of class PSCWorklog
