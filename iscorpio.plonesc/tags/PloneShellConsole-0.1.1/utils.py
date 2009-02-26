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
from random import randint

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

# the Message write to the file system.
MESSAGE_TEMPLATE = """%s,%s,%s"""

# execute script through script man.
def executeScript(svnurl, svnuser, svnpassword):

    tempFolder = "/var/tmp"
    # creating a temp file safely.
    inputFileName = os.path.join(tempFolder, str(randint(100000, 999999)))
    outputFileName = '%s.output' % inputFileName
    inputFileName = '%s.input' % inputFileName

    # write the input.
    inputFile = open(inputFileName, 'w')
    inputFile.write(MESSAGE_TEMPLATE % (svnurl, svnuser, svnpassword))
    inputFile.close()

    # wait until the output is ready.
    while not os.path.exists(outputFileName):

        # sleep in seconds.
        time.sleep(10)

    # one more wait until the file is final.
    time.sleep(5)

    # read the output.
    outputFile = open(outputFileName, 'r')
    theOutput = outputFile.read()
    outputFile.close()

    # parsing the output.
    svnPattern = re.compile(r"(URL|Repository Root|Revision|Last Changed Rev|Last Changed Date): (http://.*|\d*|\d{4}-\d{2}.*)\n")
    svnResult = svnPattern.findall(theOutput)

    mvnPattern = re.compile(r"Uploading: http://.*(/maven.*/(.*\.(jar|war)))\n")
    mvnResult = mvnPattern.findall(theOutput)

    return [svnResult, mvnResult]
# end of class
