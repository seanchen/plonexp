#! /usr/local/bin/python

import urllib
import httplib2
import re

from gdata import service
import gdata
import atom

url = 'http://www.dssfeedback.com/forums/login.php?do=login'
body = {}
body['vb_login_username'] = 'user'
body['vb_login_password'] = 'password'
body['do'] = 'login'
body['url'] = '/'
body['s'] = ''
body['securitytoken'] = 'guest'
body['cookieuser'] = '1'
headers = {'Content-type': 'application/x-www-form-urlencoded'}

# NOTE:
# we have to enable cache here to use the cookies.
http = httplib2.Http(".cache")
response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

print "RESPONSE: %s" % response
print "Login CONTENT: %s" % len(content)

headers['Cookie'] = response['set-cookie']
headers['cache-control'] = 'no-cache'
headers['pragma'] = 'private'
#headers['Cookie'] = 'bbsessionhash=4dc6dac6ba33a9496db3857d5d1db2bb; path=/; HttpOnly, bblastvisit=1234964504; expires=Thu, 18-Feb-2010 13:41:44 GMT; path=/, bblastactivity=0; expires=Thu, 18-Feb-2010 13:41:44 GMT; path=/'

url = 'http://www.dssfeedback.com/'
response, content = http.request(url, 'GET', headers=headers)

print "HOMEPAGE CONTENT:\n\r %s" % len(content)
homepage = file('./homepage.html', 'w')
homepage.write(content)
homepage.close()

# parse the homepage to get the keys.
keys = {}
keys['DISH0101'] = re.findall('<!-- ZZZ --> ([0-9A-F]* [New]*)', content)
keys['DISH0106'] = re.findall('<!-- YYY --> ([0-9A-F]* [New]*)', content)
keys['BELL0901'] = re.findall('<!-- XXX --> ([0-9A-F]* [New]*)', content)
keys['BELL0907'] = re.findall('<!-- PPP --> ([0-9A-F]* [New]*)', content)
print keys

key0 = keys['DISH0101'][0].split(' ')
key1 = keys['DISH0101'][1].split(' ')
dish0101 = '<strong>DISH 0101</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

key0 = keys['DISH0106'][0].split(' ')
key1 = keys['DISH0106'][1].split(' ')
dish0106 = '<strong>DISH 0106</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

key0 = keys['BELL0901'][0].split(' ')
key1 = keys['BELL0901'][1].split(' ')
bell0901 = '<strong>BELL 0901</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

key0 = keys['BELL0907'][0].split(' ')
key1 = keys['BELL0907'][1].split(' ')
bell0907 = '<strong>BELL 0907</strong><br/><em>key0 </em><strong>%s</strong><br/>%s<br/><em>key1 </em><strong>%s</strong><br/>%s<br/>' % (key0[1], key0[0], key1[1], key1[0])

new_content = dish0101 + dish0106 + bell0901 + bell0907

# login...
selfservice = service.GDataService('user', 'password')
selfservice.source = 'Blogger_Python_Sample-1.0'
selfservice.service = 'blogger'
selfservice.server = 'www.blogger.com'
selfservice.ProgrammaticLogin()

# Get the blog ID for the first blog.
feed = selfservice.Get('/feeds/default/blogs')
self_link = feed.entry[0].GetSelfLink()
if self_link:
    selfblog_id = self_link.href.split('/')[-1]

# find the update entry.
query = service.Query()
query.feed = '/feeds/' + selfblog_id + '/posts/default'
query.published_min = "2008-02-17T14:00:00-08:00"
query.published_max = "2008-02-18T00:00:00-08:00"
#query.orderby = 'published'
feed = selfservice.Get(query.ToUri())

print query.ToUri()
print feed.title.text
print feed.entry
for entry in feed.entry:
    print '\t' + entry.title.text
# should have only one entry.
theEntry = feed.entry[0]

# update the post on server side.
theEntry.content = atom.Content(content_type='html', text=new_content)
selfservice.Put(theEntry, theEntry.GetEditLink().href)

# try to download the attachment!
url = 'http://www.dssfeedback.com/forums/attachment.php?attachmentid=19857&d=1233716275'
response, content = http.request(url, 'GET', headers=headers)
print 'attach files: %s' % len(content)
