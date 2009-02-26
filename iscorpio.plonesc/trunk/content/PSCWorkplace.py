# PSCWorkplace.py

__doc__ = """PSCWorkplace is a Plone foler to provide a console for remote job"""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

# PSCWorkplace is a folder in Plone, which suppose to provide a centralized place
# a set of similar remote job.  It also tracks all logging message around the
# remote jobs.

import os
import commands
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

    security.declareProtected('View', 'pscWorplaceExecute')
    def pscWorkplaceExecute(self):
        """
        execute a workplace request.
        """
        status = IStatusMessage(self.REQUEST)
        form = self.REQUEST.form

        if form.has_key('form.button.cancel'):
            status.addStatusMessage('Cancel Executing ...', type='info')
            return self.REQUEST.RESPONSE.redirect(self.absolute_url());

        # the svn url.
        svnurl = form.get('svnurl', None)
        self.makeBuild(svnurl)

        status.addStatusMessage('Successfully make build for [%s], please check log for details.' % svnurl,
                                type='info')

        return self.REQUEST.RESPONSE.redirect(self.absolute_url())

    # make a build from the given svn url.
    security.declarePrivate('View', 'makeBuild')
    def makeBuild(self, svnurl):

        buildFolder = '~/temp'
        workFolder = 'workplace'

        # change to working directory.
        os.chdir(buildFolder)

        # check out the lates code from svnurl
        svnMessage = commands.getoutput('svn co --username user --password password %s %s' % (svnurl, workFolder))
        self.log.info(svnMessage)

        # make build by using MVN
        os.chdir('%s/%s' % (buildFolder, workFolder))
        mvnMessage = commands.getoutput('mvn deploy')
        self.log.info(mvnMessage)

        # parse the mvn output message.

        commands.getoutput('rm -rf %s/%s' % (buildFolder, workFolder))
        # generate the PSCWorklog document.
        return

# register to the product.
registerType(PSCWorkplace, PROJECTNAME)
