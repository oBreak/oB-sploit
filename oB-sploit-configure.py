#!/usr/bin/env python

'''
Writes a configuration file for the oB-sploit program. This controls which
exploits are run.

Scan1   = Example
Scan2   = NOT ADDED YET --- WebLogic RCE (Remote Code Execution) - from https://github.com/frohoff/ysoserial
    This requires input of 'ip:port command' as arguments.
Scan3   = ARIN.net lookup for the IP in question.



'''

# Import
import configparser

# Variables


# Functions
def writeConf():
    conf = configparser.ConfigParser()
    conf['credentials-example']         = {'user1': 'example', 'pass1': 'password', 'user2': 'admin', 'pass2': 'root'}
    conf['connectionstring-example']    = {'servername': 'server', 'port': '23'}
    conf['scans']                       = {'scan1': 'False',\
                                           'scan2': 'False',\
                                           'scan3': 'True'}

    with open ('conf.ini', 'w') as configfile:
        conf.write(configfile)
    return

writeConf()