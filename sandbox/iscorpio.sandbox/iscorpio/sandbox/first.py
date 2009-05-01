#!/usr/bin/python

####################################################################
#
####################################################################

import os
import commands
import time

# the main entry.
if __name__ == "__main__":

    # the spool folder
    SPOOL_FOLDER = '/var/spool/first'
    BACKUP_FOLDER = '/var/spool/bak'
    # check the listening folder.
    size = len(os.listdir(SPOOL_FOLDER))
    if size > 0:

        timestamp = time.strftime('%Y%m%d-%H%M%S')
        #output = commands.getoutput('scp %s/* user@10.68.6.159:~/spool' % SPOOL_FOLDER)
        output = os.system('scp %s/* user@10.68.6.159:~/spool' % SPOOL_FOLDER)
    
        logFile = open('%s/log' % BACKUP_FOLDER, 'a')
        logFile.write('\n---------------- Started at: %s' % timestamp)
        logFile.write('\nCopied %d file(s)' % size)
        logFile.write('\n------------------------------------\n')
        logFile.close()
    
        commands.getoutput("mkdir %s/%s" % (BACKUP_FOLDER, timestamp))
        commands.getoutput("mv %s/* %s/%s" %
                           (SPOOL_FOLDER, BACKUP_FOLDER, timestamp))


import smtplib

class GmailHandler:

    def gmailSmtp(self):

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        print session.login('usr', 'password')
