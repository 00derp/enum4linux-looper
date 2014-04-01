#!/usr/bin/python
# Enum4linux Looper
# Created by T$A
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import argparse
from netaddr import *
import subprocess

def get_ips(iparg):
   ips = []
   try:
      if os.path.isfile(iparg):
         f = open(iparg,'r')
         for line in f:
            line = line.rstrip()
            if '/' in line:
               for ip in IPNetwork(line).iter_hosts():
                  ips.append(str(ip))
            else:
               ips.append(line)
         f.close()
         return ips
      if '/' in iparg:
         for ip in IPNetwork(iparg).iter_hosts():
            ips.append(str(ip))
      else:
         ips.append(str(IPAddress(iparg)))
   except:
      print ("Error reading file or IP Address notation: %s" % iparg)
      exit()
   return ips

start_time = time.time()

# parse the arguments
parser = argparse.ArgumentParser(description='This tool is used to automate the testing of many IP''s with enum4linux')
parser.add_argument('-ip','--ipaddress', help='IP Address, IP/CIDR, IP Address File',required=True)
parser.add_argument('-a','--args', help='Parameters that will be passed to the underlying enum4linux command (pass the args in without a "-")',default='U',required=False)
args = parser.parse_args()

# get the list of ips
ips = get_ips(args.ipaddress)

print ("Enum4linux loop is starting...")

for ip in ips:
   #do the enum4linux looping
   subprocess.call(["enum4linux", ("-" + args.args), ip])

print ("Enum4linux loop is done...\nCompleted in: %s" % (time.time() - start_time))
