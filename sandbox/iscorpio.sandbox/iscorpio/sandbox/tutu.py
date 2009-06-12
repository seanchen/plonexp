# tutu.py

# a mailing list services.

import re
import time
import email
from email.message import Message
import imaplib
import smtplib

import gdata
from gdata import service
from gdata import blogger
import atom

IMAP_MAILHOST = 'imap.gmail.com'
IMAP_PORT = 993
SMTP_MAILHOST = 'smtp.gmail.com'
SMTP_PORT = 587

EMAIL_PATTERN = '%s+%s*@%s+%s*\.(?:%s|%s|%s)' % (('[_a-zA-Z0-9-]',
                                                 '(?:\.[_a-zA-Z0-9-]+)',
                                                 '[a-zA-Z0-9-]',
                                                 '(?:\.[a-zA-Z0-9-]+)',
                                                 '(?:[0-9]{1,3})',
                                                 '(?:[a-zA-Z]{2,3})',
                                                 '(?:aero|coop|info|museum|name)'))

TO_FIRSTNAME = '[TO FIRSTNAME]'
FROM_FIRSTNAME = '[FROM FIRSTNAME]'

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

    def getMessages(self, mailbox='INBOX'):

        # assume we check the new message from INBOX
        result, response = self.imapSession.select(mailbox)
        #print response
        # we are in select state now.
        result, response = self.imapSession.search(None, 'NOT', 'FLAGGED')
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
class EmailMessage(object):

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

# account monitor
class AccountMonitor(object):

    """
    """

    # init.
    def __init__(self, fileName=None, maxMessages=10, maxMsgEachTime=46):

        # the file name.
        if fileName:
            self.accountFileName = fileName

        # the accounts list, a list of tuple:
        # (email, password, full name)
        self.accounts = []

        # max emails allowed to send out for an account.
        self.maxMessagesPerAccount = maxMessages
        self.maxMessagesEachTime = maxMsgEachTime
        # tracking the account sending history.
        # (account index, sending count)
        self.accountTracking = [0, 0]
        # current account for sending. a tuple of from email and
        # an instance of EmailServices
        # (from email, email servies instance)
        self.currentAccount = None

        self.loadAccounts()

    # load the account from the file name.
    def loadAccounts(self):

        accountFile = open(self.accountFileName)

        try:
            for line in accountFile:
                email, password, fullName = line.split('>>>>')
                self.accounts.append((email, password, fullName))
        finally:
            accountFile.close()

    # send email strategically
    def sendEmails(self, toList, message):

        i = 0
        self.accountTracking = [0, 0]
        for to in toList:
            message.__delitem__('To')
            message['To'] = to
            fromEmail, sender = self.getNextSender(i)
            message.__delitem__('From')
            message['From'] = fromEmail

            messageString = message.as_string()
            firstName = to.split()[0]
            messageString = messageString.replace(TO_FIRSTNAME, firstName)
            fromFirst = fromEmail.split()[0]
            messageString = messageString.replace(FROM_FIRSTNAME, fromFirst)

            sender.sendMail(fromEmail, to, messageString)
            print '%4d %s --> %s' % (i, fromEmail, to)
            i = i + 1

        print 'Sent %s messages from %s' % (self.accountTracking[1], self.currentAccount[0])
        if self.currentAccount:
            self.currentAccount[1].quitSmtpSession()

    # return tuple (fromemail, emailService) for the give sequence id.
    def getNextSender(self, index):

        if (index + 1) % self.maxMessagesEachTime == 0:
            if self.currentAccount:
                self.currentAccount[1].quitSmtpSession()
            self.accountTracking[1] = 0
            print 'Sleep at %s ...' % time.strftime('%x %X')
            time.sleep(60 * 10)

        if self.accountTracking[1] == self.maxMessagesPerAccount:
            # reach max.
            print 'Sent %s messages from %s' % (self.accountTracking[1], self.currentAccount[0])
            if self.currentAccount:
                # close the current email service!
                self.currentAccount[1].quitSmtpSession()
            time.sleep(60 * 2)
            # reset
            self.accountTracking[1] = 0
            self.accountTracking[0] = (self.accountTracking[0] + 1) % \
                                      len(self.accounts)

        if self.accountTracking[1] == 0:
            # the first message for this account!
            # get the account and prepare the email service.
            email, password, fullName = self.accounts[self.accountTracking[0]]
            fromEmail = '%s <%s>' % (fullName, email)
            smtp = EmailServices()
            smtp.startSmtpSession(email, password)
            self.currentAccount = (fromEmail, smtp)

        #
        self.accountTracking[1] = self.accountTracking[1] + 1

        return self.currentAccount

    # check undeliverying emails.
    def checkBadEmails(self):

        emailService = EmailServices()
        badEmails = set()
        for account in self.accounts:

            emailService.startImapSession(account[0], account[1])
            print "Checking %s ..." % account[0]

            messages = emailService.getNewMessages()
            for seq, message in messages:
                subject = message.getSubject()
                print "---- %s" % subject

                if self.isBadResponse(subject):
                    messageText = message.getMessageTextPlain()
                    addrs = re.findall(EMAIL_PATTERN, messageText)
                    for one in set(addrs):
                        print ">>>>>>>> %s" % one
                        badEmails.add(one)

                    # flag as read.
                    emailService.flagMessages([seq], "\\Seen")

            # close imap sesion.
            emailService.closeImapSession()

        # return the bad emails set.
        return badEmails

    # check if the email subject is about a bad response.
    def isBadResponse(self, subject):

        if subject:
            title = subject.upper()
        else:
            # default is good response.
            return False

        if title.find('FAILURE') >= 0 or \
           title.find('RETURNED MAIL') >= 0 or \
           title.find('UNDELIVER') >= 0 or \
           title.find('DELIVERY NOTIFI') >= 0:
            return True

        return False

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
        # FistName LastName <email@example.org>
        self.tagDict = {}

        self.loadEmails()

    # load emails, full names, tags from the given file.
    def loadEmails(self):

        # load the file content into memory.
        repoFile = open(self.repoFileName)
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
            # trying to guess the full name.
            fullName = fullName.replace('.', ' ')
            fullName = fullName.replace('_', ' ')
        if self.emailDict.has_key(email):
            fullName, tagList = self.emailDict[email]
            newTagList.extend(tagList)
            newTagList = list(set(newTagList))

        self.emailDict[email] = (fullName, newTagList)

    # add a email string address:
    # [full name] <emailaddress>;tag,tag
    # if don't know full name, should follow this format.
    # emailaddress;tag,tag
    def tagEmailStr(self, emailStr):

        emailAndTags = emailStr.split(';')
        fullEmail = emailAndTags[0].replace('>', '').split(' <')
        email = fullEmail[0]

        fullName = None
        if len(fullEmail) > 1:
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

