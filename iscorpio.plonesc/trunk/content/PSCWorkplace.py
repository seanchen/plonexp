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
import time
from operator import itemgetter

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

from Products.CMFPlone.utils import _createObjectByType

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

    security.declarePublic('getWorklogs')
    def getWorklogs(self):
        """
        return all worklogs in this folder.
        """
        allLogs = self.contentValues(
            filter = {'portal_type' : ['PSCWorklog']}
            )
        allLogs.sort(key=itemgetter('id'), reverse=True)
        return allLogs

    security.declareProtected('PloneShellConsole: Execute PSCWorkplace', 'pscWorkplaceExecute')
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
        svnuser = form.get('svnuser')
        svnpassword = form.get('svnpassword')
        self.makeBuild(svnurl, svnuser, svnpassword)

        status.addStatusMessage('Successfully make build for [%s], please check log for details.' % svnurl,
                                type='info')

        return self.REQUEST.RESPONSE.redirect(self.absolute_url())

    # make a build from the given svn url.
    security.declarePrivate('makeBuild')
    def makeBuild(self, svnurl, svnuser, svnpassword):

        buildFolder = '/var/tmp'
        workFolder = 'workplace'

        # change to working directory.
        os.chdir(buildFolder)

        # check out the lates code from svnurl
        svnMessage = commands.getoutput('svn co --username %s --password %s %s %s' %
                                        (svnuser, svnpassword, svnurl, workFolder))
        self.log.debug(svnMessage)

        # get the latest reversion.
        os.chdir('%s/%s' % (buildFolder, workFolder))
        svnMessage = commands.getoutput('svn info')
        self.log.info(svnMessage)

        # parse the info output, extract the reversion number

        log_id = 'log-%s' % time.strftime('%Y%m%d%H%M%S')
        # current user info.
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        full_name = member.getProperty('fullname')

        # creating a log from back end.
        # ============================
        # invokeFactory from folderish object will check the global allowed flag to
        # decide whether not we can create the specified type of content.
        #worklog = self.invokeFactory('PSCWorklog', 100)
        # the _createObjectByType will bypass the global allowed flag checking.
        _createObjectByType('PSCWorklog', self, id=log_id)
        worklog = getattr(self, log_id)

        worklog.setTitle('log message at %s' % time.strftime('%Y-%m-%d %H:%M'))
        worklog.setPsc_log_username(full_name)
        worklog.setPsc_log_timestamp('the time stamp')
        worklog.setPsc_log_message(svnMessage)
        # we have to reindex the object, otherwise the title will not show in the
        # navigation tree and title of the page.
        worklog.reindexObject()

        # make build by using MVN
        #mvnMessage = commands.getoutput('mvn deploy')
        #self.log.info(mvnMessage)

        # parse the mvn output message, extract the artifact names and
        # then create the artifacts list in the worklog.

        commands.getoutput('rm -rf %s/%s' % (buildFolder, workFolder))
        # generate the PSCWorklog document.
        return

# register to the product.
registerType(PSCWorkplace, PROJECTNAME)
