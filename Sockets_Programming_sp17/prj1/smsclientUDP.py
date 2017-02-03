#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''

import socket   # for sockets
import sys      # for exit
import string   # for string operation

#Initialize global variable
TIMEOUT = 2 # 2s for time out restriction
MAX_TRIES = 3 # 3 times for maximum retries

def runUDPClient():
    # Create a UDP/IP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP socket
        print 'Socket created'
    except socket.error, errmsg:
        print 'Could not create socket. Error Code : ' + str(errmsg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Try to extract the ip address
    try:
        serverIP = socket.gethostbyname(server)
        # handles IP address as input without error
    except socket.gaierror:
        #could not resolve
        print 'Hostname ' + server + ' could not be resolved. Exiting'
        sys.exit()

    # get the address with ip address and port number
    server_address = (serverIP, port)
    # Set time out to be 3s
    sock.settimeout(TIMEOUT)

    # the client send a message to the server
    try:
        sent = sock.sendto(msg, server_address)
    except socket.error, errmsg:
        print "message sent failed: ", errmsg, ". Try", tries, " time(s)"

    # receive the result from server
    msgResponded = False
    tries = 1
    reponse = ""

    while (not msgResponded) and (tries <= MAX_TRIES):
        # try to receive the result
        try:
            response, thatserver_address = sock.recvfrom(4096)
            # If we reach the end of the message, break out of this while loop
            # if our response isn't empty, we marked msgResponded = true
            if (response != ""):
                msgResponded = True
        except socket.timeout, err:
            print 'Result receive error: ', err, 'after try ', tries, 'times.'
            handleTimeout(tries, sock)
            tries += 1
            continue

    print "Reply from server: \n", response
    print 'Socket closed'
    sock.close()

def handleTimeout(tries, socket):
    if (tries == MAX_TRIES):
        print "After 3 tries, still fail to receive response. Socket close."
        socket.close()
        sys.exit()

if __name__ == "__main__":
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
    f = open(file, 'r')
    for row in f:
        row = row.replace('\n', "")
        msg += (str)(row) # the list is for storing spam words
    f.close()

    runUDPClient()
