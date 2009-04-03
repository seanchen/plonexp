#!/usr/bin/python

import smtplib
import imaplib

username = 'user'
password = 'password'
targetEmail = 'email'

# ACCESS Gmail by SMTP
session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.ehlo()
print session.login(username, password)

# IMAP access
imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
print imap.login(username, password)
# select the folder, the list() function will list all folders.
print imap.select('[Gmail]/Sent Mail')
# search all messages.
typ, msgnums = imap.search(None, 'NOT','FLAGGED')

for num in msgnums[0].split():
    # fetch each message
    typ, data = imap.fetch(num, '(RFC822)')
    # print out the message body.
    print 'Message %s\n%s\n' % (num, data[0][1])

    # forward to another email through SMTP
    print '-------------------- %s' % session.sendmail(username,
                                                       [targetEmail],
                                                       data[0][1])
    # flat it as FLAGGED
    imap.store(num, '+FLAGS', '\\Flagged')

imap.close()
