# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:23:57 2016

Utility classes and functions to execute esec_userbase_main script

@author: Antony Bernadou & Louis Melliorat
"""
import datetime as dt
#from urlparse import urlparse
from urllib.parse import urlparse


class Log:
    
    # 1st field = timestamp (Timestamp in UNIX epoch)
    timestamp = dt.datetime.fromtimestamp(0.);
    # 2nd field = duration (x-elapsed-time)
    elapsedtime = 0.
    # 3rd field = ip client (Client IP Address)
    ipclient = "0.0.0.0"
    # 4th field = response code (sc-result-code/sc-http-status)
    #statuscode = ''
    #responsecode = ''
    statusresponsecode = ''
    # 5th field : response size (Response size (header + body)) 
    responsesize = 0
    # 6th field : request (Request first line - request method, URI.)
    httpmethod = "CONNECT"
    uri = ""
    urlset = urlparse("")
    urlscheme = ''
    urlnetloc = ''
    urlpath = ''
    urlparams = ''
    urlquery = ''
    urlfragment = ''
    urlport = ''
    # 7th field : username (Authenticated user name)
    username = "UNKNOWN"
    # 8th field : (s-hierarchy/s-hostname)
    hierarchy = ''
    hostname = ''
    # 9th field : mimetype (cs-mime-type) : text/javascript
    mimetype = ''
    # 10th field : aclcode (ACL decision tag) : DEFAULT_CASE_12-INET-INET_identity-DefaultGroup-NONE-NONE-DefaultGroup 
    aclcode = ''    
    # 11th field : scanningverdict (Scanning verdict information) : <IW_adv,-1.2,0,"-",0,0,0,1,"-",-,-,-,"-",1,-,"-","-",-,-,IW_adv,-,"-","-","Unknown","Unknown","-","-",632.88,0,-,"Unknown","-",-,"-",-,-,"-","-"> 
    scanningverdict = ''
    # 12th field : %?BLOCK_SUSPECT_USER_AGENT,MONITOR_SUSPECT_USER_AGENT? (The Web Proxy blocked or monitored the transaction based on the Suspect User Agent setting for the Access Policy group) : - 
    accesspolicyverdict = ''    
    # 13th field : %<User-Agent:%!%-%. %XC (x-webcat-code-abbr) : IW_adv 
    webcatcode = ''    
    # 14th field : requestsize (Request size (headers + body)) : 833 
    requestsize = 0    
    # 15th field :  (X-Forwarded-For header) : "10.249.215.223" 
    xff = ''
    # 16th field : %u (cs(User-Agent)) : "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko" 
    useragent = ''
    # 17th field :  (x-error-code) :
    errorcode = "0"
    # 18th field :  (Data source IP address (server IP address)) 
    ipserver = "0.0.0.0"
           
    
    def __init__(self, row):
        # parse timestamp
        try:
            self.timestamp = dt.datetime.fromtimestamp(float(row[0]))
        except:
            pass
        try:
            self.elapsedtime = float(row[1])
        except ValueError:
            pass
        self.ipclient = row[2]
        try:
            self.statusresponsecode = row[3]
        except IndexError:
            pass
        except ValueError:
            pass
        try:
            self.responsesize = int(row[4])
        except ValueError:
            pass
        self.httpmethod = row[5]
        self.uri = row[6]
        try:
            self.urlset = urlparse(self.uri)
            self.urlscheme = self.urlset.scheme
            self.urlnetloc = self.urlset.netloc
            self.urlpath = self.urlset.path
            self.urlparams = self.urlset.params
            self.urlquery = self.urlset.query
            self.urlfragment = self.urlset.fragment
            self.urlport = self.urlset.port
        except:
            pass
        self.username = row[7] if row[7]!='-' else "UNKNOWN"
        try:
            self.hierarchy = row[8].split('/')[0]
            self.hostname = row[8].split('/')[1]
        except:
            pass
        self.mimetype = row[9]
        self.aclcode = row[10]
        self.scanningverdict = row[11]
        
        if len(row)==19:
            self.accesspolicyverdict = row[12]
            self.webcatcode = row[13]
            try:
                self.requestsize = int(row[14])
            except ValueError:
                pass
            self.xff = row[15]
            self.useragent = row[16]
            self.errorcode = row[17]
            self.ipserver = row[18]
        elif len(row) > 19:
            tmprow = list(row[12:])
            tmprow.reverse()            
            #self.accesspolicyverdict = row[12]
            self.webcatcode = tmprow[5]
            try:
                self.requestsize = int(tmprow[4])
            except ValueError:
                pass
            self.xff = tmprow[3]
            self.useragent = tmprow[2]
            self.errorcode = tmprow[1]
            self.ipserver = tmprow[0]
            
#    def toString(self):
#        return 
    
            

def isweekend(log):
    res = 0
    try:
        res = int(log.timestamp.weekday() in [5, 6])
    except:
        pass
    return(res)
        
def isoutsideofficehours(log):
    res = 0
    try:
        res = int(log.timestamp.hour not in range(7,20))
    except:
        pass
    return(res)
    
def iscatadv(log):
    res = 0
    try:
        res = int(log.webcatcode == "IW_adv")
    except:
        pass
    return(res)    
    
 
def iscatgamb(log): # Gambling
    res = 0
    try:
        res = int(log.webcatcode == "IW_gamb") 
    except:
        pass
    return(res)       
       
def iscathack(log): # Hacking
    res = 0
    try:
        res = int(log.webcatcode == "IW_hack")  
    except:
        pass
    return(res)    
    
def iscatilac(log): # Illegal Activities
    res = 0
    try:
        res = int(log.webcatcode == "IW_ilac")
    except:
        pass
    return(res)
    
    
def iscatsusp(log): # suspect/Threat URLs
    res = 0
    try:
        res = int(log.webcatcode == "Susp")  
    except:
        pass
    return(res)    

def iscatp2p(log): # Peer File Transfer
    res = 0
    try:
        res = int(log.webcatcode == "IW_p2p")   
    except:
        pass
    return(res)    
###     
def iscatmail(log): # Web-based Email
    res = 0
    try:
        res = int(log.webcatcode == "IW_mail")        
    except:
        pass
    return(res)

def iscatpark(log): # Parked Domains 
    res = 0
    try:
        res = int(log.webcatcode == "IW_park")
    except:
        pass
    return(res)
 
def iscatinfr(log): # Infrastructure
    res = 0
    try:
        res = int(log.webcatcode == "IW_infr")       
    except:
        pass
    return(res)       
       
def isPOST(log): 
    res = 0
    try:
        res = int(log.httpmethod == "POST")        
    except:
        pass
    return(res)
   
def isAppl(log):
    res = 0
    try:
        res = int("application" in log.mimetype)  
    except:
        pass
    return(res)

def isApploctetstream(log):
    res = 0
    try:
        res = int(log.mimetype == "application/octet-stream")       
    except:
        pass
    return(res)              
###       
    
def isbadport(log):
    res = 0
    try:   
        res = int(log.urlport not in [None, 80, 8080, 443, 34])
    except:
        pass
    return(res)
    
def isHTTPcode(log,code):
    res = 0
    try:
        code = str(code)
        res = int(code in log.statusresponsecode)
    except:
        pass
    return res

def isTCPdenied(log):
    res = 0
    try:
        res = int("TCP_DENIED" in log.statusresponsecode)
    except:
        pass
    return(res)
    
def isTCPmiss(log):
    res = 0
    try:
        res = int("TCP_MISS" in log.statusresponsecode)  
    except:
        pass
    return(res)
   
def duration(log):
    res = 0
    try:
        res = log.elapsedtime
    except:
        pass
    return(res)    
    
def getrequestsize(log):
    res = 0
    try:
        res = log.requestsize   
    except:
        pass
    return(res)
    
def getresponsesize(log):
    res = 0
    try:
        res = log.responsesize    
    except:
        pass
    return(res)
    
def iserrorcode(log):
    res = 0
    try:
        res = int(log.errorcode != '0' )
    except:
        pass
    return(res)    
    
def isaclcodeBlockadmin(log):
    res = 0
    try:
        res = int("BLOCK_ADMIN" in log.aclcode)
    except:
        pass
    return(res)    
##
def isTunnel(log):
    res = 0
    try:
        res = int(log.urlscheme == "tunnel")
    except:
        pass
    return(res)    
##
     
def isIPinURL(log):
    res = 0
    try:   
        res = int(log.ipclient in log.uri)
    except:
        pass
    return(res)     

"""
Put here all the necessary functions to compute user feature
Use as much information from log class as you can
Then add attribute to User class and dont forget to take care of this 
attributes in constructor (__init__) and in addlog and createRow methods

