import urllib2
import os
import json
import time
import datetime

def fetch():
        """
        This method will return controller profile parameters
        """
        log_diff=("/home/Capstone/THRDEL/profiling.log","a")
	shakti={}	
	try:
		url = 'curl -s http://52.11.203.22:5000/parameters'
		result = os.popen(url).read()
		parsedResult = json.loads(result)
		print parsedResult

		for controller in parsedResult:
    			print controller,parsedResult[controller]
    			shakti[str(controller)]=str(parsedResult[controller])
	       	        shakti["timestamp"]=str(str(time.strftime("%x"))+" "+str(time.strftime("%X")))
        		json_data_diff = json.dumps(shakti)
        		log_diff.write(json_data_diff+"\n")
	except Exception:
               pass   

def control(): 
    """
    This method is an infinite poller for fetching controller profiles
    """
    while True:
    	fetch()
	time.sleep(15)


if __name__=="__main__":
   control()
