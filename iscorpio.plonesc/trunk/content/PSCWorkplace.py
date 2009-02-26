# PSCWorkplace.py

__doc__ = """PSCWorkplace is a Plone foler to provide a console for remote job"""
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
# from ATContenttypes
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf

from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFCore.utils import getToolByName

from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column

from Products.PloneShellConsole.config import PROJECTNAME

PSCWorkplaceSchema = ATFolderSchema.copy() + Schema((

        # Workplace configurtions.
        DataGridField(
            'psc_config_params',
            required = True,
            columns = ('key', 'value', 'description'),
            allow_empty_rows = False,
            widget = DataGridWidget(
                label = u'Configuration Parameters',
                auto_insert = False,
                description = "Please adding your configuration parameters here:",
                columns = {
                    'key' : Column("The Key"),
                    'value' : Column("The Value"),
                    'description' : Column("Description")
                    },
                ),
            ),

        ),
    )

finalizeATCTSchema(PSCWorkplaceSchema)

# define the class.
class PSCWorkplace(ATFolder):
    """ 
    """

    schema = PSCWorkplaceSchema

    # type and name for plone site.
    meta_type = 'PSCWorkplace'
    portal_type = 'PSCWorkplace'
    archetype_name = 'PSCWorkplace'

    _at_rename_after_creation = True

    __implements__ = (
        ATFolder.__implements__,
        IATFolder,
        )

    # local logger,
    log = logging.getLogger('PloneShellConsole PSCWorkplace')

    security = ClassSecurityInfo()

    # here are the methods.

# register to the product.
registerType(PSCWorkplace, PROJECTNAME)
