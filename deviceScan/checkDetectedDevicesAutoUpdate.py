import sys
import os
import datetime
import socket
import time
import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="AgileReserve",
    user="postgres",
    password="123"
)

cursor = conn.cursor()
# ----------------------------------------------------------------------------------------------------
def pollDevice(ip, port, command, timeout=3):
    returnData = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall((command + '\n').encode("ascii"))
        returnData = s.recv(1024).decode("ascii").strip()
        s.settimeout(0)
    except:
        pass
    s.close()
    return returnData

# ----------------------------------------------------------------------------------------------------
def getDetectedList(dictDetectedDevices, dictIpAddresses, timeout, listFile):
    print('INFO: Reading list of detected devices...')
    retries = 10
    while(retries > 0):
        try:
            dFile = open(listFile, 'r')
            for line in dFile:
                lineParts = line.split('\t')
                if len(lineParts) >= 2:
                    dIDN = lineParts[0].strip()
                    ipAddress = lineParts[1].strip()
                    if dIDN.startswith('ROHDE&SCHWARZ'):
                        dictDetectedDevices[dIDN] = timeout
                        dictIpAddresses[dIDN] = ipAddress
                        print('    INFO: Found [' + dIDN + '] with IP address ' + ipAddress + ' from detected device list file...')
            dFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (getDetectedList): ', sys.exc_info()[1])
            time.sleep(3)
        retries = retries - 1

#-------------------------------------------------------------------------------
def getUserName(ip, knownUsers, hostNames):
    hostName = ip
    try:
        hostName = getHostName(ip, hostNames)
        for kUser in knownUsers:
            if kUser.split('\t')[1].strip() == hostName:
                hostName = kUser.split('\t')[0].strip()
    except:
        hostName = ip
    return hostName

#-------------------------------------------------------------------------------
def getHostName(ip, hostNames):
    hostName = ip
    try:
        for hostData in hostNames:
            if hostData.split('\t')[0].strip() == ip:
                hostName = hostData.split('\t')[1].strip()
    except:
        hostName = ip
    return hostName

#-------------------------------------------------------------------------------
def getKnownList(listFile):
    kList = []
    try:
        if os.path.isfile(listFile):
            kLines = open(listFile, 'r')
            for kLine in kLines:
                if kLine.strip() != '':
                    kList.append(kLine.strip())
            kLines.close()
    except:
        print('EXCEPTION ERROR (getKnownList): ', sys.exc_info()[1])
    return kList

# ----------------------------------------------------------------------------------------------------
def writeToHTML(htmlFile, hContents):
    retries = 10
    while(retries > 0):
        try:
            # read priority device data
            priorityDeviceData = []
            priorityDeviceDataFound = False
            hFile = open(htmlFile, 'r')
            for line in hFile:
                if line.strip() == '<h1>Priority Devices Poll Result (Office Network)</h1>':
                    priorityDeviceDataFound = True
                if line.strip() == '<h1>Detected Devices Poll Result (8ASO Device Network)</h1>':
                    priorityDeviceDataFound = False
                if priorityDeviceDataFound:
                    priorityDeviceData.append(line)
            hFile.close()
            # write data to file
            hFile = open(htmlFile, 'w')
            hFile.write(r'<META HTTP-EQUIV="refresh" CONTENT="5">' + '\n')
            hFile.write(r'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"><html><head><title>8ASO Devices Poll Result (Auto-Refresh)</title>' + '\n')
            hFile.write(r'<style type="text/css"> body { font-family: Tahoma, Verdana, Segoe, sans-serif; } h1, h2, h3, h4 { color: #009DEC; } </style>' + '\n')
            hFile.write(r'<style> table, th, td {border: 1px solid black;} </style>' + '\n')
            hFile.write(r'</head><body>' + '\n')
            hFile.write(r'<h1>Detected Devices Poll Result (8ASO Device Network)</h1>' + '\n')
            hFile.write(r'<table cellpadding="5"><tr><th>Device</th><th>FW Version</th><th>Serial No.</th><th>Device Host Name</th><th>IP Address</th><th>Identification</th><th>Lock Owner</th><th>Users</th><th>Options</th></tr>' + '\n')
            for text in hContents:
                hFile.write(text + '\n')
            for text in priorityDeviceData:
                hFile.write(text)
            hFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (writeToHTML): ', sys.exc_info()[1])
            time.sleep(3)
        retries = retries - 1

