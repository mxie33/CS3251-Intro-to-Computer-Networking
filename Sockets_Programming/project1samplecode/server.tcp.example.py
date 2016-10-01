# Socket client example in python
# from: http://www.binarytides.com/python-socket-programming-tutorial/

import socket   # for sockets
import sys      # for exit

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
try:
    s.bind((HOST, PORT))
    print 'Socket bind complete'
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
try: 
    s.listen(10)
    print 'Socket now listening on port [' + str(PORT) + ']'
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Now keep talking with the client
while 1:
    # Wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # TODO: catch exceptions here...
    data = conn.recv(1024)

    # TODO: validate this data before doing anything with it...
    print 'received data [' + data + '] sending OK'

    reply = 'OK: ' + data

    if not data: 
        break # Close the connection if we don't receive any data, not something you would normally allow a client to do
     
    # TODO catch exceptions here...
    conn.sendall(reply)

# TODO catch exceptions here...
conn.close()

print 'Connection Closed with ' + addr[0] + ':' + str(addr[1])

# TODO catch exceptions here...
s.close()

print 'Socket Closed' 
