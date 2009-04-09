# dss.py

# the class to handle the http request to dss website.

import re
import urllib
import httplib2
import time

import logging

from iscorpio.sandbox.mynetbox import BoxDotNet

logger = logging.getLogger('DSS')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

class MyDss(object):

    LOGIN_URL = 'http://www.dssfeedback.com/forums/login.php?do=login'

    BOX_SHARED_ROOT = 'http://www.box.net/shared/'

    def __init__(self, boxApiKey='', boxUser='', boxPassword=''):

        # headers for HTTP request. we will use it to save Cookies.
        self.headers = {}
        # an instance of httplib2.Http, with cache support.
        self.http = httplib2.Http(".cache")
        #self.http = httplib2.Http()

        # the default dss dict should be empty.
        self.dssDict = {}

        self.boxApiKey = boxApiKey
        self.boxUser = boxUser
        self.boxPassword = boxPassword

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
        fileName = '/tmp/' + attachment[1]
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

        return (fileName, attachmentUrl)

    # load current file dict from the given content.
    # model = [modelname (updatetime)]IIII[dssId]IIII[boxId]UUUU[public_link]
    # brand = [brandname]BBBB[model1]MMMM[model2]
    # [brand1]AAAA[brand2]
    def loadCurrentDict(self, postContent):

        # {dssid : [brandname, modelname, dssid, boxid, public_link]}
        # one record for each model.
        self.dssDict = {}
        for brand in postContent.split('AAAA'):

            aBrand = brand.split('BBBB')
            brandName = aBrand[0].upper()
            models = aBrand[1]

            for model in models.split('MMMM'):

                aModel = model.split('UUUU')
                modelInfo = aModel[0].split('IIII')
                modelName = modelInfo[0]
                modelDssId = modelInfo[1]
                modelBoxId = modelInfo[2]
                # public_link for this model.
                modelUrl = aModel[1]

                self.dssDict[modelDssId] = [brandName, modelName,
                                            modelDssId, modelBoxId,
                                            modelUrl]

        return self.dssDict

    # build the post content and return it.
    def getPostContent(self):

        if not self.dssDict:
            return ''

        # we need categorize it by brand name
        brandDict = {}
        for dssId, dssValues in self.dssDict.iteritems():
            brandName = dssValues[0]
            # each brand will be dict.
            models = []
            # check by brand name, if it's exist then we pick it up.
            if brandDict.has_key(brandName):
                models = brandDict[brandName]
            else:
                brandDict[brandName] = models

            models.append([dssValues[1], dssValues[2], dssValues[3],
                           dssValues[4]])

        logger.info('BRAND DICT: %s' % brandDict)

        wenjiansJson = []
        wenjians = []
        for brandName, modelList in brandDict.iteritems():

            logger.info('%s - %s' % (brandName, modelList))

            wjs = {}
            wjs['bq'] = brandName,
            wjs['wjs'] = []
            wjModels = []
            for modelInfo in modelList:
                logger.info('\t%s' % modelInfo)

                wj = {}
                wj['bq'] = '%sIIII%sIIII%s' % (modelInfo[0],
                                               modelInfo[1],
                                               modelInfo[2])
                wj['wj'] = modelInfo[3]

                wjs['wjs'].append(wj)
                wjModels.append('%sUUUU%s' % (wj['bq'], wj['wj']))

            wenjiansJson.append(wjs)
            wenjians.append(brandName + 'BBBB' + 'MMMM'.join(wjModels))

        logger.info('WENJIANS: %s', wenjians)
        logger.info('WENJIANS JSON: %s', wenjiansJson)
        
        return 'AAAA'.join(wenjians)
    
    # process the given new posts: a list of dict.
    # each post should have the following info:
    # dssid : 1234
    # brandname : VIEWSAT
    # modelname : ULTRA
    # newposturl : http://www.dssfeedback.com/forums/showthread.php?t=34565&goto=newpost
    def processNewPosts(self, newPosts):

        # preparing my box.
        mybox = BoxDotNet()
        mybox.login(self.boxApiKey, self.boxUser, self.boxPassword)

        for post in newPosts:

            logger.info('Processing %s', post)

            today = time.strftime('%Y-%m-%d')
            modelName = '%s (%s)' % (post['modelName'], today)

            # save the new attachment in local.
            fileName, attachmentUrl = self.saveAttachment(post['newPostUrl'])
            response = mybox.upload(fileName, auth_token=mybox.token,
                                    folder_id='0', share='1')
            boxId = response.files[0].file[0]['id']
            publicLink = self.BOX_SHARED_ROOT + response.files[0].file[0]['public_name']

            dssId = post['dssId']
            if self.dssDict.has_key(dssId):
                dssInfo = self.dssDict[dssId]
                # update some fields:

                # model name update to today
                dssInfo[1] = modelName
                if boxId != dssInfo[3]:
                    # remove the exist file on my box.
                    mybox.delete(api_key=mybox.apiKey,
                                 auth_token=mybox.token,
                                 target='file',
                                 target_id=dssInfo[3])
                    dssInfo[3] = boxId
                # update the new box public_link
                dssInfo[4] = publicLink
            else:
                dssInfo = []
                dssInfo.append(post['brandName'])
                dssInfo.append(modelName)
                dssInfo.append(dssId)
                dssInfo.append(boxId)
                dssInfo.append(publicLink)
                # add to the dss dict.
                self.dssDict[dssId] = dssInfo

            logger.info("Updated %s" % self.dssDict[dssId])

        # log out my box.
        mybox.logout(api_key=mybox.apiKey,
                     auth_token=mybox.token)

        return self.dssDict