# ----------------------------------------------------------------------------------------------------
def updateAutotestEnvironmentOverride(enviFile, dictDeviceInfo):
    retries = 10
    while(retries > 0):
        try:
            # read envi file
            fileData = []
            eFile = open(enviFile, 'r')
            for line in eFile:
                fileData.append(line)
            eFile.close()
            # parse data
            newFileData = []
            currentDevice = ''
            for line in fileData:
                newLine = line
                if r'&device' in line:
                    currentDevice = line.rsplit('\t', 1)[1].strip()
                    if currentDevice == 'EMx50':
                        currentDevice = 'EM550'
                    if currentDevice == 'EM100':
                        currentDevice = 'EM100XT'
                if line.startswith('date\t'):
                    newLine = 'date\t' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
                if r'&keep(device_ip)' in line:
                    for device in dictDeviceInfo:
                        if currentDevice in device and dictDeviceInfo[device][0] != '(NO REPLY)':
                            newLine = 'assign\t&keep(device_ip)\t' + dictDeviceInfo[device][0] + '\n'
                if r'&keep(firmware)' in line:
                    for device in dictDeviceInfo:
                        if currentDevice in device and dictDeviceInfo[device][1] != '':
                            deviceFw = int(float(''.join([x for x in dictDeviceInfo[device][1] if x in '0123456789.']))*100)
                            newLine = 'assign\t&keep(firmware)\t' + str(deviceFw) + '\n'
                newFileData.append(newLine)
            # write data to file
            eFile = open(enviFile, 'w')
            for line in newFileData:
                eFile.write(line)
            eFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (updateAutotestEnvironmentOverride): ', sys.exc_info()[1])
            time.sleep(3)
        retries = retries - 1


