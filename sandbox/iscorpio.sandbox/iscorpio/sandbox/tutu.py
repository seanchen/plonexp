# tutu.py

# a mailing list services.

import re
import email
from email.message import Message
import imaplib
import smtplib

IMAP_MAILHOST = 'imap.gmail.com'
IMAP_PORT = 993
SMTP_MAILHOST = 'smtp.gmail.com'
SMTP_PORT = 587

class EmailServices(object):

    """ ImapServices will provide a easy and simple interface to
    access IMAP email services.
    """

    # init.
    def __init__(self):

        # for IMAP server.
        self.imapSession = None
        # for SMTP server.
        self.smtpSession = None

    # start a imap session.
    def startImapSession(self, username, password):

        self.imapSession = imaplib.IMAP4_SSL(IMAP_MAILHOST, IMAP_PORT)
        return self.imapSession.login(username, password)

    # setart a SMTP session
    def startSmtpSession(self, username, password):

        self.smtpSession = smtplib.SMTP(SMTP_MAILHOST, SMTP_PORT)
        # gmail using tls for smtp.
        self.smtpSession.ehlo()
        self.smtpSession.starttls()
        self.smtpSession.ehlo()
        self.smtpSession.login(username, password)
        return self.smtpSession

    # end a imap session.
    def closeImapSession(self):

        if self.imapSession:
            self.imapSession.close()
            self.imapSession.logout()
            self.imapSession = None

    # quit the SMTP session
    def quitSmtpSession(self):

        if self.smtpSession:
            self.smtpSession.quit()
            self.smtpSession = None

    # return all selectable mailboxes
    def getAllMailboxes(self):

        result, response = self.imapSession.list()

        mailboxes = []
        if result == 'OK':
            for each in response:
                # suppose the response format is somethin like
                # (\Noselect) "/" "[Gmail]"
                if each.find('\\Noselect') >= 0:
                    continue

                folders = re.findall('"(.*)"', each)[0].split('" "')
                mailboxes.append(folders[1])

        return mailboxes

    # get the new messages in a list:
    # each message will be an instance of email.message.Message
    def getNewMessages(self, mailbox='INBOX'):

        # assume we check the new message from INBOX
        result, response = self.imapSession.select(mailbox)
        #print response
        # we are in select state now.
        result, response = self.imapSession.search(None, 'UNSEEN')
        # response should be a string of message number
        #print response
        msgs=[]
        for sequence in response[0].split():
            # get the message and
            result, message = self.imapSession.fetch(sequence, '(RFC822)')
            #print "===================================="
            #print message[0]
            # the email.message.Message format.
            emailMessage = EmailMessage(email.message_from_string(message[0][1]))
            msgs.append((sequence, emailMessage))

        return msgs

    # add flag to a message with the given sequence.
    # this only happen after select a mailbox.
    # there is no return value for this method, since we are using
    # .SILENT suffix.
    def flagMessages(self, seqs, flag):

        for seq in seqs:
            self.imapSession.store(seq, '+FLAGS.SILENT', flag)

        self.imapSession.expunge()

    # return non flagged sent mails
    def getNotFlaggedOutMail(self):

        self.imapSession.select('[Gmail]/Sent Mail')

        typ, msgnums = self.imapSession.search(None, 'NOT', 'FLAGGED')

        for one in msgnums[0].split():
            # fetch each message
            typ, data = self.imapSession.fetch(one, '(RFC822)')
            # print out the message body.
            print 'Message %s\n%s\n' % (one, data[0][1])

    # send message,
    def sendMail(self, fromAddr, toAddr, messageString):

        if self.smtpSession == None:

            return "SMTP Session NOT start!"

        self.smtpSession.sendmail(fromAddr, toAddr, messageString)

