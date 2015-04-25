
"""
Title:Performance Monitoring Tool for POX SDN Controller
Author: Team Expedition
Date of Creation: 18 April 2015
Date of Modification: 21 April 2015
Last Modified by: Ashwin Joshi
"""
import requests
import time
import datetime
import re
import httplib2
import json
from ConfigParser import SafeConfigParser

def heartbeat(url,ip,count):
    """
    This method connects to controllers and determinies its health 
    """
    controller=["POX","RYU","FLOODLIGHT","OPENDAYLICHT"]
    heartbeat=dict()
    log_diff = open("/home/Capstone/HEARTBEAT/availability.log","a")
    try:
        h = httplib2.Http(".cache")
        h.add_credentials('admin', 'admin')
        print url
        #resp, content = h.request('http://10.55.17.20:8080/controller/nb/v2/statistics/default/flowstats', "GET")
        resp, content = h.request(url, "GET")
        print resp.status
        if resp.status == 200:
            print "Controller @ "+ip+" Up @"+str(datetime.datetime.now().time())
            #heartbeat[controller[count]]={"timestamp":str(str(time.strftime("%x"))+" "+str(time.strftime("%X"))),"Availability":100}

            json_data_diff = controller[count]+","+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+","+str(100) 
            log_diff.write(json_data_diff+"\n")
               
        else:
            #heartbeat[controller[count]]={"timestamp":str(str(time.strftime("%x"))+" "+str(time.strftime("%X"))),"Availability":0}
            json_data_diff = controller[count]+","+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+","+str(0)
            log_diff.write(json_data_diff+"\n")
           
    except: 
            #heartbeat[controller[count]]={"timestamp":str(str(time.strftime("%x"))+" "+str(time.strftime("%X"))),"Availability":0}
            json_data_diff = controller[count]+","+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+","+str(0)
            log_diff.write(json_data_diff+"\n")
            print "Controller @ "+ip+" Down @"+str(datetime.datetime.now().time())

def startChecker():
    """
    This method initializes the heartbeatchecker
    """
    parser = SafeConfigParser()
    parser.read('/home/Capstone//KPI_config.conf')
   
    urls=[parser.get('healthcheck','pox'),parser.get('healthcheck','ryu'),parser.get('healthcheck','fdl'),parser.get('healthcheck','odl')]
    while True:
        count=0
        for url in urls:
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', url )
            heartbeat(url,ip[0],count)
            count+=1
        print "--------------------------------"
        time.sleep(5)


def checkHeartbeat():
    """
    This method is a trigger method for heartbeat. It also infinitely runs the checker
    """
    h = httplib2.Http(".cache")
    h.add_credentials('admin', 'admin')
    while True:
    	startChecker()

if __name__=="__main__":
    checkHeartbeat()

