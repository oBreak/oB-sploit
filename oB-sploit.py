#!/usr/bin/env python

# Import

import os
import configparser
import time
import requests
import sys
import subprocess
from os import listdir
from pathlib import Path
import socket
from threading import Thread
import subprocess
#from SocketServer import ThreadingMixIn   # What is this used for?

# Variables

debugSet        = True
debugLog        = []
home            = str(Path.home())
fileDir         = os.path.dirname(os.path.realpath('__file__'))
outfileWin      = os.path.join(fileDir, 'out\\out.txt')
outfileMac      = os.path.join(fileDir, 'out/out.txt')
outfile         = os.path.join(fileDir, 'out/out.txt')
debugfileWin    = os.path.join(fileDir, 'debug\\debug.txt')
debugfileMac    = os.path.join(fileDir, 'debug/debug.txt')
debugfile       = os.path.join(fileDir, 'debug/debug.txt')
scansrc         = os.path.join(fileDir, 'scansrc/')

mypath          = ''
mypathWin       = home + "\\Projects\\gh-oB-sploit\\in\\"
mypathMac       = home + "/Projects/gh-oB-sploit/in/"
targets         = []
fileCount       = int(0)
conf            = {}
lineBreaks      = str('\n')
scanresults     = []
class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print ("received data:", data)
            if data.decode('utf-8') == 'a':
                resp = "0.1"
                conn.send(resp.encode('utf-8'))
                print('Option a')
            if data.decode('utf-8') == 'b':
                resp = "0.2"
                conn.send(resp.encode('utf-8'))
                print('Option b')
            #print data.decode('utf-8')
                #resp = str('0.1')
                #conn.send(resp.encode('utf-8'))
            '''if not data: break
            print ("received data:", data)'''
            conn.send(data)  # echo


TCP_IP = '127.0.0.1'
TCP_PORT = 64
BUFFER_SIZE = 20  # Normally 1024, but we want fast response


# Functions

'''
Inbound function is meant to take in files of types txt, log, or csv. Handling for each file
is differentiated.

CSV files should only contain the data elements meant to be gathered. There should be no headers
or labels.

IP addresses and hostnames are accepted in the inbound files. Adding functionality to take custom ports.
'''

def boot():
    ''' Commented out because this would not work on Macs and it is just for making it look nice
    on the command line. Focusing on functionality for now and will come back to clean up the formatting
    at a later date.

    try:
        os.system('cls')
    except SyntaxError:
        pass
    '''
    print('Initializing program: oB-sploit.')
    print('Debug activated is: ' + str(debugSet) + '.')
    print('')
    pass

def openSocks():
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        tcpsock.listen(4)
        print ("Waiting for incoming connections...")
        (conn, (ip, port)) = tcpsock.accept()
        newthread = ClientThread(ip, port)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

def readConf():
    global conf
    conf = configparser.ConfigParser()
    conf.read('conf.ini')
    if debugSet == True:
        debugLog.append('Configuration sections loaded:')
        debugLog.append(conf.sections())
    return

def inbound():
    global fileCount, mypath
    iF = []   # iF is inbound files
    try:
        for f in listdir(mypathWin):
            if f.find(".txt", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".log", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".csv", len(f) - 4) != -1:
                iF.append(f)
            else:
                #print(f + ' outside of txt, log, or csv types.')
                fileCount = fileCount - 1
            fileCount = fileCount + 1
            print (range(fileCount))
        mypath = mypathWin
    except FileNotFoundError:
        for f in listdir(mypathMac):
            if f.find(".txt", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".log", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".csv", len(f) - 4) != -1:
                iF.append(f)
            else:
                #print(f + ' outside of txt, log, or csv types.')
                fileCount = fileCount - 1
            fileCount = fileCount + 1
        mypath = mypathMac
    if debugSet == True:
        debugLog.append('iF (inbound files) contains:')
        for x in iF:
            debugLog.append(x + ' added to iF')
        debugLog.append('fileCount is: ' + str(fileCount))
    return iF

def parse(x):
    file = open('in/' + x, 'r')
    for line in file:
        line = line.strip() # Removes blank lines.
        if line:
            targets.append(line)
            if debugSet == True:
                debugLog.append('Appending ' + line + ' to targets.')
    pass

def outbound():
    print('\n================\n==Begin output==\n================\n')
    n = 0
    global outfile
    if os.path.isfile(outfile):
        print(outfile + ' exists; appending timestamp to written file.')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        outfilefull = str(outfile)
        outfiletype = outfilefull[-4:]
        outfilename = outfilefull[:(len(outfilefull) - 4)]
        outfilefull = outfilename + '-' + timestr + outfiletype
        print(outfilefull)
        outfile = os.path.join(fileDir, outfilefull)

    try:
        f = open(outfile, 'a')
        print('')
        print('\tSetting output file,', outfile)
        print('')
    except:
        print("\tFailed to open output file!")
        f.close()
    for j in scanresults:
        f.write(j)
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' lines complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.')
    print('\n')
    return

