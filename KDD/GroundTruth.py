# get disaster names in string
disasterNames = uuidAnddisaster_name.values()

disasterNamesNotNone = []
disasterNameIsNoneUuid = []

for i,j in uuidAnddisaster_name.items():
    if len(j) > 0:
        disasterNamesNotNone.append(j)
    else:
        disasterNameIsNoneUuid.append(i)

disasterNamesString = []
for i in disasterNamesNotNone:
    for j in i:
        disasterNamesString.append(j)

# get frequency of each disaster
disasterCnt = Counter(disasterNamesString)
disasterCntList = disasterCnt.items()
disasterCntSorted = sorted(disasterCntList,key=lambda tup: tup[1], reverse=True) # disasterCntSorted useful

# each disaster and its related uuids
disasterAndUuid = {}
for i,j in uuidAnddisaster_name.items():
    if len(j) > 0:
        for k in j:
            if k in disasterAndUuid:
                disasterAndUuid[k].append(i)
            else:
                disasterAndUuid[k] = [i]

disasterAndUuidSorted = sorted(disasterAndUuid.items(), key=lambda x: len(x[1]), reverse=True)

disasterAndUuidSortedFinal = []
for i in disasterAndUuidSorted:
    disasterAndUuidSortedFinal.append((i[0], sorted(i[1],key=uuidAndDateTime.get))) # disasterAndUuidSortedFinal useful

disasterAndUuidSortedFinalDict = {}
for i in disasterAndUuidSortedFinal:
    disasterAndUuidSortedFinalDict[i[0]] = i[1]

with open('relatedDisasterDocs.json', 'w') as f:
    json.dump(disasterAndUuidSortedFinalDict, f)