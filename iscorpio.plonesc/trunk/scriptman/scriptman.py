#!/usr/bin/env python2.4

# scriptman is daemon to execute some script

import os
import sys
import atexit
import signal
import time
import commands

def executeLoop():

    tempFolder = '/var/tmp'
    workFolder = 'workplace'

    while 1:

        # check the input file.
        inputFileName = commands.getoutput('ls %s/*.input' % tempFolder)
        if not inputFileName.startswith('ls: '):
            # input file found...

            inputFile = open(inputFileName, 'r')
            input = inputFile.read().split(',')
            inputFile.close()
            commands.getoutput('rm -rf %s' % inputFileName)

            os.chdir(tempFolder)
            # check out the lates code from svnurl
            svnMessage = commands.getoutput('svn co --username %s --password %s %s %s' %
                                            (input[1], input[2], input[0], workFolder))

            # get the latest reversion.
            os.chdir('%s/%s' % (tempFolder, workFolder))
            svnOutput = commands.getoutput('svn info')
            # make build by using MVN
            mvnOutput = commands.getoutput('mvn deploy')

            # preparing the output file name.
            outputFileName = inputFileName.replace('input', 'output')
            outputFile = open(outputFileName, 'w')
            outputFile.write(svnOutput + mvnOutput)
            outputFile.close()

            os.chdir(tempFolder)
            commands.getoutput('rm -rf %s/%s' % (tempFolder, workFolder))

        time.sleep(3)

SCRIPTMAN_PID_FILE = "/var/tmp/scriptman.pid"

def write_pid(pidfile_path, pid):
    """ Write the daemon pid to our pid file """
    pid_file = open(pidfile_path, 'w')
    pid_file.write(str(pid))
    pid_file.close()

def exit_function(pidfile_path):
    # Remove the daemon pid file
    try: 
        os.unlink(pidfile_path)
    except: 
        pass

def handle_sigterm(signum, frame):
    sys.exit(0)


if __name__ == "__main__":

    # Do the Unix double-fork magic; see Stevens's book "Advanced
    # Programming in the UNIX Environment" (Addison-Wesley) for details
    # In DEBUG mode we do not fork/detach from the terminal!
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (
            e.errno, e.strerror)
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit from second parent; print eventual PID before exiting
            write_pid(SCRIPTMAN_PID_FILE, pid)
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (
            e.errno, e.strerror)
        sys.exit(1)

    atexit.register(exit_function, SCRIPTMAN_PID_FILE)
    signal.signal(signal.SIGTERM, handle_sigterm)

    executeLoop()
