#!/usr/bin/python

import struct,time,sys,socket

if (len(sys.argv) < 2) or (sys.argv[1] == '--help'):
    print """
  ...........................:: TIME-DRIFT ::.............................

    Synopsis:
        Time-drift.py shows the difference between time on local machine
        and time provided by NTP server.

    usage:
        time-drift.py ntp-server

  .............................................:: Asazello, 16.02.15 ::...
    """
    exit(1)

NTPserv = sys.argv[1]

# Time server and its port
time_server = (NTPserv, 123)

# Epoch in Unix format
epoch = 2208988800L

try:
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

    # Prepare data for server
    data = '\x1b' + 47 * '\0'

    # Send data to the server
    client.sendto(data, time_server)

    # Recieve data back from the server
    data, address = client.recvfrom( 1024 )

    if data:
        # Process the data
        time_now = struct.unpack( '!12I', data )[10]

        # An exception if the time is 0
        if time_now == 0:
            # Invalid response
            print '0'
        # Calculate current time
        print ((time_now - epoch) - time.time())

    else:
        print '0'

except:
    print '0'
