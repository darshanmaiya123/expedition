"""
Title:Performance Monitoring Tool for RYU SDN Controller
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
import logging
from ConfigParser import SafeConfigParser

def ryu_switchStats(ryu_url):
    """
    This method calls the RYU RestAPI for getting configured switches in topology
    """
    #print ryu_url
    try:
    	result = os.popen(ryu_url).read()
   	parsedResult = json.loads(result)

    	for switch in parsedResult:
        	ryu_portStats(switch)
    except Exception:
        pass

def ryu_portStats(switch):
    """
    This method calls RestAPI for all ports of a given switch
    """
    shakti={}
    parser = SafeConfigParser()
    parser.read('/home/Capstone/KPI_config.conf')
    command= parser.get('ryu', 'ryu_switch_port_info')
    try:
      result = os.popen(command+str(switch)).read()
      parsedResult = json.loads(result)
 
      for port in parsedResult[unicode(str(switch))]:
         if int(port["port_no"]) < 65530:
            if str(port["port_no"]) in temp_store:
                txtp = (int(port['tx_bytes'])-int(temp_store[str(port["port_no"])]['TXbytes']))/15
                if txtp < 0:
                    txtp=0
                rxtp = (int(port['rx_bytes'])- int(temp_store[str(port["port_no"])]['RXbytes']))/ 15
                if rxtp < 0:
                    rxtp=0

                shakti[str(port["port_no"])]={"txtp":txtp,"rxtp":rxtp}
                temp_store[str(port["port_no"])]['TXbytes']=port['tx_bytes']
                temp_store[str(port["port_no"])]['time-difference']= 5
                temp_store[str(port["port_no"])]['RXbytes']=port['rx_bytes']

                himu.update({str(switch):shakti})
                himu["timestamp"]=str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))
                checkFault("RYU",int(rxtp),int(txtp),int(port['rx_errors']),int(port['tx_errors']),str(switch),str(port["port_no"]))

    except Exception:
            pass

def checkFault(controller,rxtp,txtp,rxE,txE,switch,port):
    """
    This method serves as a Fault Logger depending upon the performance threshold violation
    """
    LOG_FILENAME = 'example.log'
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


def ryu_control():
    """
    This method controls the logic flow in your program
    """
    count = 0
    parser = SafeConfigParser()
    parser.read('/home/Capstone/KPI_config.conf')
    ryu_url = parser.get('ryu', 'ryu_switch_info')
    while True:
        global himu
        himu={}
        ryu_switchStats(ryu_url)
        log_diff=open("/home/Capstone/RYU/portstats.log","a")
        json_data_diff = json.dumps(himu)
        print json_data_diff
        print "---------------------------"
        log_diff.write(json_data_diff+"\n")
        time.sleep(15)
        count+=1


if __name__=="__main__":
    global temp_store
    temp_store={'1':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'2':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'3':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'},'4':{'time-difference': '0', 'TXbytes': '0', 'RXbytes': '0'}}
    ryu_control()
