# PSCWorkplace.py

__doc__ = """PSCWorkplace is a Plone foler to provide a console for remote job"""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

# PSCWorkplace is a folder in Plone, which suppose to provide a centralized place
# a set of similar remote job.  It also tracks all logging message around the
# remote jobs.

import os
import re
import commands
import logging
import time
import subprocess
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
        self.log.info("making build for %s" % svnurl)
        self.makeBuild(svnurl, svnuser, svnpassword)

        status.addStatusMessage('Successfully make build for [%s], please check log for details.' % svnurl,
                                type='info')

        self.log.debug("redirecting to %s" % self.absolute_url())
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
        svnOutput = commands.getoutput('svn info')
        self.log.info(svnOutput)
    
        # parse the info output, extract the reversion number
        svnPattern = re.compile(r"(URL|Repository Root|Revision|Last Changed Rev|Last Changed Date): (http://.*|\d*|\d{4}-\d{2}.*)\n")
        svnResult = svnPattern.findall(svnOutput)
        svnPath = svnResult[0][1].replace(svnResult[1][1], "")
        svnMessage = self.psc_svn_message(self,
                                          svnURL = svnResult[0][1],
                                          svnPath = svnPath,
                                          svnRevision = svnResult[2][1],
                                          svnLastRev = svnResult[3][1],
                                          svnLastDate = svnResult[4][1])
    
        # make build by using MVN
        #mvnOutput = commands.getoutput('mvn deploy')
        pmvn = subprocess.Popen("mvn" + " deploy", shell=True, stdout=subprocess.PIPE)
        mvnOutput = pmvn.communicate()[0]
        self.log.debug(mvnOutput)

        self.log.info("generating the worklog ...")
        # parse the mvn output message, extract the artifact names and
        # then create the artifacts list in the worklog.
        mvnPattern = re.compile(r"Uploading: http://.*(/maven.*/(.*\.(jar|war)))\n")
        mvnResult = mvnPattern.findall(mvnOutput)
        mvnMessage = ""
        for one in mvnResult:
            mvnMessage = mvnMessage + self.psc_mvn_message(self,
                                                           artifactURL = one[0],
                                                           artifactName = one[1]
                                                           )
        self.log.debug("mvn message: %s" % mvnMessage)

        # generate the PSCWorklog document.
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
        worklog.setPsc_log_timestamp(time.strftime('%b %d, %Y %H:%M'))
        worklog.setPsc_log_username(full_name)
        worklog.setPsc_log_subject(svnMessage)
        worklog.setPsc_log_message(mvnMessage)
        # we have to reindex the object, otherwise the title will not show in the
        # navigation tree and title of the page.

        worklog.reindexObject()
        # clean up the working folder.
        commands.getoutput('rm -rf %s/%s' % (buildFolder, workFolder))

        return

# register to the product.
registerType(PSCWorkplace, PROJECTNAME)
