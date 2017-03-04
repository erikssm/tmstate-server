#!/usr/bin/env python
import socket
import sys
import datetime

def main():
    if not len(sys.argv) == 2:
        print "usage: ./client DEST_IP"
        sys.exit(1)

    sock = None
    try:
        sock = socket.create_connection((sys.argv[1], 22000))
        # Send data
        message = 'msg'
        #message = 'setstate'
        sock.sendall(message)

        data = sock.recv(4096)	    
        if "0" == data:
            print 'state is not set '
        else:
            print 'state is SET'

        now = datetime.datetime.now()
        if now.hour >= 8 and now.hour <= 10:
            print 'proceed..'
        else:
            print 'skip'

    except Exception as ex:
        print str( ex )
    finally:
        if sock:
            sock.close()

if __name__ == "__main__":
    main()
