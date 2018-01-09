#! /usr/bin/env python

import netsnmp
import sys
from optparse import OptionParser
import socket
import time
import logging
from pprint import pprint


STATUS = {'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3}
CHECKNAME = 'PAN_DISK'


def process_args():
    parser = OptionParser()
    # Required Options
    parser.add_option('-d', '--hostname', dest='hostname',
                      help='The hostname you want to check')
    parser.add_option('-c', '--community', dest='community', help='snmp community')
    (options, args) = parser.parse_args()

    # Detect required fields
    if not options.hostname or not options.community:
        parser.error('Must specify an hostname to check and an snmp community')
    return options

def check_pan_disk(hostname, community):
    pan_disk_oid = '.1.3.6.1.2.1.25.2.3.1'
    oid = netsnmp.Varbind(pan_disk_oid)
    #logger.debug('oid %s',oid)
    output = netsnmp.snmpwalk(oid, Version=2, DestHost=hostname, Community=community)
    #logger.debug('output %s',output)
   # return output 

#def calc_pan_disk():
    [index, oid, descr, allocUt, AvailS, UsedS] = [output[i:i+11] for i in range(0,len(output),11)]
    disk_info= descr[0:5]+AvailS[0:5]+UsedS[0:5]
    [Disktype, AvailSize, UsedSize] =[disk_info[i:i+5] for i in range(0,len(disk_info),5)]

#List for all types of Disk on the pans
    ram = Disktype[0],AvailSize[0],UsedSize[0]
    sd = Disktype[1],AvailSize[1],UsedSize[1]
    cfg_dk = Disktype[2],AvailSize[2],UsedSize[2]
    lg_dk = Disktype[3],AvailSize[3],UsedSize[3]
    rt_dk = Disktype[4],AvailSize[4],UsedSize[4]
    
    #print ram
    #print sd
    #print cfg_dk
    #print lg_dk
    #print rt_dk

#Zipping all lists together
    disks= zip(ram, sd, cfg_dk, lg_dk, rt_dk)
   #print disks

#flatten the list
    dk_flat  = [val for sublist in disks for val in sublist]
    #print dk_flat

#Slicing lists to create key value pairs for dictionary
    disk_keys = dk_flat[0:5]
    disk_av_values = dk_flat[5:10]
    disk_used_values = dk_flat[10:15]
    #print disk_keys
    #print disk_av_values
    #print disk_used_values

#Creating a dictionary 
    d = dict(zip(disk_keys,zip(disk_av_values,disk_used_values)))
    pprint (d)

# percentange calculation
    for key in d:
    #d2 = {key: (v1,v2,((int(v2)/int(v1))*100)) for key,(v1,v2) in d.items()}
    #print d2
        perc_usage = float( float(d[key][1])/float(d[key][0]))*100
        # print key, usage
        if perc_usage > 30.0:
         alert_level = 'CRITICAL'
         print "Disk name" + " " + key + " " + "is using more than 30%"
        elif perc_usage > 10.0:
         alert_level = 'WARNING'
         print "Disk name" + " " + key + " " + "is using more than 10%"
        else:
         alert_level = 'OK' 


def main():
    options = process_args()
    check_pan_disk(options.hostname, options.community)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    main()
