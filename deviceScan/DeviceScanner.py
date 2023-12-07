import sys
import os
import time
import socket
import ipaddress
from pathlib import Path

DEBUGGING_IP = ipaddress.ip_address('192.168.0.158')

# ----------------------------------------------------------------------------------------------------
def readListFromFile(dictDevices, listFile, timeout, dictCountdown):
    print('INFO: Reading device list from list file...')
    retries = 10
    while(retries > 0):
        try:
            dFile = open(listFile, 'r')
            for line in dFile:
                lineParts = line.split('\t')
                if len(lineParts) >= 2:
                    dIDN = lineParts[0].strip()
                    if dIDN.startswith('ROHDE&SCHWARZ'):
                        dictDevices[dIDN] = lineParts[1].strip()
                        dictCountdown[dIDN] = timeout
                        print('    INFO: Found [' + dIDN + '] from list file...')
            dFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (readListFromFile): ', sys.exc_info()[1])
        retries = retries - 1
        time.sleep(3)

# ----------------------------------------------------------------------------------------------------
def writeListToFile(dictDevices, listFile):
    retries = 10
    while(retries > 0):
        try:
            dFile = open(listFile, 'w')
            for device in dictDevices:
                dFile.write(device + '\t' + dictDevices[device] + '\n')
            dFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (writeListToFile): ', sys.exc_info()[1])
        retries = retries - 1
        time.sleep(3)

# ----------------------------------------------------------------------------------------------------
def pollDevice(ip, port, command, timeout=0.2):
    returnData = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall((command + '\n').encode("ascii"))
        returnData = s.recv(1024).decode("ascii")
        s.settimeout(0)
    except Exception as e:
        if ip == DEBUGGING_IP:
            print(f"PollDevice Exception for: {ip} - {port} ")
            print(e)
        pass
    s.close()
    return returnData

# ----------------------------------------------------------------------------------------------------
def addDevice(dictDevices, dReply, ipAddress, timeout, dictCountdown, getHostName):
    try:
        replyParts = dReply.upper().strip().split(',')

        # DEBUGGING
        if ipaddress == DEBUGGING_IP:
            print(f"DEBUGGING: {ipAddress} replyparts on next line")
            print(replyParts)

        if len(replyParts) >= 4:
            if replyParts[0].startswith('ROHDE&SCHWARZ'):
                hostName = 'NO_HOSTNAME_' + ipAddress
                if getHostName:
                    try:
                        hostName = socket.gethostbyaddr(ipAddress)[0].split('.')[0]
                    except:
                        hostName = 'NO_HOSTNAME_' + ipAddress
                        print('    EXCEPTION ERROR (addDevice - hostName): ', sys.exc_info()[1])
                dIDN = (replyParts[0] + ',' + replyParts[1] + ',' + replyParts[2] + ',' + str(hostName)).upper()
                dictDevices[dIDN] = ipAddress
                dictCountdown[dIDN] = timeout
                print('    INFO: Device found: ' + dIDN)
    except:
        print('    EXCEPTION ERROR (addDevice): ', sys.exc_info()[1])

# ----------------------------------------------------------------------------------------------------
def cleanDeviceList(dictDevices, dictCountdown):
    print('INFO: Cleanup list...')
    try:
        deleteList = []
        for device in dictCountdown:
            dictCountdown[device] = dictCountdown[device] - 1
            if dictCountdown[device] < 0:
                deleteList.append(device)
        for device in deleteList:
            if device in dictDevices:
                del dictDevices[device]
                print('    INFO: Device [' + device + '] removed from list...')
            del dictCountdown[device]
    except:
        print('    EXCEPTION ERROR (cleanDeviceList): ', sys.exc_info()[1])

# ----------------------------------------------------------------------------------------------------

def read_config():
    file_name = 'ip_ranges.txt'
    ip_ranges = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                start, end = line.strip().split('-')
                ip_ranges.append((ipaddress.ip_address(start), ipaddress.ip_address(end)))
    except FileNotFoundError:
        print(f"    ERROR: {file_name} not found in {os.getcwd()}")
        exit()
    except Exception as e:
        print("    EXCEPTION ERROR (read_config):", str(e))
        print("    Expected format: startIP-endIP, e.g. 192.168.61.1-192.168.61.255")
        exit()
    return ip_ranges

# ----------------------------------------------------------------------------------------------------
# main
def main():
        print("started DeviceScanner.py running")
    # arg1 = logfile
    # arg2 = get hostname 
    # if len(sys.argv) > 2:
    #     logFile = sys.argv[1]
        logFile = os.path.join(Path(__file__).resolve().parent, "DeviceList.txt")
        if not os.path.isfile(logFile):
            print(f'    ERROR: [{logFile}] is not a valid file...')
            exit()

        getHostName = False
        # if sys.argv[2] == 'CHECK_HOSTNAME ':
        #     getHostName = True

        # initialize device list
        dictDevices = {}
        dictCountdown = {}

        # initialize address list
        ipAddressList = [ ipaddress.ip_address('172.17.75.1') , ipaddress.ip_address('172.25.57.5') , ipaddress.ip_address('192.168.61.229') ]

        ip_ranges = read_config()
        for startIp, endIp in ip_ranges:
            while startIp <= endIp:
                ipAddressList.append(startIp)
                startIp += 1

        # DEBUGGING
        
        if DEBUGGING_IP in ipAddressList:
            print('DEBUGGING: 192.168.0.158 is in the list')

        # start scan
        print('INFO: Starting device scan...')
        while True:
            for currentIP in ipAddressList:
                for port in [5555, 5025]:
                    pollReply = pollDevice(str(currentIP), port, '*IDN?')

                    # DEBUGGING
                    if currentIP == DEBUGGING_IP:
                        print(f"DEBUGGING: {currentIP} - {pollReply}")
                                                        

                    if pollReply != '':
                        print(f"{currentIP}: {pollReply.strip()}")
                        addDevice(dictDevices, pollReply, str(currentIP), 10, dictCountdown, getHostName)
                        writeListToFile(dictDevices, logFile)
                    else:
                        print(f"{currentIP}:")
            cleanDeviceList(dictDevices, dictCountdown)
            writeListToFile(dictDevices, logFile)
            time.sleep(0.1)
    # else:
    #     print('    ERROR: not enough arguments...')

    # # DEBUGGING
    # input("Press Enter to continue...")

# ----------------------------------------------------------------------------------------------------