# email message class, a wrap class for the email.message.Message.
# we try to provide some easy method t access and build a email
# message.
class EmailMessage(Message):

    """
    """

    # init.
    def __init__(self, message=None):

        self.message = message

        # the plain text message
        self.textPlain = None
        # the html text.
        # attachments: counts, file, payload, etc.

    # return the subject for this message.
    def getSubject(self):

        if self.message:
            return self.message["Subject"]
        else:
            return None

    # return the plain text message from a emal.message.Message.
    def getMessageTextPlain(self):

        # we load it only when we need it.
        if self.textPlain == None:
                
            # we will make sure the main content type is text and
            # the content type is plain/text
            for part in self.message.walk():
                if part.get_content_maintype() != 'text':
                    continue
                if part.get_content_type() != 'text/plain':
                    continue
        
                self.textPlain = part.get_payload(decode=True)
                break

        return self.textPlain;

# utility class to manage the emails in the mailing list.
class EmailRepository(object):

    """
    """

    # init
    # fileName should be a full path name.
    def __init__(self, fileName):

        self.repoFileName = fileName
        self.fileNewLine = None
        # this dict is mainly for maintainence purpose.
        self.emailDict = {}
        # tag as the key and the value is a list of full email
        self.tagDict = {}

        self.loadEmails(self.repoFileName)

    # load emails, full names, tags from the given file.
    def loadEmails(self, fileName):

        # load the file content into memory.
        repoFile = open(fileName)
        try:
            for line in repoFile:
                fullEmail, tags = line.split(';')
                # get name and email separatly
                fullName, email = fullEmail.replace('>', '').split(' <')
                # preparing the taglist.
                tagList = tags.split(',')
                # pop out the new line, which is the last one.
                fileNewLine = tagList.pop()
                if self.fileNewLine == None:
                    self.fileNewLine = fileNewLine
                # build the email dict.
                self.emailDict[email] = (fullName, tagList)

                # build the tag dict, make sure everybody has tag All.
                if not tagList.__contains__('All'):
                    tagList.append('All')
                for tag in tagList:
                    if not self.tagDict.has_key(tag):
                        self.tagDict[tag] = []
                    self.tagDict[tag].append(fullEmail)
        finally:
            repoFile.close()

    # return the full email as a list for the given tag.
    def getEmails(self, tagName='All'):

        return self.tagDict[tagName]

    # add tag to a email address.
    # tags should be a string with ',' as separator.  Its default value
    # will be 'All'
    def tagEmail(self, email, tags='All', fullName=None):

        newTagList = tags.split(',')
        if fullName == None:
            fullName = email.split('@')[0]
        if self.emailDict.has_key(email):
            fullName, tagList = self.emailDict[email]
            newTagList.extend(tagList)
            newTagList = list(set(newTagList))

        self.emailDict[email] = (fullName, newTagList)

    # add a email string address:
    # [full name] <emailaddress>;tag,tag
    def tagEmailStr(self, emailStr):

        emailAndTags = emailStr.split(';')
        fullEmail = emailAndTags[0].replace('>', '').split(' <')
        email = fullEmail[0]

        fullName = None
        if len(fullEmail) > 0:
            email = fullEmail[1]
            fullName = fullEmail[0]

        tags = 'All'
        if len(emailAndTags) > 0:
            tags = emailAndTags[1]

        return self.tagEmail(email, tags, fullName)

    # remove email, normally this is a bad email: could not deliver.
    def removeEmails(self, emailsList):

        for email in emailsList:
            self.emailDict.pop(email, None)

    # remove tags for the given email.
    def removeEmailsTags(self, emailsList, tags):

        removeTagList = tags.split(',')
        for email in emailsList:
            if self.emailDict.has_key(email):
                fullName, tagList = self.emailDict[email]
                for tag in removeTagList:
                    tagList.remove(tag)
                self.emailDict[email] = (fullName, tagList)
            else:
                self.tagEmail(email)

    # save the emails to file.
    def saveEmails(self):

        fileRepo = open(self.repoFileName, 'w')
        for email, nameTags in self.emailDict.iteritems():
            tags = ','.join((','.join(nameTags[1]), self.fileNewLine))
            fileRepo.write('%s <%s>;%s' % (nameTags[0], email, tags))

        fileRepo.flush()
        fileRepo.close()
