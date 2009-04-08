# dss.py

# the class to handle the http request to dss website.

import re
import urllib
import httplib2

import logging

logger = logging.getLogger('DSS')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

class MyDss(object):

    LOGIN_URL = 'http://www.dssfeedback.com/forums/login.php?do=login'

    def __init__(self):

        # headers for HTTP request. we will use it to save Cookies.
        self.headers = {}
        # an instance of httplib2.Http, with cache support.
        self.http = httplib2.Http(".cache")
        #self.http = httplib2.Http()

    def login(self, username, password):

        # prepare the login form data.
        loginForm = {}
        loginForm['vb_login_username'] = username
        loginForm['vb_login_password'] = password
        loginForm['do'] = 'login'
        loginForm['url'] = '/'
        loginForm['s'] = ''
        loginForm['securitytoken'] = 'guest'
        loginForm['cookieuser'] = '1'

        self.headers['Content-type'] = 'application/x-www-form-urlencoded'
        response, content = self.http.request(self.LOGIN_URL, 'POST', headers=self.headers,
                                              body=urllib.urlencode(loginForm))

        logger.info('----------------------------RESPONSE-----------------------')
        logger.info(response)
        logger.debug(content)

        self.headers = {}
        self.headers['Cookie'] = response['set-cookie']
        #self.headers['Connection'] = response['connection']
        self.headers['cache-control'] = 'no-cache'

        return self.headers

    # get content from the given url.
    def getUrlContent(self, url):

        response, content = self.http.request(url, 'GET', headers=self.headers)
        logger.debug('------------------------CONTENT-------------------------------')
        logger.debug(content)

        return content

    # return keys from dss homepage.
    def getKeys(self):

        url = 'http://www.dssfeedback.com/'
        content = self.getUrlContent(url)

        # parse the homepage to get the keys.
        keys = {}
        keys['DISH0101'] = re.findall('<!-- ZZZ --> ([0-9A-F]*)[ ]?([New]*)', content)
        keys['DISH0106'] = re.findall('<!-- YYY --> ([0-9A-F]*)[ ]?([New]*)', content)
        keys['BELL0901'] = re.findall('<!-- XXX --> ([0-9A-F]*)[ ]?([New]*)', content)
        keys['BELL0907'] = re.findall('<!-- PPP --> ([0-9A-F]*)[ ]?([New]*)', content)
        logger.info('keys = %s' % keys)

        key0 = keys['DISH0101'][0]
        key1 = keys['DISH0101'][1]
        dish0101 = '<strong>DISH 0101</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

        key0 = keys['DISH0106'][0]
        key1 = keys['DISH0106'][1]
        dish0106 = '<strong>DISH 0106</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

        key0 = keys['BELL0901'][0]
        key1 = keys['BELL0901'][1]
        bell0901 = '<strong>BELL 0901</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

        key0 = keys['BELL0907'][0]
        key1 = keys['BELL0907'][1]
        bell0907 = '<strong>BELL 0907</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

        new_content = dish0101 + dish0106 + bell0901 + bell0907

        return new_content

    # return the latest the attachment for a model.
    def saveAttachment(self, newPostUrl):

        content = self.getUrlContent(newPostUrl)

        allAttachments = re.findall('<a href="(attachment.php\?attachmentid=[0-9]+\&amp;d=[0-9]+)">(.+)</a>',
                                    content)
        attachment = allAttachments.pop()
        logger.info('Latest Attachment: ')
        logger.info(attachment)

        attachmentUrl = 'http://www.dssfeedback.com/forums/%s' % attachment[0]
        logger.info('Attachment URL: %s' % attachmentUrl)

        data = self.getUrlContent(attachmentUrl)
        f = open(attachment[1], 'wb')
        f.write(data)
        f.close()

        return (attachment[1], attachmentUrl)
