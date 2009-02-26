# utils.py

__doc__ = """some utility tools."""
__author__ = "iscorpio@users.sourceforge.net"
__docformat__ = 'plaintext'

import os
import time
import commands
import re
import subprocess
import logging
from threading import Thread

class ScriptExecutor:

    log = logging.getLogger('PloneShellConsole ScriptExecutor')

    # the contructor.
    #def __init__(self):
        # ...

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
        self.log.info("svn result: %s" % svnResult)
    
        # make build by using MVN
        #mvnOutput = commands.getoutput('mvn deploy')
        pmvn = subprocess.Popen("mvn" + " deploy", shell=True, stdout=subprocess.PIPE)
        mvnOutput = pmvn.communicate()[0]
        self.log.debug(mvnOutput)

        # parse the mvn output message, extract the artifact names and
        # then create the artifacts list in the worklog.
        mvnPattern = re.compile(r"Uploading: http://.*(/maven.*/(.*\.(jar|war)))\n")
        mvnResult = mvnPattern.findall(mvnOutput)
        self.log.info("mvn result: %s" % mvnResult)

        # clean up the working folder.
        commands.getoutput('rm -rf %s/%s' % (buildFolder, workFolder))

        return [svnResult, mvnResult]
# End of class.

# execute the script in a separate thread.
class ScriptExecutorThread(Thread):

    def __init__(self, svnurl, svnuser, svnpassword):

        Thread.__init__(self)

        self.svnurl = svnurl
        self.svnuser = svnuser
        self.svnpassword = svnpassword
        self.output = None

    def run(self):

        executor = ScriptExecutor()
        self.output = executor.makeBuild(self.svnurl, self.svnuser, self.svnpassword)
# End of class
