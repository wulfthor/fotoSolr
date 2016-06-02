#!/usr/bin/python

import sys
import logging
import pdb
import json
import os
import re
import pdb
import pysolr
import pprint


def runFile(inputFile):

  base=os.path.basename(inputFile)
  name=os.path.splitext(base)
  baseUrl="http://cspic.smk.dk/"
  keepDict=dict()
  outputFile=inputFile + "out"
  sizeDict={'K':1,'KB':1,'M':1024,'MB':1024,'GB':1044480}
  keyList=["modify","Colorspace","Compression","Copyright","Filesize","Format","Image","RawFileName","Image Name","Number pixels","Orientation","Page geometry","Print size","Quality","Resolution","Type","Units"]

  keyListMap={"id":"id","ImageUrl":"imageurl","inputFilename":"name","modify":"date","Colorspace":"colorspace","Compression":"compression","Copyright":"copyright","Filesize":"filesize","Format":"format","Image":"image","RawFileName":"rawfilename","Image Name":"id","Number pixels":"number_of_pixels","Orientation":"orientation","Page geometry":"geometry","Page geometry width":"geometry_width","Page geometry height":"geometry_height","Print size":"printsize","Quality":"quality","Resolution":"resolution","Type":"type","Units":"units"}

  keepDict['inputFilename'] = inputFile.split(".")[0]

  for line in open(inputFile):
    logging.debug("----------------")
    tmpArr=line.split(':')
    if (len(tmpArr) < 2):
      logging.debug("empty line")
      continue
    logging.debug(line + str(len(tmpArr[1])))

    if (len(tmpArr[1]) < 2):
      logging.debug("Has subkey. Skip")
      continue

    if re.search('^\s+[a-z]+:\s*[a-z]+:\s*(.*)',line):
      m=re.match('^\s+([a-z]+):\s*([a-z]+):\s*(.*)',line)
      metatype=m.group(1)
      tmpVal=m.group(3)
      tmpKey=m.group(2)
      logging.debug("meta " + metatype + " val " + tmpVal)
      logging.debug("lowKEY " + tmpKey)
    else:
      tmpKey=tmpArr.pop(0).lstrip()
      tmpVal=':'.join(tmpArr).lstrip().rstrip()
      logging.debug("KEY " + tmpKey)

#Now parse
    if re.search('Filesize',tmpKey):
      print "FIll " + tmpVal
      m=re.search('(\d+\.?\d+)(\w+)',tmpVal)
      logging.debug("Filesize: " + tmpVal)
      tmpVal = int((float(m.group(1)) * sizeDict[m.group(2)]))

    elif re.search('Number pixels',tmpKey):
      m=re.search('(\d+\.?\d*)(\w+)',tmpVal)
      tmpVal = int((float(m.group(1)) * sizeDict[m.group(2)]))

    elif re.search('Resolution',tmpKey):
      tmpVal = tmpVal.split('x')[0]

#Page geometry": "1200x1269+0+0" split for two fields, width & height
    elif re.search('Page geometry',tmpKey):
       m=re.match('(\d+)x(\d+)+',tmpVal)

       keepDict['Page geometry width']= m.group(1)
       keepDict['Page geometry height']= m.group(2)

    elif re.search('Image$',tmpKey):
      tmpUrlArr=tmpVal.split('/')
      tmpUrlArr.pop(0)
      tmpUrlArr.pop(0)
      tmpUrlArr.pop(0)
      tmpUrlArr.pop(0)
      tmpUrl = '/'.join(tmpUrlArr)

      fullUrl=baseUrl + tmpUrl
      keepDict['ImageUrl']=fullUrl

    elif (re.search('Image Name\[2,5\]',tmpKey)):
      keepDict['id'] = tmpVal

    elif (re.search('modify|create',tmpKey)):
      #2005-01-21T11:05:09+01:00
      tmpVal = tmpVal.split("+")[0]
      logging.debug("modifydate: " + tmpVal)


    else:
      logging.debug("no crit for " + line)

    if tmpKey in keyList:
      logging.debug("Assigning " + tmpKey + " to " + str(tmpVal)) 
      keepDict[tmpKey]=tmpVal



    #exif:DateTime:2004:07:28 09:24:42

  #print(json.dumps(keepDict))
  outputDict=dict()

  for k,v in keepDict.iteritems():
    outputDict[keyListMap[k]]=v
    #print "Base: " + str(base)
    #print "P: " + str(name)
    #print "I: " + str(inputFile)

  #print(json.dumps(outputDict))
  jsonArr=json.dumps(outputDict)
  newName = keepDict['inputFilename'] + ".json"
  f = open(newName, 'w')
  print >> f,"["
  print >> f,jsonArr
  print >> f,"]"
  f.close()

  #pprint.pprint(jsonArr)
  logging.debug("------- End ---------\n\n")



def main():
  myhome="/home/drupal"
  logging.basicConfig(filename=myhome+'/logs/prep.log',level=logging.DEBUG)
  inputFile=sys.argv[1]
  runFile(inputFile)

if __name__ == '__main__':
  main()
