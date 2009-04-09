import os
import re

NEWLINE = '\n'

filename = 'trackingfixes'

dssDict = {}

# load tracking info...
# we will build a dict from the tracking file. the key will be the dss thread id.
log = open(filename)
lines = log.read().splitlines()
log.close()
print lines
for line in lines:
    print line

    values = line.split(',')
    dssDict[values[0]] = values

print dssDict

# 1. read the notification email from gmail, using IMAP.
# 2. parse the email message to get brand name, model name, thread id (dssid) and new post page URL.

# 3. login to dssfeedback website.
# 4. open URL for new post page. http://www.dssfeedback.com/forum/thread.php?t=dssid&goto=newpost
url = ''
response, newPost = http.request(url, 'GET', headers=headers)
# 5. parse the new post page to get the latest attachment URL and file name for this thread (model)
#    http://www.dssfeedback.com/forum/attachment.php?attachmentid=1280&d=980283
files = re.findall('<a href="(attachment.php\?attachmentid=[0-9]+\&amp;d=[0-9]+)">(.+)</a>', newPost)
theOne = files.pop()
attachmentUrl = 'http://www.dssfeedback.com/forum/%s' % theOne[0]
# 6. open the URL for the latest attachment and save it as a local file with the filename.
response, content = http.request(attachmentUrl, 'GET', headers=headers)
attachment = open(theOne[1], 'wb')
attachment.write(content)
attachment.close()
# 7. upload into box.net
# 8. update the dssDict with the same dssid:
#    boxfileid, publiclink
# 9. flag the email as readed.


# 4. write everything from dssDict into the same file.
log = open('temp', 'w')
for dssId, dss in dssDict.iteritems():
    log.writelines(','.join(dss))
    log.writelines(NEWLINE)

brandDict = {}
# building the dict in memory before update the blog post as a JSON string.
# We doing this because we need categrize the entry by brand. So all models under
# one brand will sit together.
for dss in dssDict.keys():

    values = dssDict[dss]

    # for each brand is a dict, the key is brand name, values[1]
    brand = {}
    if brandDict.has_key(values[1]):
        brand = brandDict[values[1]]

    # get the model, each model a list of value, 
    model = []
    if brand.has_key(values[2]):
        model = brand[values[2]]

    model = [values[7], values[6]]

    brand[values[2]] = model

    brandDict[values[1]] = brand

print brandDict

# here we will generate the 
wenjiansJson = []
wenjians = []
for brandName, modelDict in brandDict.iteritems():

    print '%s - %s' % (brandName, modelDict)

    wjs = {}
    wjs['bq'] = brandName
    wjs['wjs'] = []
    wenjianModels = []
    for modelName, modelValues in modelDict.iteritems():
        print '\t%s - %s' % (modelName, modelValues)

        wj = {}
        wj['bq'] = '%s (%s)' % (modelName, modelValues[0])
        wj['wj'] = modelValues[1]

        wjs['wjs'].append(wj)
        wenjianModels.append(wj['bq'] + "UUUU" + wj['wj'])

    wenjiansJson.append(wjs)
    wenjians.append(brandName + 'BBBB' + 'MMMM'.join(wenjianModels))

print "--------------------------------------------------"
print wenjiansJson

theData = 'AAAA'.join(wenjians)

print "=================================================="
print theData

