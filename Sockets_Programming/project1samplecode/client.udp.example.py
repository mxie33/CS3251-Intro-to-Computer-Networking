# from https://pymotw.com/2/socket/udp.html

import socket
import sys
import getopt

# Create a UDP/IP socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.err, msg:
    print 'Could not create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

server = 'localhost';
port = 10000;
message = 'Status Normal'

try:
   opts, args = getopt.getopt(sys.argv[1:],"hs:p:m:",["server=","port=","message="])
except getopt.GetoptError:
   print 'using default server [' + server + '] port [' + port + '] and message [' + message + ']'
for opt, arg in opts:
   if opt == '-h':
      print 'usage: '
      print sys.argv[0] + ' -s <server> -p <port> -m <message>'
      sys.exit()
   elif opt in ("-s", "--server"):
      server = arg
   elif opt in ("-p", "--port"):
      port = int(arg)
   elif opt in ("-m", "--message"):
      message = arg

try:
    remote_ip = socket.gethostbyname( server )
    # handles IP address as input without error
except socket.gaierror:
    #could not resolve
    print 'Hostname ' + server + ' could not be resolved. Exiting'
    sys.exit()

server_address = (server, port)

try:

    # Send data
    print 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    print 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print 'received "%s"' % data

finally:
    print 'closing socket'
    sock.close()
