from pathlib import Path
import sys
import os
import time
import socket
import ipaddress

# ----------------------------------------------------------------------------------------------------
def writeListToFile(dictHostNames, listFile):
    retries = 10
    while(retries > 0):
        try:
            dFile = open(listFile, 'w')
            for ipaddress in dictHostNames:
                dFile.write(str(ipaddress) + '\t' + dictHostNames[ipaddress] + '\n')
            dFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (writeListToFile): ' + str(sys.exc_info()[1]))
            time.sleep(3)
        retries = retries - 1

# ----------------------------------------------------------------------------------------------------
# main
def main():
        print("started HostNameScanner.py running")
    # arg1 = start ip
    # arg2 = end ip
    # arg3 = logfile
    # if len(sys.argv) > 3:
    #     # check arguments
    #     try:
    #         startIp = ipaddress.ip_address(sys.argv[1])
    #         endIp = ipaddress.ip_address(sys.argv[2])
    #     except:
    #         print('    EXCEPTION ERROR (main - arguments): ', sys.exc_info()[1])
    #         exit()
    #     logFile = sys.argv[3]
        startIp = "192.168.1.1"
        endIp = "192.168.1.255"
        logFile = os.path.join(Path(__file__).resolve().parent, "HostNameList.txt")
        if not os.path.isfile(logFile):
            print('    ERROR: [' + logFile + '] is not a valid file...')
            exit()
        if endIp < startIp:
            print('    ERROR: end IP is less than start IP')
            exit()
        # initialize hostname list
        dictHostNames = {}
        try:
            hLines = open(logFile, 'r')
            for hLine in hLines:
                if hLine.strip() != '':
                    try:
                        dictHostNames[hLine.split('\t')[0].strip()] = hLine.split('\t')[1].strip()
                    except:
                        pass
            hLines.close()
        except:
            pass
        # start scan
        print('INFO: Starting hostname scan...')
        while(True):
            currentIP = startIp
            while endIp > currentIP:
                hostName = ''
                try:
                    hostName = socket.gethostbyaddr(str(currentIP))[0].split('.')[0].upper()
                except:
                    hostName = ''
                if hostName != '':
                    print(str(currentIP) + ': ' + hostName.strip())
                    dictHostNames[currentIP] = hostName.strip()
                    writeListToFile(dictHostNames, logFile)
                else:
                    print(str(currentIP) + ':')
                currentIP = currentIP + 1
            writeListToFile(dictHostNames, logFile)
            time.sleep(10)
    # else:
    #     print('    ERROR: not enough arguments...')

# ----------------------------------------------------------------------------------------------------