# ----------------------------------------------------------------------------------------------------
# main
# arg1 = device file
# arg2 = users file
# arg3 = html file
# arg4 = hostname file
# arg5/up = autotest override files
if len(sys.argv) > 2:
    # check arguments
    deviceFile = sys.argv[1]
    usersFile = sys.argv[2]
    htmlFile = sys.argv[3]
    hostnameFile = sys.argv[4]
    if not os.path.isfile(deviceFile):
        print('    ERROR: [' + deviceFile + '] is not a valid file...')
        exit()
    if not os.path.isfile(usersFile):
        print('    ERROR: [' + usersFile + '] is not a valid file...')
        exit()
    if not os.path.isfile(htmlFile):
        print('    ERROR: [' + htmlFile + '] is not a valid file...')
        exit()
    if not os.path.isfile(hostnameFile):
        print('    ERROR: [' + hostnameFile + '] is not a valid file...')
        exit()
    overrideFileList = []
    if len(sys.argv) > 5:
        for overrideFile in sys.argv[5:]:
            if not os.path.isfile(overrideFile):
                print('    ERROR: [' + overrideFile + '] is not a valid file...')
            else:
                overrideFileList.append(overrideFile)
    # start scan
    elapsed_time = 0
    start_time = time.time()
    dictDetectedDevices = {}
    dictDeviceInfo = {}
    knownUsers = []
    hostNames = []
    refreshList = 0
    heartBeat = True
    while (True):
        print('\n\n')
        # initialize lists every interval
        hostNames = getKnownList(hostnameFile)
        dictDetectedDevices = {}
        dictIpAddresses = {}
        getDetectedList(dictDetectedDevices, dictIpAddresses, 3, deviceFile)
        deleteList = []
        for device in dictDeviceInfo:
            if device not in dictDetectedDevices:
                deleteList.append(device)
        for device in deleteList:
            if device in dictDeviceInfo:
                del dictDeviceInfo[device]
        if refreshList > 0:
            refreshList = refreshList - 1
        else:
            knownUsers = getKnownList(usersFile)
            refreshList = 100
        # scan priority devices
        deviceInfoChanged = False
        fileText = []
        activeDevicesRow = []
        inactiveDevicesRow = []
        for dIDN in dictDetectedDevices:
            ipAddress = dictIpAddresses[dIDN]
            print('Checking: ' + ipAddress)
            pollTimeout = 5
            if dictDetectedDevices[dIDN] > 0:
                dictDetectedDevices[dIDN] = dictDetectedDevices[dIDN] - 1
            else:
                pollTimeout = 1
            # get device details
            deviceHostName = 'NO_HOSTNAME_' + ipAddress
            try:
                deviceHostName = getHostName(ipAddress, hostNames)
                deviceHostName = deviceHostName.upper()
            except:
                deviceHostName = 'NO_HOSTNAME_' + ipAddress
            # poll device details
            idnReply = ''
            lockReply = ''
            usersReply = ''
            optionsReply = ''
            validPort = 0
            for port in [5555, 5025]:
                idnReply = pollDevice(ipAddress, port, '*IDN?', pollTimeout)
                idnReply = idnReply.strip()
                if idnReply != '':
                    validPort = port
                    break
            if idnReply != '':
                deviceName = ''
                try:
                    deviceName = idnReply.split(',')[1].strip()
                except:
                    deviceName = ''
                deviceID = ''
                try:
                    deviceID = idnReply.split(',')[2].strip()
                except:
                    deviceID = ''
                if deviceName != '':
                    if deviceName not in ['PR100', 'DDF007', 'EM100', 'EM100XT', 'DDF1555']:
                        lockReply = pollDevice(ipAddress, validPort, 'SYST:LOCK:OWN?', 1)
                        lockReply = lockReply.replace('"', '').strip()
                    if deviceName not in ['SMW200A', 'SYS-SD5', 'SMU200A']:
                        usersReply = pollDevice(ipAddress, validPort, 'TRAC:UDP?', pollTimeout)
                    optionsReply = pollDevice(ipAddress, validPort, '*OPT?', pollTimeout)
            else:
                deviceName = ''
                deviceID = ''
                lockReply = ''
                usersReply = ''
                optionsReply = ''
            # prepare row text based on polled data
            if idnReply == '':
                idnReply = '(NO REPLY)'
            else:
                dictDetectedDevices[dIDN] = 3
            if lockReply == '':
                lockReply = 'NONE'
            if lockReply != 'NONE':
                lockReply = getUserName(lockReply, knownUsers, hostNames)
            if usersReply != '':
                for count in range(1,21):
                    usersReply = usersReply.replace(str(count).zfill(3), 'XXXXX_USER_XXXXX')
                userList = usersReply.split('XXXXX_USER_XXXXX')
                usersReply = ''
                users = []
                for user in userList:
                    if not user.startswith('DEF'):
                        userHostName = getUserName(user.split(',')[0].strip().replace('"', ''), knownUsers, hostNames)
                        if len(userHostName) > 0 and not userHostName.startswith('DEF') and userHostName not in usersReply:
                            usersReply = usersReply + ' ' + userHostName + ' '
                # if usersReply.endswith('<br>'):
                #     usersReply = usersReply.rsplit('<br>', 1)[0]
            else:
                usersReply = '(NONE)'
            # table row
            rowString = "{"
            # device
            rowString = rowString + '"deviceName"' + ':' + '"' + deviceName + '"' + r','
            # fw version
            fwVersion = ''
            try:
                fwVersion = idnReply.split(',')[3].split('-')[0]
            except:
                fwVersion = ''
            rowString = rowString + '"fwVersion"' + ':' + '"' + fwVersion  + '"' + r','
            # id/serial number
            rowString = rowString + '"deviceID"' + ':' + '"' + deviceID + '"' + r','
            # host name
            if 'NO_HOSTNAME_' in deviceHostName:
                rowString = rowString +'"deviceHostName"' + ':' + '"' + deviceHostName + '"' + r','
            else:
                rowString = rowString + '"deviceHostName"'+ ':' + '"'  + deviceHostName + '"' + r','
            # current ip: if none, set to black; then set previous ip to bold
            rowString = rowString + '"ipAddress"' + ':' + '"' + ipAddress + '"' + r','
            # idn: if not matched to id/serial number, set to red
            rowString = rowString + '"idnReply"'+ ':' + '"'  + idnReply + '"' + r','
            # lock: if none, set to black
            if lockReply == 'NONE':
                rowString = rowString + '"lockReply"'+ ':' + '"' + lockReply + '"' + r','
            else:
                rowString = rowString + '"lockReply"' + ':' + '"'+ lockReply + '"' + r','
            # users
            rowString = rowString + '"usersReply"' + ':' + '"' + usersReply + '"' + r','
            # options
            rowString = rowString + '"optionsReply"'+ ':' + '"'  + optionsReply + '"' + '}'
            # end row
            # if locked: set all to red
            if lockReply != 'NONE':
                rowString = rowString.replace('0000FF', 'FF0000').replace('000000', 'FF0000')
            # if no idn: set all to gray
            if idnReply == '(NO REPLY)':
                rowString = rowString.replace('0000FF', '808080').replace('000000', '808080').replace('FF0000', '808080')
                inactiveDevicesRow.append(rowString)
            else:
                activeDevicesRow.append(rowString)
                # check any change in device info
                if dIDN in dictDeviceInfo:
                    deviceInfoIp = dictDeviceInfo[dIDN][0]
                    deviceInfoFw = dictDeviceInfo[dIDN][1]
                    if ipAddress != '(NO REPLY)' and ipAddress != deviceInfoIp:
                        deviceInfoIp = ipAddress
                        deviceInfoChanged = True
                        print(dIDN + ' IP Address Changed...')
                    if fwVersion != '' and fwVersion != deviceInfoFw:
                        deviceInfoFw = fwVersion
                        deviceInfoChanged = True
                        print(dIDN + ' Firmware Changed...')
                    dictDeviceInfo[dIDN] = [deviceInfoIp, deviceInfoFw]
                else:
                    dictDeviceInfo[dIDN] = [ipAddress, fwVersion]
                    deviceInfoChanged = True
            time.sleep(0.2)
        fileText = fileText + activeDevicesRow
        fileText = fileText + inactiveDevicesRow
        # end of table
        for test in fileText:
            print("fileText:", test)
            test = json.loads(test)
            ip_address = test["ipAddress"]

            cursor.execute('SELECT COUNT(*) FROM "AgileReserveSys_machinelist"')
            count = cursor.fetchone()
            number = count[0]


            cursor.execute('SELECT * FROM "AgileReserveSys_machinelist" WHERE serial_no=%s', (test["deviceID"],))

            existing_ip = cursor.fetchone()
            print(existing_ip)

            if existing_ip:
                query = 'UPDATE "AgileReserveSys_machinelist" SET device_name = %s, fw_version = %s, ip_address = %s, device_host_name = %s, identification = %s, options = %s, lock_reply = %s, users_reply = %s WHERE serial_no = %s'

                cursor.execute(query, (test["deviceName"], test["fwVersion"], test["ipAddress"], test["deviceHostName"], test["idnReply"], test["optionsReply"], test["lockReply"], test["usersReply"], test["deviceID"] ))
            else:
                query = 'INSERT INTO "AgileReserveSys_machinelist" (id, device_name, fw_version, serial_no, device_host_name, ip_address, identification, options, lock_reply, users_reply) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

                new_id = int(number) + 1

                cursor.execute(query, (new_id, test["deviceName"], test["fwVersion"], test["deviceID"], test["deviceHostName"], test["ipAddress"], test["idnReply"], test["optionsReply"], test["lockReply"], test["usersReply"]))
            conn.commit()

        
        # write to html
        # writeToHTML(htmlFile, fileText)
        # update autotest environment override file
        if deviceInfoChanged and len(overrideFileList) > 0:
            for enviFile in overrideFileList:
                updateAutotestEnvironmentOverride(enviFile, dictDeviceInfo)
                print(enviFile + ' Updated...')
        # update console timestamp
        #os.system('cls')
        print('Update Timestamp: ' + str(datetime.datetime.now()))
        time.sleep(0.2)

#-------------------------------------------------------------------------------







