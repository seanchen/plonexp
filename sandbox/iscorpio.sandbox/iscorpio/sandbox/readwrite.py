import os

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

# here we will check the notification for update.
# if there is update, we will
# 1. download it from dss
# 2. upload into box.net
# 3. update the dssDict with the same dssid

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
wenjians = []
for brandName, modelDict in brandDict.iteritems():

    print '%s - %s' % (brandName, modelDict)

    wjs = {}
    wjs['bq'] = brandName
    wjs['wjs'] = []
    for modelName, modelValues in modelDict.iteritems():
        print '\t%s - %s' % (modelName, modelValues)

        wj = {}
        wj['bq'] = '%s (%s)' % (modelName, modelValues[0])
        wj['wj'] = modelValues[1]

        wjs['wjs'].append(wj)

    wenjians.append(wjs)

print "--------------------------------------------------"
print wenjians
        