examples : 
    - is response code 200 ? 407 ? 404 ? 4xx ? fonction ok, regarder quels codes
                                                    seraient interessants
    - max duration ? ok
    - max request / response size ? ok
    - average duration  or request / response size ? ok
    - check for wierd web categories : ok
    - check if "block" appears in accesspolicyverdict field ok
    - check if the user made a weird download the mimetype : NO
    - check if there was an error code : ok
    - many others ...

"""
        
class User:    
    userID = "UNKNOWN"
    nb_logs = 0
    nb_weekend = 0
    nb_outsideofficehours = 0    
    nb_badport = 0
    
    nb_cat_adv = 0
    nb_cat_gamb = 0
    nb_cat_hack = 0
    nb_cat_ilac = 0
    nb_cat_susp = 0
    nb_cat_p2p = 0
    
    nb_cat_mail = 0
    nb_cat_park = 0
    nb_cat_infr = 0   
    nb_POST = 0
    nb_mime_appl = 0
    nb_mine_appl_octet_stream = 0
    nb_url_tunnel = 0
    
    nb_codeHTTP_200 = 0
    nb_codeHTTP_401 = 0
    nb_codeHTTP_403 = 0
    nb_codeHTTP_404 = 0
    nb_codeHTTP_407 = 0
    nb_codeHTTP_500 = 0
    nb_codeHTTP_501 = 0
    
    nb_tcp_denied = 0
    nb_tcp_miss = 0
    
    max_duration = 0
    max_request = 0
    max_responsesize = 0
    nb_error_code = 0
    total_duration = 0
    total_request = 0  
    total_responsesize = 0
    nb_block_admin = 0
    nb_ip_in_url = 0
    

    
    
    def __init__(self, log):
        self.userID = log.username
        self.nb_logs = 1
        self.nb_weekend = isweekend(log)
        self.nb_outsideofficehours = isoutsideofficehours(log)
        self.nb_badport = isbadport(log)
        self.nb_cat_adv = iscatadv(log)        
        self.nb_cat_gamb = iscatgamb(log)        
        self.nb_cat_hack = iscathack(log)
        self.nb_cat_ilac = iscatilac(log)
        self.nb_cat_susp = iscatsusp(log)
        self.nb_cat_p2p = iscatp2p(log)       
        self.nb_codeHTTP_200 = isHTTPcode(log,200)
        self.nb_codeHTTP_401 = isHTTPcode(log,401)
        self.nb_codeHTTP_403 = isHTTPcode(log,403)
        self.nb_codeHTTP_404 = isHTTPcode(log,404)
        self.nb_codeHTTP_407 = isHTTPcode(log,407)
        self.nb_codeHTTP_500 = isHTTPcode(log,500)
        self.nb_codeHTTP_501 = isHTTPcode(log,501)
        self.max_duration = duration(log)
        self.max_request = getrequestsize(log)
        self.max_responsesize = getresponsesize(log)
        self.nb_error_code = iserrorcode(log)
        self.total_duration = duration(log)
        self.total_responsesize = getresponsesize(log)
        self.total_request = getrequestsize(log)
        self.nb_tcp_denied = isTCPdenied(log) 
        self.nb_tcp_miss = isTCPmiss(log) 
        self.nb_block_admin = isaclcodeBlockadmin(log)
        self.nb_ip_in_url = isIPinURL(log)        
        self.nb_cat_mail = iscatmail(log) 
        self.nb_cat_park = iscatpark(log) 
        self.nb_cat_infr = iscatinfr(log)         
        self.nb_POST = isPOST(log)
        self.nb_mime_appl = isAppl(log)
        self.nb_mine_appl_octet_stream = isApploctetstream(log)
        self.nb_url_tunnel = isTunnel(log)
        
    def addlog(self, log):                       
        self.nb_logs += 1
        self.nb_weekend += isweekend(log)
        self.nb_outsideofficehours += isoutsideofficehours(log)
        self.nb_badport += isbadport(log)
        self.nb_cat_adv += iscatadv(log)        
        self.nb_cat_gamb += iscatgamb(log)       
        self.nb_cat_hack += iscathack(log)
        self.nb_cat_ilac += iscatilac(log)
        self.nb_cat_susp += iscatsusp(log)
        self.nb_cat_p2p += iscatp2p(log)        
        self.nb_codeHTTP_200 += isHTTPcode(log,200)
        self.nb_codeHTTP_401 += isHTTPcode(log,401)
        self.nb_codeHTTP_403 += isHTTPcode(log,403)
        self.nb_codeHTTP_404 += isHTTPcode(log,404)
        self.nb_codeHTTP_407 += isHTTPcode(log,407)
        self.nb_codeHTTP_500 += isHTTPcode(log,500)
        self.nb_codeHTTP_501 += isHTTPcode(log,501)
        self.max_duration = max(duration(log),self.max_duration)
        self.max_request = max(getrequestsize(log),self.max_request)
        self.max_responsesize = max(getresponsesize(log),self.max_responsesize)                
        self.nb_error_code += iserrorcode(log)
        self.total_duration += duration(log)
        self.total_request += getrequestsize(log)
        self.total_responsesize += getresponsesize(log)        
        self.nb_tcp_denied += isTCPdenied(log)  
        self.nb_tcp_miss += isTCPmiss(log) 
        self.nb_block_admin += isaclcodeBlockadmin(log)
        self.nb_ip_in_url += isIPinURL(log)        
        self.nb_cat_mail += iscatmail(log)
        self.nb_cat_park += iscatpark(log)
        self.nb_cat_infr += iscatinfr(log)       
        self.nb_POST += isPOST(log)
        self.nb_mime_appl += isAppl(log)
        self.nb_mine_appl_octet_stream += isApploctetstream(log)
        self.nb_url_tunnel += isTunnel(log) 
    
    def toString(self):
        res = self.userID+'\n'
        res += "Nb logs : {0}\n".format(self.nb_logs)
        res += "Nb weekend : {0}\n".format(self.nb_weekend)
        res += "Nb outside office hours : {0}\n".format(self.nb_outsideofficehours)
        res += "Nb bad port : {0}\n".format(self.nb_badport)
        res += "Nb webcat advertisement : {0}\n".format(self.nb_cat_adv)
        res += "Nb webcat gambing : {0}\n".format(self.nb_cat_gamb)        
        res += "Nb webcat hacking : {0}\n".format(self.nb_cat_hack)
        res += "Nb webcat illegal activities : {0}\n".format(self.nb_cat_ilac)
        res += "Nb webcat suspect/Threat URLs : {0}\n".format(self.nb_cat_susp)
        res += "Nb webcat Peer File Transfer : {0}\n".format(self.nb_cat_p2p)
        res += "Nb webcat mail : {0}\n".format(self.nb_cat_mail)
        res += "Nb webcat parked domains : {0}\n".format(self.nb_cat_park)
        res += "Nb webcat infrastructure : {0}\n".format(self.nb_cat_infr)
        res += "Nb http methode POST : {0}\n".format(self.nb_POST)
        res += "Nb mime type application : {0}\n".format(self.nb_mime_appl)
        res += "Nb mime type appl octet stream : {0}\n".format(self.nb_mine_appl_octet_stream)
        res += "Nb url tunnel: {0}\n".format(self.nb_url_tunnel)              
        res += "Nb code HTTP 200 : {0}\n".format(self.nb_codeHTTP_200)
        res += "Nb code HTTP 401 : {0}\n".format(self.nb_codeHTTP_401)
        res += "Nb code HTTP 403 : {0}\n".format(self.nb_codeHTTP_403)
        res += "Nb code HTTP 404 : {0}\n".format(self.nb_codeHTTP_404)
        res += "Nb code HTTP 407 : {0}\n".format(self.nb_codeHTTP_407)
        res += "Nb code HTTP 500 : {0}\n".format(self.nb_codeHTTP_500)
        res += "Nb code HTTP 501 : {0}\n".format(self.nb_codeHTTP_501)
        res += "Max duration : {0}\n".format(self.max_duration)
        res += "Max request : {0}\n".format(self.max_request)
        res += "Max response size : {0}\n".format(self.max_responsesize)
        res += "Nb error code : {0}\n".format(self.nb_error_code)
        res += "Total duration : {0}\n".format(self.total_duration)
        res += "Total request : {0}\n".format(self.total_request)
        res += "Total response size : {0}\n".format(self.total_responsesize)                
        res += "Nb BLOCK AMDIN : {0}\n".format(self.nb_block_admin)
        res += "Nb IP in URL : {0}\n".format(self.nb_ip_in_url)
        res += "Nb TCP_DENIED : {0}\n".format(self.nb_tcp_denied) 
        res += "Nb TCP_MISS : {0}\n".format(self.nb_tcp_miss)
        return(res)
        
    def createRow(self):
        res=[]
        res.append(self.userID)
        res.append(self.nb_logs)
        res.append(self.nb_weekend)
        res.append(self.nb_outsideofficehours)
        res.append(self.nb_badport)
        res.append(self.nb_cat_adv)        
        res.append(self.nb_cat_gamb)        
        res.append(self.nb_cat_hack)
        res.append(self.nb_cat_ilac)
        res.append(self.nb_cat_susp)
        res.append(self.nb_cat_p2p)        
        res.append(self.nb_cat_mail)
        res.append(self.nb_cat_park)
        res.append(self.nb_cat_infr)         
        res.append(self.nb_POST)
        res.append(self.nb_mime_appl)
        res.append(self.nb_mine_appl_octet_stream)
        res.append(self.nb_url_tunnel)                
        res.append(self.nb_codeHTTP_200)
        res.append(self.nb_codeHTTP_401)
        res.append(self.nb_codeHTTP_403)
        res.append(self.nb_codeHTTP_404)
        res.append(self.nb_codeHTTP_407)
        res.append(self.nb_codeHTTP_500)
        res.append(self.nb_codeHTTP_501)
        res.append(self.max_duration)
        res.append(self.max_request)
        res.append(self.max_responsesize)        
        res.append(self.nb_error_code)
        res.append(self.total_duration)
        res.append(self.total_request)
        res.append(self.total_responsesize)
        res.append(self.nb_block_admin)
        res.append(self.nb_ip_in_url)
        res.append(self.nb_tcp_denied)
        res.append(self.nb_tcp_miss)
        return(res)
    
    