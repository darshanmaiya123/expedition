"""
Title:Performance Monitoring Tool for OpenDaylight SDN Controller
Author: Team Expedition
Date of Creation: 18 April 2015
Date of Modification: 21 April 2015
Last Modified by: Ashwin Joshi
"""

import os
import sys
import subprocess
import json
import datetime
import time
import httplib2
import logging
from ConfigParser import SafeConfigParser

def od_switchStats(username,password,odl_switch_info):
    """
    This method calls the OpenDayLight RestAPI for getting configured switches in topology 
    """
    log_diff=open("/home/Capstone/ODL/portstats.log","a")
    h = httplib2.Http(".cache")
    h.add_credentials(username,password)
    try:
    	resp, content = h.request(odl_switch_info,"GET")
    	json_data = json.loads(content)

    	for switch in json_data["nodes"]["node"]:
        	od_portStats(switch['node-connector'],switch['id'])

    	json_data_diff = json.dumps(himu)
    	log_diff.write(json_data_diff+"\n")
    	print himu
    	print "-----------------------"
    except Exception:
       print " Down"

def od_portStats(switch,switch_id):
    """
    This method calls RestAPI for all ports of a given switch
    """
    print switch_id
    shakti={}
    for port in switch:
        data={}
        if "eth" in str(port["flow-node-inventory:name"]):
            #print "port",str(port["flow-node-inventory:name"])[-1]
            print str(port["flow-node-inventory:name"])[-1]
            if str(port["flow-node-inventory:name"])[-1] in temp_store:

               txtp = (int(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'transmitted'])-int(temp_store[str(port["flow-node-inventory:name"])[-1]]['TXbytes']))/15
               if txtp < 0:
                  txtp=0
               rxtp = (int(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'received'])- int(temp_store[str(port["flow-node-inventory:name"])[-1]]['RXbytes']))/ 15
               if rxtp < 0:
                  rxtp=0
               shakti[str(port["flow-node-inventory:name"])[-1]]={"txtp":txtp,"rxtp":rxtp}
               temp_store[str(port["flow-node-inventory:name"])[-1]]['TXbytes']=port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'transmitted']
               temp_store[str(port["flow-node-inventory:name"])[-1]]['time-difference']= 15
               temp_store[str(port["flow-node-inventory:name"])[-1]]['RXbytes']=port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'received']

    himu.update({switch_id[-1]:shakti})
    himu["timestamp"]=str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))
    #print "Tx Bytes",port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'received']
    #print "Rx Bytes",port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes'][u'transmitted']
    #print "Tx Errors",port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-errors']
    #print "Rx Errors",port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-errors']
    checkFault("OPENDAYLIGHT",int(rxtp),int(txtp),int(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-errors']),int(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-errors']),switch_id,str(port["flow-node-inventory:name"]))

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

        
   
def odl_control():
    """
    This method controls the logic flow in your program
    """
    count = 0
    parser = SafeConfigParser()
    parser.read('/home/Capstone/KPI_config.conf')
    username = parser.get('opendaylight', 'username')
    password = parser.get('opendaylight', 'password')
    odl_switch_info = parser.get('opendaylight', 'odl_switch_info')
    while True:
        global himu
        himu={}
        od_switchStats(username,password,odl_switch_info)
        time.sleep(15)
        count+=1

temp_store={'1':{'time-difference': '15', 'TXbytes': '0', 'RXbytes': '0'},'2':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'3':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'4':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'5':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'}}

if __name__=="__main__":
    odl_control()




