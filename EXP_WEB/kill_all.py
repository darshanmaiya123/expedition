import os

def main():
    os.popen('kill $(ps aux | grep \'python /home/Capstone/\' | awk \'{print $2}\')')

if __name__ == '__main__':
    main()
