#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import getopt
import pipes
from threading import Thread
try:
    from cidrize import cidrize
except ImportError:
    print "You are missing cidrize..."
    print "Install it: pip install cidrize"
    sys.exit(2)

try:
    from netaddr import IPNetwork
except ImportError:
    print "You are missing netaddr..."
    print "Install it: pip install netaddr"
    sys.exit(2)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class testip(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    def run(self):
        cmd = "ping -q -c2 -W1 %s" %(self.ip)
        pingcli = os.popen(cmd ,"r")
        while 1:
            line = pingcli.readline()
            if not line: break
            igot = re.findall(testip.lifeline,line)
            if igot:
                self.status = int(igot[0])

def resolve(host,my_dns):
    if my_dns:
        fh = os.popen('dig @' + pipes.quote(my_dns) + ' +short -x ' + pipes.quote(host))
    else:
        fh = os.popen('dig +short -x ' + pipes.quote(host))
    out = fh.read()
    out = out.replace(".\n"," ")
    rc  = fh.close()
    if rc:
        out = "NONE"
    return out

def usage():
    print """
  .............................:: PINGER ::...............................

    Synopsis:
        Pinger is fast, multi-threaded ping and reverse dns lookup tool.

    usage:
        pinger.py [-d <DNS-IP>]  [-r]  [-i]  [-f]  <IP> [<IP> ... <IP>]

    options:
        -i  --ip   ip=      IP address/range
        -d  --dns  dns=     Specify a DNS server
        -r  --resolve       Resolve DNS name
        -f  --free-only     Display only free (Down) IPs

    returned symbols:"""
    print "        " + bcolors.OKGREEN + "✔ " + bcolors.ENDC + "   - Host is ALIVE and resolves properly."
    print "        " + bcolors.OKBLUE + "✔ " + bcolors.ENDC + "   - Host is ALIVE but doesn't resolve."
    print "        " + bcolors.FAIL + "✘ " + bcolors.ENDC + "   - Host id DOWN but resolves."
    print """
    <IP> is very flexible and can be one of any of the following formats:

        192.0.2.18                192.0.2.18/32
        192.0.20.64/26            192.0.2.*
        192.0.2.80-192.0.2.85     192.0.2.170-175
        192.0.2.8[0-5]            192.0.2.[5678]

  .............................................:: Asazello, 02.07.15 ::...
    """

def main(argv):
    my_dns = ""
    resolvedns = False
    free_only = False
    my_cidr = ""
    scidr = []
    pinglist = []
    testip.lifeline = re.compile(r"(\d) received")
    report = ("Down","Partial Response","Alive")

    try:
        opts, args = getopt.getopt(argv, "hi:rfd:", ["help", "ip=", "resolve", "free-only", "dns="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-r", "--resolve"):
            resolvedns = True
        elif opt in ("-i", "--ip"):
            args.insert(0,arg)
        elif opt in ("-d", "--dns"):
            my_dns = arg
        elif opt in ("-f", "--free-only"):
            free_only = True

    for my_cidr in args:
        try:
            test_scidr = cidrize(my_cidr,strict=True)
        except:
            pass
        else:
            scidr.extend(test_scidr)

    if not scidr:
        usage()
        sys.exit()

    for cidrs in scidr:
        for ip in IPNetwork(cidrs):
            current = testip(str(ip))
            pinglist.append(current)
            current.start()

    for pings in pinglist:
        pings.join()
        if resolvedns:
            resolved = resolve(pings.ip,my_dns)
            if report[pings.status] == "Down":
                if resolved:
                    print bcolors.FAIL + "✘ " + bcolors.ENDC + " " + pings.ip + "  " + resolved + "- " + report[pings.status]
                else:
                    print "   " + pings.ip + "  " + resolved + "- " + report[pings.status]
            else:
                if resolved:
                    if not free_only:
                        print bcolors.OKGREEN + "✔ " + bcolors.ENDC + " " + pings.ip + "  " + resolved + "- " + report[pings.status]
                else:
                    if not free_only:
                        print bcolors.OKBLUE + "✔ " + bcolors.ENDC + " " + pings.ip + "  " + resolved + "- " + report[pings.status]
        else:
            if report[pings.status] == "Down":
                print "  " + pings.ip + " - " + report[pings.status]
            else:
                if not free_only:
                    print bcolors.OKGREEN + "✔ " + bcolors.ENDC + pings.ip + " - " + report[pings.status]

if __name__ == "__main__":
    if not sys.argv[1:]:
        usage()
        sys.exit()
    else:
        main(sys.argv[1:])
