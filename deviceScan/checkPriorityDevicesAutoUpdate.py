import sys
import os
import datetime
import socket
import time

# ----------------------------------------------------------------------------------------------------
def pollDevice(ip, port, command, timeout=3):
    returnData = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall((command + '\n').encode("ascii"))
        returnData = s.recv(1024).decode("ascii")
        s.settimeout(0)
    except:
        pass
    s.close()
    return returnData

# ----------------------------------------------------------------------------------------------------
def getPriorityList(dictPriorityDevices, timeout, listFile):
    print('INFO: Reading list of priority devices...')
    retries = 10
    while(retries > 0):
        try:
            dFile = open(listFile, 'r')
            for line in dFile:
                dIDN = line.strip()
                if dIDN.startswith('ROHDE&SCHWARZ'):
                    dictPriorityDevices[dIDN] = timeout
                    print('    INFO: Found [' + dIDN + '] from priority device list file...')
            dFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (getPriorityList): ', sys.exc_info()[1])
        retries = retries - 1
        time.sleep(3)

#-------------------------------------------------------------------------------
def getUserName(ip, knownUsers):
    linkName = '<a href=" " title="' + ip + '">' + ip + '</a>'
    try:
        hostName = socket.gethostbyaddr(ip)[0].split('.')[0].upper()
        linkName = '<a href=" " title="' + ip + '">' + hostName + '</a>'
        for kUser in knownUsers:
            if hostName in kUser.upper():
                userName = kUser.split('\t')[0]
                linkName = '<a href=" " title="' + hostName + ':' + ip + '">' + userName + '</a>'
    except:
        pass
    return linkName

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
            # read detected device data
            detectedDeviceData = []
            detectedDeviceDataFound = False
            hFile = open(htmlFile, 'r')
            for line in hFile:
                if line.strip() == '<h1>Detected Devices Poll Result (8ASO Device Network)</h1>':
                    detectedDeviceDataFound = True
                if line.strip() == '<h1>Priority Devices Poll Result (Office Network)</h1>':
                    detectedDeviceDataFound = False
                if detectedDeviceDataFound:
                    detectedDeviceData.append(line)
            hFile.close()
            # write data to file
            hFile = open(htmlFile, 'w')
            hFile.write(r'<META HTTP-EQUIV="refresh" CONTENT="5">' + '\n')
            hFile.write(r'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"><html><head><title>8ASO Devices Poll Result (Auto-Refresh)</title>' + '\n')
            hFile.write(r'<style type="text/css"> body { font-family: Tahoma, Verdana, Segoe, sans-serif; } h1, h2, h3, h4 { color: #009DEC; } </style>' + '\n')
            hFile.write(r'<style> table, th, td {border: 1px solid black;} </style>' + '\n')
            hFile.write(r'</head><body>' + '\n')
            for text in detectedDeviceData:
                hFile.write(text)
            hFile.write(r'<h1>Priority Devices Poll Result (Office Network)</h1>' + '\n')
            hFile.write(r'<table cellpadding="5"><tr><th>Device</th><th>FW Version</th><th>Serial No.</th><th>Device Host Name</th><th>IP Address</th><th>Identification</th><th>Lock Owner</th><th>Users</th><th>Options</th></tr>' + '\n')
            for text in hContents:
                hFile.write(text + '\n')
            hFile.close()
            retries = 0
        except:
            print('    EXCEPTION ERROR (writeToHTML): ', sys.exc_info()[1])
        retries = retries - 1
        time.sleep(3)

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
        retries = retries - 1
        time.sleep(3)

# ----------------------------------------------------------------------------------------------------
# main
# arg1 = priority file
# arg2 = users file
# arg3 = html file
# arg4 = envi file

