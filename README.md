asazello/sys-tools
==================
This repository is an eclectic collection of different Linux system administrator tools.

pinger.py
---------
Pinger.py is fast, multi-threaded ping and reverse dns lookup tool written in Python.

Required depencency:

    cidrize  -  Cidrize parses IPv4/IPv6 addresses, CIDRs, ranges, and wildcard matches 
                & attempts return a valid list of IP addresses
    netaddr  -  Pythonic manipulation of IPv4, IPv6, CIDR, EUI and MAC network addresses.

Usage:

    pinger.py [-d <DNS-IP>]  [-r]  -i <IP>

    options:
        -i  --ip   ip=      IP address/range
        -d  --dns  dns=     Specify a DNS server
        -r  --resolve       Resolve DNS name

    <IP> is very flexible and can be one of any of the following formats:

        192.0.2.18                192.0.2.18/32
        192.0.20.64/26            192.0.2.*
        192.0.2.80-192.0.2.85     192.0.2.170-175
        192.0.2.8[0-5]            192.0.2.[5678]

time-drift.py
-------------
Time-drift.py shows the difference between time on local machine and time provided by NTP server.

Usage:

    time-drift.py ntp-server

