"""
Title:Performance Monitoring Tool for POX SDN Controller
Author: Team Expedition
Date of Creation: 18 April 2015
Date of Modification: 21 April 2015
Last Modified by: Ashwin Joshi
"""
import os
import subprocess
import json
import datetime
import time
import httplib2
from ConfigParser import SafeConfigParser
import logging

def pox_switchStats(pox_url):
    """
    This method calls the POX RestAPI for getting configured switches in topology
    """
    command = pox_url
    try:
    	result = os.popen(command).read()
    	parsedResult = json.loads(result)

    	for switch in parsedResult:
        	print switch[u'dpid']
        	pox_portStats(switch[u'dpid'])
    except Exception:
        pass
            


def pox_portStats(switch):
    """
    This method calls RestAPI for all ports of a given switch   
    """
    shakti={} 
    parser = SafeConfigParser()
    parser.read("/home/Capstone/KPI_config.conf")
    pox_url = parser.get('pox', 'pox_switch_port_info')

    command = "curl -s " + pox_url+str(switch)+"/ports"
    try:
       result = os.popen(command).read()
       parsedResult = json.loads(result)
       #print parsedResult
       for port in parsedResult:
         if int(port["number"]) < 65530:
            if str(port["number"]) in temp_store:
                txtp = (int(port['txBytes'])-int(temp_store[str(port["number"])]['TXbytes']))/15
                if txtp < 0:
                    txtp=0
                rxtp = (int(port['rxBytes'])- int(temp_store[str(port["number"])]['RXbytes']))/ 15
                if rxtp < 0:
                    rxtp=0

                shakti[str(port["number"])]={"txtp":txtp,"rxtp":rxtp}
                temp_store[str(port["number"])]['TXbytes']=port['txBytes']
                temp_store[str(port["number"])]['time-difference']= 5
                temp_store[str(port["number"])]['RXbytes']=port['rxBytes']
        
                himu.update({str(switch[-1]):shakti})
                himu["timestamp"]=str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))
                checkFault("POX",int(rxtp),int(txtp),int(port['rxError']),int(port['txError']),switch,str(port["number"]))
    except Exception:
                pass

def checkFault(controller,rxtp,txtp,rxE,txE,switch,port):
    """  
    This method serves as a Fault Logger depending upon the performance threshold violation
    """
    logging.basicConfig(filename="/home/Capstone/FAULT_LOG/fault.log",level=logging.DEBUG)


    parser = SafeConfigParser()
    parser.read("/home/Capstone/KPI_config.conf")
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


def pox_control():
    """  
    This method controls the logic flow in your program
    """
    count = 0
    parser = SafeConfigParser()
    parser.read("/home/Capstone/KPI_config.conf")
    pox_url = parser.get('pox', 'pox_switch_info')
    while True:
        global himu
        himu={}
        pox_switchStats(pox_url)
        log_diff=open("/home/Capstone/POX/portstats.log","a")
        json_data_diff = json.dumps(himu)
        log_diff.write(json_data_diff+"\n")
        #print himu
        time.sleep(15)
        count+=1


if __name__=="__main__":
    global temp_store
    temp_store={'1':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'2':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'3':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'4':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'5':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'}}
    pox_control()
