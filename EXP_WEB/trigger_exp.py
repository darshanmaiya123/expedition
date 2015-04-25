import os

def startODL():
    os.system("python /home/Capstone/ODL/ODL_KPI.py > /dev/null 2>&1 &")


def startPOX():
    os.system("python /home/Capstone/POX/POX_KPI.py > /dev/null 2>&1 &")


def startRYU():
    os.system("python /home/Capstone/RYU/RYU_KPI.py > /dev/null 2>&1 &")


def startFDL():
    os.system("python /home/Capstone/FDL/FDL_KPI.py > /dev/null 2>&1 &")


def healthchecker():
    os.system("python /home/Capstone/HEARTBEAT/healthchecker.py > /dev/null 2>&1 &")


def fetch():
    os.system("python /home/Capstone/THRDEL/fetch.py > /dev/null 2>&1 &")

def main():
    startODL()	
    startPOX()
    startRYU()
    startFDL()
    healthchecker()
    fetch()

if __name__ == '__main__':
    main()

    


