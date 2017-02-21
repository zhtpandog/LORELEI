from __future__ import division
import json
import operator
import os
import numpy as np
from collections import Counter
import pandas as pd


############################################ data prep ##########################################################

uuidAndWCLower = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/uuidAndWCLower.json').read())
uuidAndEntitiesLower = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/uuidAndEntitiesLower.json').read())
uuid = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/uuid.json').read())


uuidAndDates = {}
uuidAnddisaster_name = {}
uuidAndTopics = {}
topicsSet = set()
path = r'/Users/ZhangHaotian/desktop/LO/reliefWebProcessed'
for fileName in os.listdir(path)[1:]:
    my_data = json.loads(open(path + '/' + fileName).read())
    subdata_loreleiJSONMapping = my_data['loreleiJSONMapping']
    subdata_topics = subdata_loreleiJSONMapping['topics']
    uuidAndTopics[my_data['uuid']] = subdata_topics
    topicsSet = topicsSet | set(subdata_topics)
    subdata_sourcedata = subdata_loreleiJSONMapping['sourcedata']
    subdata_date = subdata_sourcedata['date_created']
    uuidAndDates[my_data['uuid']] = subdata_date
    subdata_disname = subdata_sourcedata['disaster_name']
    uuidAnddisaster_name[my_data['uuid']] = subdata_disname

uuidAndDateTime = {}
for i,j in uuidAndDates.items():
    uuidAndDateTime[i] = pd.Timestamp(j)
uuidAndDateTimeSorted = sorted(uuidAndDateTime.items(), key=operator.itemgetter(1))

uuidAnddisaster_name_cleaned = {} # 1728
for i,j in uuidAnddisaster_name.items():
    if len(j) != 0:
        uuidAnddisaster_name_cleaned[i] = j

uuidAnddisaster_name_cleaned_lower = {} # 1728
for i,j in uuidAnddisaster_name_cleaned.items():
    temp = []
    for k in j:
        temp.append(k.lower())
    uuidAnddisaster_name_cleaned_lower[i] = temp

entityLowerSet = set()  # 48566
for i, j in uuidAndEntitiesLower.items():
    entityLowerSet = entityLowerSet | set(j)

uuidAndTopics_cleaned = {} # 4499 uuids have topic field
for i,j in uuidAndTopics.items():
    if len(j) > 0:
        uuidAndTopics_cleaned[i] = j

uuidAndEntitiesLower_cleaned = {} # 6260 uuids have entity field
for i,j in uuidAndEntitiesLower.items():
    if len(j) > 0:
        uuidAndEntitiesLower_cleaned[i] = j

############################################ data prep ##########################################################


# entityAndFreq stores entity name and its frequency
entityAndFreq = {}
uuidAndNumEntity = {}

for i,j in uuidAndEntitiesLower.items():
    if len(j) > 0:
        uuidAndNumEntity[i] = len(j)
        for k in j:
            if k not in entityAndFreq:
                entityAndFreq[k] = 0
            else:
                entityAndFreq[k] += 1
    else:
        uuidAndNumEntity[i] = 0

# sorted_eAF is a list and each entry in the list is a tuple contains entity name and its frequency
sorted_eAF = sorted(entityAndFreq.items(), key=operator.itemgetter(1), reverse=True)
# sorted_eAN is a list and each entry in the list is a tuple contains uuid and its number of entities
sorted_uAN = sorted(uuidAndNumEntity.items(), key=operator.itemgetter(1), reverse=True)


##################################### Everything about disaster statistics ######################################

# get disaster names in string
disasterNamesString = []
for i,j in uuidAnddisaster_name_cleaned_lower.items():
    for k in j:
        disasterNamesString.append(k)

# get frequency of each disaster
disasterCnt = Counter(disasterNamesString)
disasterCntList = disasterCnt.items()
disasterCntSorted = sorted(disasterCntList,key=lambda tup: tup[1], reverse=True) # 688

# each disaster and its related uuids
disasterAndUuid = {}
for i,j in uuidAnddisaster_name_cleaned_lower.items():
    for k in j:
        if k in disasterAndUuid:
            disasterAndUuid[k].append(i)
        else:
            disasterAndUuid[k] = [i]

disasterAndUuidSorted = sorted(disasterAndUuid.items(), key=lambda x: len(x[1]), reverse=True)

disasterAndUuidSortedFinal = [] # disaster name ordered, from most popular to least, not in dict
for i in disasterAndUuidSorted:
    disasterAndUuidSortedFinal.append((i[0], sorted(i[1],key=uuidAndDateTime.get))) # disasterAndUuidSortedFinal useful

disasterAndUuidSortedFinalDict = {} # disaster name unordered, in dict
for i in disasterAndUuidSortedFinal:
    disasterAndUuidSortedFinalDict[i[0]] = i[1]

disasterAndTimeSpan = {}
for i,j in disasterAndUuidSortedFinalDict.items():
    temp['start'] = uuidAndDateTime[j[0]]
    temp['end'] = uuidAndDateTime[j[-1]]
    disasterAndTimeSpan[i] = temp

