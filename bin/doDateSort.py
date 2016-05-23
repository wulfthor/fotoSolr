#!/usr/bin/python

import sys
import os
import re
import pdb
import solr
import pysolarized
import logging
import pprint
import datetime as dt


'''
date:modify: 2014-10-28T14:58:31+01:00 globus_catsdb_an_image.jpg.txt
date:modify: 2014-10-29T12:51:22+01:00 globus_catsdb_copy3.jpg.txt
date:modify: 2014-10-30T14:58:04+01:00 globus_catsdb_copy4.jpg.txt
date:modify: 2014-10-29T10:26:51+01:00 globus_catsdb_copy.jpg.txt
date:modify: 2014-10-28T14:59:39+01:00 globus_catsdb_kms4340.jpg.txt

'''


def utf8(str):
  return unicode(str, "iso-8859-1").encode("utf-8")

def runFile(myFile):
  myOutFile = str(myFile) + "_res"
  lines = myFile.readlines()
  mytmpDict = dict()
  myOutArr = []
  myres = ""
  prevDate = "1990-10-28 14:58:31"
  dt_obj_old = dt.datetime.strptime(prevDate, '%Y-%m-%d %H:%M:%S')

  for line in lines:
    logging.debug("into .." + line)
    parts = line.split(' ')
    logging.debug("p " + parts[1])
    m = re.match('([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})T([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})(.*)',parts[1])
    if m:
      newts=m.group(1) + " " + m.group(2)
      key=parts[2].rstrip()
      dt_obj_try = dt.datetime.strptime(newts, '%Y-%m-%d %H:%M:%S')
      logging.debug("new things " + str(dt_obj_try))
      logging.debug("old things " + str(dt_obj_old))
      if (dt_obj_try > dt_obj_old):
        dt_obj_old = dt_obj_try
        mytmpDict[key]=str(dt_obj_try)
        myres = key
        logging.debug("change keythings " + key)
        logging.debug("change tsthings " + newts)
      else:
        logging.debug("keep keythings " + key)
        logging.debug("keep tsthings " + str(dt_obj_old))
      
    else:
      logging.debug("no match " + line)

  #pprint.pprint(mytmpDict)
  print "mv " + myres + " .."


def main():
  myFile = open(sys.argv[1], 'r')
  myhome = "/home/drupal"
  logging.basicConfig(filename=myhome+'/logs/thw.log',level=logging.DEBUG)
  runFile(myFile)
  logging.debug("done " + str(myFile))
  myFile.close()

if __name__ == '__main__':
  main()