#if len(sys.argv) > 4:
#    # check arguments
#    priorityFile = sys.argv[1]
#    usersFile = sys.argv[2]
#    htmlFile = sys.argv[3]
#    enviFile = sys.argv[4]
#    if not os.path.isfile(priorityFile):
#        print('    ERROR: [' + priorityFile + '] is not a valid file...')
#        exit()
#    if not os.path.isfile(usersFile):
#        print('    ERROR: [' + usersFile + '] is not a valid file...')
#        exit()
#    if not os.path.isfile(htmlFile):
#        print('    ERROR: [' + htmlFile + '] is not a valid file...')
#        exit()
#    if not os.path.isfile(enviFile):
#        print('    ERROR: [' + enviFile + '] is not a valid file...')
#        exit()
#    # start scan
#    elapsed_time = 0
#    start_time = time.time()
#    dictPriorityDevices = {}
#    dictDeviceInfo = {}
#    knownUsers = []
#    refreshList = 0
#    heartBeat = True
#    while (True):
#        # initialize lists every interval
#        if refreshList > 0:
#            refreshList = refreshList - 1
#        else:
#            dictPriorityDevices = {}
#            getPriorityList(dictPriorityDevices, 3, priorityFile)
#            knownUsers = getKnownList(usersFile)
#            refreshList = 100
#            deleteList = []
#            for device in dictDeviceInfo:
#                if device not in dictPriorityDevices:
#                    deleteList.append(device)
#            for device in deleteList:
#                if device in dictDeviceInfo:
#                    del dictDeviceInfo[device]
#        # scan priority devices
#        deviceInfoChanged = False
#        fileText = []
#        activeDevicesRow = []
#        inactiveDevicesRow = []
#        for pDevice in dictPriorityDevices:
#            pDeviceParts = pDevice.split(',')
#            deviceName = pDeviceParts[1].strip()
#            deviceID = pDeviceParts[2].strip()
#            deviceHostName = pDeviceParts[3].strip()
#            pollTimeout = 5
#            if dictPriorityDevices[pDevice] > 0:
#                dictPriorityDevices[pDevice] = dictPriorityDevices[pDevice] - 1
#            else:
#                pollTimeout = 1
#            # get ip address
#            currentIP = '(NO REPLY)'
#            # check if device has no hostname
#            if deviceHostName.startswith('NO_HOSTNAME_'):
#                currentIP = deviceHostName.replace('NO_HOSTNAME_', '').strip()
#            else:
#                # try to get current ip via hostname
#                try:
#                    currentIP = socket.gethostbyname(deviceHostName)
#                except:
#                    os.system('ping ' + deviceHostName + ' -n 1 > temp.txt')
#                    try:
#                        currentIP = socket.gethostbyname(deviceHostName)
#                    except:
#                        currentIP = '(NO REPLY)'
#            # poll device details
#            idnReply = ''
#            lockReply = ''
#            usersReply = ''
#            optionsReply = ''
#            # if ip address is available
#            if currentIP != '(NO REPLY)':
#                validPort = 0
#                for port in [5555, 5025]:
#                    idnReply = pollDevice(currentIP, port, '*IDN?', pollTimeout)
#                    idnReply = idnReply.strip()
#                    if idnReply != '':
#                        validPort = port
#                        break
#                if idnReply != '':
#                    if deviceName not in ['PR100', 'DDF007', 'EM100', 'EM100XT', 'DDF1555']:
#                        lockReply = pollDevice(currentIP, validPort, 'SYST:LOCK:OWN?', 1)
#                        lockReply = lockReply.replace('"', '').strip()
#                    if deviceName not in ['SMW200A', 'SYS-SD5', 'SMU200A']:
#                        usersReply = pollDevice(currentIP, validPort, 'TRAC:UDP?', pollTimeout)
#                    optionsReply = pollDevice(currentIP, validPort, '*OPT?', pollTimeout)
#                else:
#                    lockReply = ''
#                    usersReply = ''
#                    optionsReply = ''
#            # prepare row text based on polled data
#            if idnReply == '':
#                idnReply = '(NO REPLY)'
#            else:
#                dictPriorityDevices[pDevice] = 3
#            if lockReply == '':
#                lockReply = 'NONE'
#            if lockReply != 'NONE':
#                lockReply = getUserName(lockReply, knownUsers)
#            if usersReply != '':
#                for count in range(1,21):
#                    usersReply = usersReply.replace(str(count).zfill(3), 'XXXXX_USER_XXXXX')
#                userList = usersReply.split('XXXXX_USER_XXXXX')
#                usersReply = ''
#                users = []
#                for user in userList:
#                    if not user.startswith('DEF'):
#                        userHostName = getUserName(user.split(',')[0].strip().replace('"', ''), knownUsers)
#                        if len(userHostName) > 0 and not userHostName.startswith('DEF') and userHostName not in usersReply:
#                            usersReply = usersReply + '<b>' + userHostName + '</b><br>'
#                if usersReply.endswith('<br>'):
#                    usersReply = usersReply.rsplit('<br>', 1)[0]
#            else:
#                usersReply = '(NONE)'
#            # table row
#            rowString = r'<tr>'
#            # device
#            rowString = rowString + r'<td><font color="#0000FF"><b>' + deviceName + r'</b></font></td>'
#            # fw version
#            fwVersion = ''
#            try:
#                fwVersion = idnReply.split(',')[3].split('-')[0]
#            except:
#                fwVersion = ''
#            rowString = rowString + r'<td><font color="#0000FF">' + fwVersion + r'</font></td>'
#            # id/serial number
#            rowString = rowString + r'<td><font color="#0000FF">' + deviceID + r'</font></td>'
#            # host name
#            if 'NO_HOSTNAME_' in deviceHostName:
#                rowString = rowString + r'<td><font color="#000000">' + deviceHostName + r'</font></td>'
#            else:
#                rowString = rowString + r'<td><font color="#0000FF">' + deviceHostName + r'</font></td>'
#            # current ip: if none, set to black; then set previous ip to bold
#            if currentIP == '(NO REPLY)':
#                rowString = rowString + r'<td><font color="#000000">' + currentIP + r'</font></td>'
#            else:
#                rowString = rowString + r'<td><font color="#0000FF"><b>' + currentIP + r'</b></font></td>'
#            # idn: if not matched to id/serial number, set to red
#            #if deviceID.split('/')[0] in idnReply or idnReply == '(NO REPLY)':
#            rowString = rowString + r'<td><font color="#0000FF">' + idnReply + r'</font></td>'
#            #else:
#            #    rowString = rowString + r'<td><font color="#FF0000">' + idnReply + r'(Mismatched Serial Number!!!)</font></td>'
#            # lock: if none, set to black
#            if lockReply == 'NONE':
#                rowString = rowString + r'<td><font color="#000000">(' + lockReply + r')</font></td>'
#            else:
#                rowString = rowString + r'<td><font color="#0000FF">(<b>' + lockReply + r'</b>)</font></td>'
#            # users
#            rowString = rowString + r'<td><font color="#000000">' + usersReply + r'</font></td>'
#            # options
#            rowString = rowString + r'<td><font color="#000000">' + optionsReply + r'</font></td>'
#            # end row
#            rowString = rowString + r'</tr>'
#            # if locked: set all to red
#            if lockReply != 'NONE':
#                rowString = rowString.replace('0000FF', 'FF0000').replace('000000', 'FF0000')
#            # if no idn: set all to gray
#            if idnReply == '(NO REPLY)':
#                rowString = rowString.replace('0000FF', '808080').replace('000000', '808080').replace('FF0000', '808080')
#                inactiveDevicesRow.append(rowString)
#            else:
#                activeDevicesRow.append(rowString)
#                # check any change in device info
#                if pDevice in dictDeviceInfo:
#                    deviceInfoIp = dictDeviceInfo[pDevice][0]
#                    deviceInfoFw = dictDeviceInfo[pDevice][1]
#                    if currentIP != '(NO REPLY)' and currentIP != deviceInfoIp:
#                        deviceInfoIp = currentIP
#                        deviceInfoChanged = True
#                        print(pDevice + ' IP Address Changed...')
#                    if fwVersion != '' and fwVersion != deviceInfoFw:
#                        deviceInfoFw = fwVersion
#                        deviceInfoChanged = True
#                        print(pDevice + ' Firmware Changed...')
#                    dictDeviceInfo[pDevice] = [deviceInfoIp, deviceInfoFw]
#                else:
#                    dictDeviceInfo[pDevice] = [currentIP, fwVersion]
#                    deviceInfoChanged = True
#            time.sleep(0.2)
#        fileText = fileText + activeDevicesRow
#        fileText = fileText + inactiveDevicesRow
#        # end of table
#        fileText.append(r'</table>')
#        if heartBeat:
#            fileText.append(r'<br/><i><font color="#0000FF">Update Timestamp: ' + str(datetime.datetime.now()) + r'</font></i>')
#        else:
#            fileText.append(r'<br/><i><font color="#008000">Update Timestamp: ' + str(datetime.datetime.now()) + r'</font></i>')
#        heartBeat = not heartBeat
#        elapsed_time = time.time() - start_time
#        start_time = time.time()
#        fileText.append(r'<br/><i>Update Interval: ' + str(elapsed_time) + r' seconds</i>')
#        fileText.append(r'<br/><i>List Refresh Counter: ' + str(refreshList) + r'</i>')
#        fileText.append(r'<br/><i>Script Version: checkPriorityDevicesAutoUpdate.py 20170417</i>')
#        # write to html
#        writeToHTML(htmlFile, fileText)
#        # update autotest environment override file
#        if deviceInfoChanged:
#            updateAutotestEnvironmentOverride(enviFile, dictDeviceInfo)
#            print(enviFile + ' Updated...')
#        # update console timestamp
#        print('Update Timestamp: ' + str(datetime.datetime.now()))
#        time.sleep(0.2)

#-------------------------------------------------------------------------------