with open('disasterAndUuidSortedFinalDict.json', 'w') as f:
    json.dump(disasterAndUuidSortedFinalDict, f)

##################################### Everything about disaster statistics ######################################

###################################### Everything about topic statistics ########################################

topicString = []
for i,j in uuidAndTopics_cleaned.items():
    for k in j:
        topicString.append(k)

topicCnt = Counter(topicString)
topicCntList = topicCnt.items()
topicCntSorted = sorted(topicCntList,key=lambda tup: tup[1], reverse=True)

topicAndUuid = {}
for i,j in uuidAndTopics_cleaned.items():
    for k in j:
        if k in topicAndUuid:
            topicAndUuid[k].append(i)
        else:
            topicAndUuid[k] = [i]

topicAndUuidSorted = sorted(topicAndUuid.items(), key=lambda x: len(x[1]), reverse=True)

topicAndUuidSortedFinal = [] # disaster name ordered, from most popular to least, not in dict
for i in topicAndUuidSorted:
    topicAndUuidSortedFinal.append((i[0], sorted(i[1],key=uuidAndDateTime.get))) # disasterAndUuidSortedFinal useful

topicAndUuidSortedFinalDict = {} # disaster name unordered, in dict
for i in topicAndUuidSortedFinal:
    topicAndUuidSortedFinalDict[i[0]] = i[1]

with open('topicAndUuidSortedFinalDict.json', 'w') as f:
    json.dump(topicAndUuidSortedFinalDict, f)

#
topicAndTimeSpan = {}
for i,j in topicAndUuidSortedFinalDict.items(): # j is a list of uuids
    temp = {}
    temp['start'] = uuidAndDateTime[j[0]]
    temp['end'] = uuidAndDateTime[j[-1]]
    topicAndTimeSpan[i] = temp
with open('topicAndTimeSpan.json', 'w') as f:
    json.dump(topicAndTimeSpan, f)

topicAndTimeSpanNew = {}
for i,j in topicAndUuidSortedFinalDict.items(): # i is each topic, j is ralated uuids
    times = []
    for k in j: # k is one uuid
        try:
            for x in uuidAnddisaster_name_cleaned_lower[k]: # x is each disaster name string
                times.append(int(x[-4:]))
                times.append(int[x[-9:-5]])
        except:
            pass
    times = sorted(times)
    topicAndTimeSpanNew[i] = (times[0], times[-1])



topicAndUniqueWords = {}
topicAndUniqueEntities = {}
cnt = 0
tot = len(topicAndUuid)
for i,j in topicAndUuid.items():
    wordSet = set()
    entitySet = set()
    for k in j: # for each uuid
        wordSet = wordSet | set(uuidAndWCLower[k])
        entitySet = entitySet | set(uuidAndEntitiesLower[k])
    topicAndUniqueWords[i] = wordSet
    topicAndUniqueEntities[i] = entitySet
    cnt += 1
    print cnt / tot

uuidAndUniqueWordCnt = {}
for i,j in topicAndUniqueWords.items():
    uuidAndUniqueWordCnt[i] = len(j)
uuidAndUniqueWordCntSorted = sorted(uuidAndUniqueWordCnt.items(), key=operator.itemgetter(1), reverse=True)

uuidAndUniqueEntityCnt = {}
for i,j in topicAndUniqueEntities.items():
    uuidAndUniqueEntityCnt[i] = len(j)
uuidAndUniqueEntityCntSorted = sorted(uuidAndUniqueEntityCnt.items(), key=operator.itemgetter(1), reverse=True)


###################################### Everything about topic statistics ########################################

##################################### Everything about entity statistics ########################################

# get disaster names in string
entityString = []
for i,j in uuidAndEntitiesLower_cleaned.items():
    for k in j:
        entityString.append(k)

# get frequency of each disaster
entityCnt = Counter(entityString)
entityCntList = entityCnt.items()
entityCntSorted = sorted(entityCntList,key=lambda tup: tup[1], reverse=True) # 48566

# each disaster and its related uuids
entityAndUuid = {}
for i,j in uuidAndEntitiesLower_cleaned.items():
    for k in j:
        if k in entityAndUuid:
            entityAndUuid[k].append(i)
        else:
            entityAndUuid[k] = [i]

entityAndUuidSorted = sorted(entityAndUuid.items(), key=lambda x: len(x[1]), reverse=True)

entityAndUuidSortedFinal = [] # disaster name ordered, from most popular to least, not in dict
for i in entityAndUuidSorted:
    entityAndUuidSortedFinal.append((i[0], sorted(i[1],key=uuidAndDateTime.get))) # disasterAndUuidSortedFinal useful

entityAndUuidSortedFinalDict = {} # disaster name unordered, in dict
for i in entityAndUuidSortedFinal:
    entityAndUuidSortedFinalDict[i[0]] = i[1]

with open('entityAndUuidSortedFinalDict.json', 'w') as f:
    json.dump(entityAndUuidSortedFinalDict, f)

##################################### Everything about entity statistics ########################################