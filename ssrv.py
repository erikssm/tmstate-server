#!/usr/bin/env python

# requirements:
#   apt install python-daemon

import socket
import sys
import signal
import time
import thread
from daemon import runner

timestamp = 0

def log(s):
    print s
    return
    #f = open('/tmp/bm-log.txt', 'a')
    #f.write( "%s\n" % str( s ) )
    #f.close();

def signal_handler(signal, frame):
    log('exiting..')
    sys.exit(0)

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/ssrv.pid'
        self.pidfile_timeout = 5
    def client_handler(self, clientsocket, client_addr):
        try:
             global timestamp
             data = clientsocket.recv(4096)
             if data:
                log( "received '%s' from %s" % ( data.strip(), str(client_addr) ) )

             if "setstate" in data:
                timestamp = time.time()
                log( "timestamp=%s" % str(timestamp) )
             elif "clearstate" in data:
                timestamp = 0
                log( "timestamp=%s" % str(timestamp) )

             if (( time.time() - timestamp ) < 60*10 ):
                sent = clientsocket.send( "1" )
             else:
                sent = clientsocket.send( "0" )

             clientsocket.close()

        except Exception as ex:
            log( "client socket error: %s" % str( ex ) )
        finally:
            if clientsocket:
                clientsocket.close()

    def run(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                server_address = ('localhost', 22000)
                log( 'starting tcp server on %s port %s' % server_address )
                sock.bind(server_address)
                sock.listen(30)
                log( 'server started, listening..' )

                while True:
                    try:
                        clientsocket = None
                        (clientsocket, client_addr) = sock.accept()
                        thread.start_new_thread( self.client_handler, (clientsocket, client_addr) )
                    except Exception as ex:
                        log( "error: %s" % str( ex ) )

            except Exception as ex:
                timeout = 5
                log( "error: %s \nrestarting in %d sec.." % ( str( ex ), timeout ) )
                time.sleep( timeout )

            finally:
                sock.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    app = App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()
