#!/usr/bin/python
# Socket client example in python
# from: http://www.binarytides.com/python-socket-programming-tutorial/
 
import socket   # for sockets
import sys  # for exit
 
# Create an INET, STREAMing (TCP) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
host = 'www.google.com';
port = 80;
 
try:
    remote_ip = socket.gethostbyname( host )
    # No exception if we pass in an IP address
 
except socket.gaierror:
    # Could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
# Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
# Send some data (HTTP request) to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    # Send the whole string
    s.sendall(message)
except socket.error:
    # Send failed
    print 'Send failed'
    sys.exit()
 
print '******************* SENDING MESSAGE FOLLOWS **************************'
print message
print 'sent successfully'
 
# Now receive 4096 bytes of data from the byte stream, ignore the rest
reply = s.recv(4096)

print '***************************** REPLY FOLLOWS *********************************'
print reply
print '***************************** END REPLY *********************************'

# Closes the socket, tcp can close the connection
s.close()

print 'Socket Closed to ' + host + ' on ip ' + remote_ip
