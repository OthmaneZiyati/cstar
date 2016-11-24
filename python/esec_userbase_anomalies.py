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
#workspace="D:/Users/abernado/Documents/8. CODE/PYTHON/201602.ESEC.CYBERSECU/"
workspace="C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU"
os.chdir(workspace)
logger.info("Creating list of input files")
#listInputFiles= glob.glob(workspace+"/data/aclog*.s")

#workspace_logs = "D:/Users/lmellior/Desktop/Logs picviz/aclog*.s"
#listInputFiles = glob.glob(workspace_logs)

listInputFiles = glob.glob(workspace+"/data/logs/test200/aclog*.s")
cmpt_file = 0
prevday = 0
nb_files = len(listInputFiles)
logger.info("Creating dictionnary of users")
dictUsers = dict()


#targetUser = "ay05326@InternetGateway"
#targetUser = "a192649@InternetGateway"
#targetUser = "ay15046@InternetGateway"
#targetUser = "a031717@InternetGateway"
#targetUser = "az00705@InternetGateway"
#targetUser = "a856056@InternetGateway"
#targetUser = "ax09574@InternetGateway"
#targetUser = "z007367@InternetGateway"
#targetUser = "s001801@InternetGateway"
targetUser = "az01252@InternetGateway"




def writeAnoFile(filePath, logList):
    outfile = open(filePath, 'w')
    #logList = map("#".join ,logList)
    logList = map(str,logList)
    outfile.write("\n".join(logList))
    outfile.close()
        
        
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
loglist=[]
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
                if (tmplog.username == targetUser)&(str(tmplog.timestamp.date())=="2015-12-01"):
                    loglist.append(row)
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

#writeAnoFile("D:/Users/abernado/Documents/8. CODE/PYTHON/201602.ESEC.CYBERSECU/out.csv", loglist)       
writeAnoFile("C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU/out10.csv", loglist)       


logger.info("===========================================")
logger.info("End file processing")
logger.info("===========================================")            
handler.close()
        


#outfile = open("C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU/out2.csv", 'w')
#loglist = map(str,loglist)
#outfile.write("\n".join(loglist))
#outfile.close()

#values = ",".join(map(str, kkk))
#loglist = map(lamdba x : ";".join(x),logist)
#outfile.write("\n".join(''.join(lines) for lines in loglist))
#kkk = map(lambda x : ",".join(x),kkk)
#print('\n'.join(''.join(elems) for elems in data))

#outfile = open("C:/Users/lmellior/ESEC/201602.ESEC.CYBERSECU/out.csv", 'w')
#kkk = list(loglist)
#kkk = map(str,kkk)
#outfile.write("\n".join(kkk))





