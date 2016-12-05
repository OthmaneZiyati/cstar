# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:21:48 2016

This Python script generates csv files with various statistics about users
computed from proxy log data

@author: Antony Bernadou & Louis Melliorat
"""

import csv
import os
import glob
import datetime as dt
import logging as logg
import time

from esec_userbase_util import Log
from esec_userbase_util import User

workspace="C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU"
#workspace="D:/Users/abernado/Documents/8. CODE/PYTHON/201602.ESEC.CYBERSECU/"
os.chdir(workspace)

logger = logg.getLogger('root')  # create logger
logger.setLevel(logg.DEBUG)
handler = logg.FileHandler("./logs/ESEC_USERBASE.log")
handler.setLevel(logg.DEBUG)
# create a logging format
formatter = logg.Formatter('[%(asctime)s - %(name)s - %(funcName)s] - \
                                   %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if len(logger.handlers)==0: # To avoid adding handler for each execution
    logger.addHandler(handler)

logger.info("===========================================")
logger.info("Starting file processing")
logger.info("===========================================")
starttime = time.time()
logger.info("Setting workspace directory")
workspace="C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU"
#workspace="D:/Users/abernado/Documents/8. CODE/PYTHON/201602.ESEC.CYBERSECU/"
os.chdir(workspace)
logger.info("Creating list of input files")

workspace_logs = "D:/Users/lmellior/Desktop/Logs picviz/aclog*.s"
listInputFiles = glob.glob(workspace_logs)
#listInputFiles = glob.glob(workspace+"/data/logs/test200/aclog*.s")
cmpt_file = 0
prevday = 0
nb_files = len(listInputFiles)
logger.info("Creating dictionnary of users")
dictUsers = dict()

def writeuserbase(day):
    ''' For each user in the user dictionnary, this function create a row
    in a csv file where colomns are feature
    There is one csv file per day'''
    global dictUsers
    if (dictUsers != {}) & (len(dictUsers)>10):
        logger.debug("dictionnary length : {0}".format(len(dictUsers)))
        logger.info("Writing output file for day {0}".format(day))
        with open('./output/{0}_userbase.csv'.format(day), 'w', newline="") as csvfile:
            wr = csv.writer(csvfile, delimiter=',', quotechar='\"',
                            quoting=csv.QUOTE_MINIMAL)
            for u in dictUsers:
             wr.writerow(dictUsers[u].createRow())
    dictUsers = {}

def estimateRemainingTime():
     if cmpt_file>1:
        currenttime = time.time()
        timespent = currenttime - starttime
        remainingtime = timespent/(cmpt_file-1)*len(listInputFiles)
        logger.info("Time spent : {:.2f} seconds ".format(timespent))
        logger.info("Estimated remaining time : {:.2f} seconds"\
                    .format(remainingtime))
        logger.info("Estimated end : {0}".format(\
                     dt.datetime.fromtimestamp(starttime+remainingtime)))

for f in listInputFiles:

    cmpt_file+=1
    logger.info("Reading file  : {0} ({1}/{2})".format(f, cmpt_file, nb_files))
    estimateRemainingTime()
    try:
        inputfile = open(f, 'r', encoding='latin-1')
        reader = csv.reader(inputfile, delimiter=' ', quotechar='"')
        compt_bad_rows=0
        for row in reader:
#            i+=1
#            if i==10:
#                break # use only the first 30 rows to test your code
            if (len(row)>18):
                tmplog = Log(row)
                if tmplog.timestamp.date()!=dt.datetime.fromtimestamp(0.).date():
                    # When encounter a new day, start a new csv file
                    if prevday!=str(tmplog.timestamp.date()):
                        prevday = str(tmplog.timestamp.date())
                        logger.debug("Current previous day : {0} ".format(prevday))
                        writeuserbase(prevday)
                    if tmplog.username in dictUsers:
                        dictUsers[tmplog.username].addlog(tmplog)
                    else:
                        dictUsers[tmplog.username] = User(tmplog)
            else:
                compt_bad_rows+=1
        logger.warn(\
            "This file contains {0} rows that could not have been parsed".\
            format(compt_bad_rows))
        inputfile.close()
    except IOError as e:
        logger.error("Has encountred I/O error " + e.message)
    except:
        logger.error("Has encountred an unexpected error")

writeuserbase(prevday)



logger.info("===========================================")
logger.info("End file processing")
logger.info("===========================================")
handler.close()
