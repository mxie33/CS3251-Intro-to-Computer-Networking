# from https://pymotw.com/2/socket/udp.html

import socket
import sys

# Create a UDP/IP socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    print 'Socket created'
except socket.err, msg:
    print 'Could not create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind the socket to the port
server_address = ('', 10000)
try:
    sock.bind(server_address)
    print 'Bind complete: started on %s port %s' % server_address
except socket.err, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

while True:
    print 'waiting to receive message'
    data, address = sock.recvfrom(4096)
    
    print 'received %s bytes from %s' % (len(data), address)
    print data

    reply = 'OK: ' + data 

    if data:
        sent = sock.sendto(reply, address)
        print 'sent %s bytes back to %s' % (sent, address)