# class to provide easy interfaces to access GDataService Blogger APIs.
class BlogspotService(object):

    """
    the blog
    """

    # the init
    def __init__(self, username, password):

        self.gdService = service.GDataService(username, password)
        self.gdService.source = 'Blogger_Python_Sample-1.0'
        self.gdService.service = 'blogger'
        self.gdService.server = 'www.blogger.com'
        self.gdService.ProgrammaticLogin()

        # keep a list of blogs.
        self.listBlogs()

    # return a list of blogs under current user.
    def listBlogs(self):

        self.blogs = []
        feed = self.gdService.Get('/feeds/default/blogs')
        for eachBlog in feed.entry:
            title = eachBlog.title.text
            link = eachBlog.GetSelfLink()
            blogId = link.href.split('/')[-1]
            self.blogs.append((title, blogId))

        return self.blogs

    # select a blog under this user by the given blog title.
    # the title is case insenstive.
    def selectBlog(self, title=None):

        if title:
            for blogTitle, blogId in self.blogs:
                # should not care about case!
                if blogTitle.upper() == title.upper():
                    self.blogId = blogId
                    break
        else:
            # returns the first blog if no title provided.
            self.blogId = self.blogs[0][1]

        self.postsUri = '/feeds/%s/posts/default' % self.blogId

        return self.blogId

    # create a post!
    def createPost(self, title, content, authorName,
                   labels=None, isDraft=False):

        # Create a gdata entry.
        entry = gdata.GDataEntry()
        # append author.
        entry.author.append(atom.Author(atom.Name(text=authorName)))
        entry.title = atom.Title(title_type='xhtml', text=title)

        # handle labels by using atom.Category.
        if labels:
            for label in labels:
                category = atom.Category(scheme=blogger.LABEL_SCHEME,term=label)
                entry.category.append(category)

        # handle draft,
        if isDraft:
            control = atom.Control()
            control.draft = atom.Draft(text='yes')
            entry.control = control

        # add content.
        entry.content = atom.Content(content_type='html', text=content)

        return self.gdService.Post(entry, self.postsUri)

    # return posts a list.
    # labels:
    #   a list of labels.
    # publishedDate:
    #   (published_min, published_max)
    def getPosts(self, labels=None, publishedDate=None, orderby=None, maxResults=25):

        posts = []

        query = service.Query()
        query.feed = self.postsUri
        
        # default sort option is updated.
        query.orderby = 'updated'
        if orderby:
            query.orderby = orderby

        # adding labels for the query.
        if labels:
            query.categories = labels

        # adding publication range for the query.
        if publishedDate:
            # the time format should be like this:
            # 2008-02-09T08:00:00-08:00
            query.published_min = publishedDate[0]
            query.published_max = publishedDate[1]

        query.max_results = maxResults

        feed = self.gdService.Get(query.ToUri())

        for entry in feed.entry:
            
            posts.append((entry.title.text,
                          entry.GetSelfLink().href,
                          entry.GetAlternateLink().href))

        return posts

    # update labels for posts, find all posts for the given labels and
    # update them with the new labels.
    def updateLabels(self, labels, newLabels):

        query = service.Query()
        query.feed = self.postsUri
        query.max_results = 10000
        if labels:
            query.categories = labels

        feed = self.gdService.Get(query.ToUri())

        newCategory = []
        if newLabels:
            for label in newLabels:
                category = atom.Category(scheme=blogger.LABEL_SCHEME,term=label)
                newCategory.append(category)

        for entry in feed.entry:
            while len(entry.category) > 0:
                entry.category.pop()
            entry.category = newCategory
            editUri = entry.GetEditLink().href
            self.gdService.Put(entry, editUri)

        return newCategory
