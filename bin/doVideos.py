#!/usr/bin/python

import sys
import json
from datetime import datetime
import csv

'''
YYYY-MM-DDThh:mm:ssZ
import datetime
.strftime('%Y-%m-%dT%H:%M:%SZ')
'''

# Open the CSV
log = open("/Users/thw/logs/log.txt","a")
log.write("----------------\n")
f = open( sys.argv[1], 'rU' )
outfiletmpName = sys.argv[1] + ".csv"
outfileDir = "/Users/thw/tmp"
outfileName = outfileDir + "/" + outfiletmpName
log.write(outfileName)

'''
fullpath,atime,mtime,ctime,size,type
./FilmArkiv/.DS_Store,1326901782,1466584327,1255434121,14340,Regular File
./FilmArkiv/._videoblog alias,1266311103,1264608273,1264605924,522429,Regular File
./FilmArkiv/abildgaard/.DS_Store,1294323374,1423477312,1250072066,6148,Regular File
./FilmArkiv/abildgaard/._Clip #11.mov,1264605607,1255442204,1255442204,4096,Regular File
'''

data = csv.DictReader(f,delimiter='%')
dataCopy = []
dataCopy = list(data)

#result = [max(g, key=lmb) for k,g in groups]
tmpRowM = ""
tscollection = []
vmdict = dict()
totalList = []
tmpRowM = ""

for row in dataCopy:
    teststring = json.dumps(row)
    if len(row) > 6:
        log.write("Escapechar in path: " + teststring + "\n")
        continue
    tmpRowDict = row;
    tmpRes=row['fullpath'].split("/")[-1:]
    tmpRowDict['name']=tmpRes[0]
    tmpRes2=tmpRes[0].split(".")[-1:]
    tmpRowDict['ext']=tmpRes2[0]
    tmpRowDict['path']='/'.join(row['fullpath'].split("/")[:-1])
    tmpRowDict['accesstime']=datetime.fromtimestamp(float(row['atime'])).strftime('%Y-%m-%dT%H:%M:%SZ')
    tmpRowDict['modifytime']=datetime.fromtimestamp(float(row['mtime'])).strftime('%Y-%m-%dT%H:%M:%SZ')
    tmpRowDict['createtime']=datetime.fromtimestamp(float(row['ctime'])).strftime('%Y-%m-%dT%H:%M:%SZ')
    totalList.append(tmpRowDict)

header = tmpRowDict.keys()

with open(outfileName, 'w') as outfile:
    fp = csv.DictWriter(outfile, header)
    fp.writeheader()
    for nrow in totalList:
        try:
            fp.writerow(nrow)
        except:
            pass

log.write("\ncloseing")
outfile.close()
f.close()
log.close()
