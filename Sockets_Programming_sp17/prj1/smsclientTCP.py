#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''
import socket   # for sockets
import sys  # for exit

def runTCPClient():  
    
    # Create an INET, STREAMing socket (TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, errmsg:
        print 'Failed to create socket: ', errmsg
        sys.exit()

    #print 'Socket Created'

    # Get the server IP
    try:
        serverIP = socket.gethostbyname(server)
        print "serverIP: ", serverIP
        # Handles passing in an IP address as well as a DNS name
    except socket.gaierror:
        # Host name could not resolve
        print 'Hostname could not be resolved. Exiting'
        s.close()
        sys.exit()

    # Connect to the server
    try:
        s.connect((serverIP , port))
        print 'Socket Connected to ' + server + ' on ip ' + serverIP
    except socket.error, errmsg:
        print 'Connection error: ', errmsg
        s.close()
        sys.exit()

    # Send the message to remote server
    try :
        # Send the request string
        s.send(msg)
    except socket.error:
        # Send failed
        print 'Send failed'
        s.close()
        sys.exit()

    # Receive the reply from the server
    response = ""
    try:
        response = s.recv(4096)
    except socket.error, errmsg:
        print "reply accept error:" , errmsg
        s.close()
        sys.exit()

    print "Reply from server: \n", response
    # Close the socket, signals that the application is ready to close the TCP connection
    #print 'Socket Closed to ' + server + ' on ip ' + socket.gethostbyname(socket.gethostname())
    s.close()

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 3:
        print 'usage:'
        print sys.argv[0] + ' <host name> <port number> <file.txt>'
        sys.exit()

    server = args[0]
    port = (int)(args[1])
    file = args[2]

    if (port not in range(1024,65536)):
        print "Bad port number: port number should goes between 1024 and 65536."
        sys.exit()
    # read file
    msg = ""
    
    # Read the message file
    try:
        f = open(file, 'r')
        for row in f:
            row = row.replace('\n', "")
            msg += (str)(row)
        f.close()
    except IOError, err:
        print "IO error: ", err
        sys.exit()

    runTCPClient()