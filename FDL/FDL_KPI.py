"""
Title:Performance Monitoring Tool for FloodLight SDN Controller
Author: Team Expedition
Date of Creation: 18 April 2015
Date of Modification: 21 April 2015
Last Modified by: Ashwin Joshi
"""

import os
import sys
import subprocess
import json
import io
import datetime
import time
import logging
from ConfigParser import SafeConfigParser

def fl_switchStats(fl_url,fl_url_1,fl_url_2):
    """
    This method calls the FloodLight  RestAPI for getting configured switches in topology
    """
    try:
    	result = os.popen(fl_url).read()
    	parsedResult = json.loads(result)
    	for record in parsedResult:
       		command = fl_url_1+record[u'switchDPID']+fl_url_2
        	result = os.popen(command).read()
        	parsedResult = json.loads(result)
        	fl_portStats(parsedResult,record[u'switchDPID'])
    except Exception:
	pass

def fl_portStats(parsedResult,switch):
    """
    This method calls RestAPI for all ports of a given switch
    """
    data={}
    shakti={}
    log_diff=open("/home/Capstone/FDL/portstats.log","a")
    for port in parsedResult[u'port']:
        if port[u'portNumber'] != 'local':
            if str(port[u'portNumber']) in temp_store:
               txtp = (int(port[u'transmitBytes'])-int(temp_store[str(port[u'portNumber'])]['TXbytes']))/15
	       if txtp < 0:
		  txtp=0
               rxtp = (int(port[u'receiveBytes'])- int(temp_store[str(port[u'portNumber'])]['RXbytes']))/ 15
               if rxtp < 0:
                  rxtp=0
	       shakti[str(port[u'portNumber'])]={"txtp":txtp,"rxtp":rxtp}
               temp_store[str(port[u'portNumber'])]['TXbytes']=port[u'transmitBytes']
               temp_store[str(port[u'portNumber'])]['time-difference']= 5
               temp_store[str(port[u'portNumber'])]['RXbytes']=port[u'receiveBytes']

               himu.update({switch[-1]:shakti})
               himu["timestamp"]=str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))
               checkFault("FLOODLIGHT",int(rxtp),int(txtp),int(port[u'receiveErrors']),int(port[u'transmitErrors']),switch,str(port[u'portNumber']))

def checkFault(controller,rxtp,txtp,rxE,txE,switch,port):
    """
    This method serves as a Fault Logger depending upon the performance threshold violation
    """
    logging.basicConfig(filename="/home/Capstone/FAULT_LOG/fault.log",level=logging.DEBUG)


    parser = SafeConfigParser()
    parser.read('/home/Capstone/KPI_config.conf')
    fm_rxtp = int(parser.get('pox_fm', 'fm_rxtp'))
    fm_txtp = int(parser.get('pox_fm', 'fm_txtp'))
    fm_rxE = int(parser.get('pox_fm', 'fm_rxE'))
    fm_txE = int(parser.get('pox_fm', 'fm_rxE'))

    result=[]
    if int(fm_rxtp) < rxtp:
       print "rxtp exceeded"
       #logging.basicConfig(format='%(levelname)s %(asctime)s : ---%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
       logging.warning(controller+":"+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+":["+switch+"]-"+port+"-rxtp exceeded")

    if int(fm_txtp) < txtp:
       print "txtp exceeded"
       #logging.basicConfig(format='%(levelname)s  %(asctime)s : ---%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
       logging.warning(controller+":"+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+":["+switch+"]-"+port+"-txtp exceeded")

    if int(fm_rxE) < rxE:
       print "rxE exceeded"
       #logging.basicConfig(format='%(levelname)s : %(asctime)s : ---%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
       logging.warning(controller+":"+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+":["+switch+"]-"+port+"-rxE exceeded")

    if int(fm_txE) < txE:
       print "txE exceeded"
       #logging.basicConfig(format='%(levelname)s : %(asctime)s : ---%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
       logging.warning(controller+":"+str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))+":["+switch+"]-"+port+"-txE exceeded")



def fl_control():
    """
    This method controls the logic flow in your program  
    """
    count = 0
    parser = SafeConfigParser()
    parser.read('/home/Capstone/KPI_config.conf')
    fl_url = parser.get('floodlight', 'fl_switch_info')
    fl_url_1 = parser.get('floodlight', 'fl_switch_port_info_1')
    fl_url_2 = parser.get('floodlight', 'fl_switch_port_info_2')
    while True:
        global himu
        himu={}
        fl_switchStats(fl_url,fl_url_1,fl_url_2)
        log_diff=open("/home/Capstone/FDL/portstats.log","a")
        json_data_diff = json.dumps(himu)
        log_diff.write(json_data_diff+"\n")
        print himu
        time.sleep(15)
        count+=1


if __name__=="__main__":
    global temp_store
    global himu
    temp_store={'local':{},'1':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'2':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'3':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'4':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'}}
    fl_control()