def scan(t): # Runs each scan on target 't'.
    ''' If the scan is set to True, send to scan# and target (s,t) to scan select. '''
    for s in conf['scans']:
        if conf['scans'][s] == 'True':
            if debugSet == True:
                debugLog.append('Running ' + s + ' against ' + t + ' in scan(t)')
            pass
        if conf['scans'][s]== 'True':
            scanselect(s,t)
    return

def scanselect(s,t):
    ''' Select the scan with the switcher, send target to the scan. '''
    switcher = {
        'scan1': int(1),
        'scan2': int(2),
        'scan3': int(3)   #Add more scans here
    }
    y=(switcher[s])
    if y == 1:
        print('Launching scan1 on ' + t)
        scan1(t)
    elif y == 2:
        print('Launching scan2 on ' + t)
        scan2(t)
    elif y == 3:
        print('Launching scan3 on ' + t)
        scan3(t)
    else:
        print ('Invalid scan selected.')
    return


def scan1(x): # WebLogic Remote Code Execution (RCE) - Under development
    y = 'Begin scan1 on ' + x
    scan1target = ['nmap', '-T4', '-F', x]
    '''
    Scan 1 target is set up to do a "quick scan" from nmap on target x. In order to do a more intense scan,
    the options would be nmap -T4 -A -v <ipaddress>.
    '''

    # open listening port/socket or some sort of notification that confirmation is received.
    # does this need to be multi-threaded?
    # perform exploit

    # PLACEHOLDER BELOW RUNS NMAP SCAN, NOT AN EXPLOIT
    #result = subprocess.run(scan1target, stdout=subprocess.PIPE)
    #scanresults.append(result.stdout.decode('utf-8'))



    return y

def scan2(x): # Does nothing
    #print(x)
    y = 'Begin scan2 on ' + x
    scanresults.append('These are the results of the scan.')
    return y

def scan3(x):  # This is doing an ARIN lookup.
    '''
    url1 = 'http://whois.arin.net/rest/ip/'
    url2 = '.txt'
    y = url1 + x + url2
    payload = {'key': 'val'}
    headers = {}
    res = requests.get(y, data=payload, headers=headers)
    txt = res.text
    scanresults.append(txt)
    '''
    y = 'Nothing done with' + x
    scanresults.append(y)
    return y

def debug(): # Gathers file paths and initial values
    if debugSet == True:
        debugLog.append('\n\n=============================\n=======DEBUG==OUTPUT=========\n=============================')
        debugLog.append('debugSet\t = ' + str(debugSet))
        debugLog.append('home\t\t = ' + str(home))
        debugLog.append('fileDir\t\t = ' + str(fileDir))
        debugLog.append('outfile\t\t = ' + str(outfile))
        debugLog.append('mypath\t\t = ' + str(mypath))
        debugLog.append('targets\t\t = ')
    return

def debug2(): # Prints data to debug file after program has run
    global debugfile
    if debugSet == True:
        print('\n================')
        print('==Debug output==')
        print('================')
        n = 0
        if os.path.isfile(debugfile):
            print(debugfile + ' exists; appending timestamp to written file.')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            debugfilefull = str(debugfile)
            debugfiletype = debugfilefull[-4:]
            debugfilename = debugfilefull[:(len(debugfilefull) - 4)]
            debugfilefull = debugfilename + '-' + timestr + debugfiletype
            print(debugfilefull + ' created.')
            debugfile = os.path.join(fileDir, debugfilefull)

        try:
            f = open(debugfile, 'a')
            print('')
            print('\tSetting debug file,', debugfile)
            print('')
        except:
            print("\tFailed to open debug file!")
            f.close()
        for j in debugLog:
            f.write(str(j))
            f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
            n = n + 1
            if n % 100 == 0:
                print('\tWriting outputs: ' + str(n) + ' lines complete.')
            else:
                pass
        else:
            pass
        print('\tOutput complete: ' + str(n) + ' lines written.')
        print('\n')
        return

def arin(x):
	url1		=	'http://whois.arin.net/rest/ip/'
	url2		=	'.txt'
	y		 	=	url1+x+url2
	payload 	=	{'key':'val'}
	headers		=	{}
	res 		= 	requests.get(y, data=payload, headers=headers)
	txt 		=	res.text
	return txt

def main():
    readConf()
    boot()
    i = inbound()
    for file in range(fileCount):
        parse(i[file])
    for t in targets:
        scan(t)
    pass

# Run

debug()
main()
outbound()
debug2()

