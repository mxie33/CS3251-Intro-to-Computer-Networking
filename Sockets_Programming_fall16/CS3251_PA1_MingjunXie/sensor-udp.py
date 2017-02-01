#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''

import socket   # for sockets
import sys      # for exit
import Util     # for random string generator and md5 hashing
import getopt   # for handling command line arguments
#Initialize global variable
TIMEOUT = 3 # 3s for time out restriction
MAX_TRIES = 3 # 3 times for maximum retries


def runUDPClient():
    # Create a UDP/IP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP socket
        print 'Socket created'
    except socket.error, msg:
        print 'Could not create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
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
    #create a random id for client
    clientID = Util.makeClientID()
    if (d):
        print "ClientID: ", clientID
    #########################################SEND REQUEST TO SERVER############################################
    # First the client send a request message to the server
    tries = 1
    while tries <= MAX_TRIES:
        try:
            request = clientID+",request"
            # Send Request to server
            if (d):
                print 'sending "%s"' % request
            sent = sock.sendto(request, server_address)
            break
        except socket.error or socket.timeout, msg:
            print "Request sent failed: ", msg, ". Try", tries, " time(s)"
            # if we reach max tries, print error and exit
            if (tries == MAX_TRIES):
                print "After 3 tries, still fail to send request. Socket close."
                sock.close()
                sys.exit()
            tries += 1

    ################################RECEIVE CHALLENGE STRING FROM SERVER#############################################
    msgResponded = False
    tries = 1
    challenge = None
    # Then the client will try to receive the challenge string from the server
    # Receive response
    while (not msgResponded) and (tries <= MAX_TRIES):

        if (d):
            print 'waiting to receive challenge string: try', tries, 'time(s)'
        # try to receive the challenge string
        try:
            challenge, thatserver_address = sock.recvfrom(4096)

            if (challenge != ""):
                msgResponded = True

            if (challenge == "Wrong request."):
                print "Wrong request, please send request again."
                sock.close()
                sys.exit()

        except socket.timeout, msg:
            print 'Challenge receive time out: ', msg
            tries += 1
            continue

        if (server_address != thatserver_address) :
            print 'Unknow server ip address: ', thatserver_address
            msgResponded = False
            tries += 1
            continue

    # If client doesn't receive challenge string after trying 3 times, client will exit
    if (not msgResponded):
        print 'Server failed to response request.'
        sock.close()
        sys.exit()

    # if client receives the challenge string, it will continuing sending information
    if (d):
        print 'received "%s"' % challenge

    #################################3##################SEND HASHMD5 TO SERVER##################################################
    #Then the client will do MD5 hash on the information
    tries = 1
    while tries <= MAX_TRIES:
        hashMD5 = Util.MD5(username, password, challenge)
        try :
            sent = sock.sendto(clientID+","+username + "," + hashMD5 + "," + sensorVal, server_address)
            break
        except socket.error or socket.timeout, msg:
            print "Authentication information send failed: ", msg, ". Try", tries, "time(s)" 
            # if we reach the max tries
            if (tries == MAX_TRIES):
                print "After 3 tries, still fail sending message. Close socket."
                sock.close()
                sys.exit()

            tries+=1
    if (d):
        print "HashMD5 sent! Waiting for response."

    #########################################################RESULT FROM SERVER################################################
    msgResponded = False
    tries = 1
    temp = None
    reponse = ""
    # Then the client will try to receive the challenge string from the server
    # Receive response
    while (not msgResponded) and (tries <= MAX_TRIES):

        if (d):
            print 'waiting to receive authentication result: try', tries, 'time(s)'
        
        # try to receive the result
        try:
            response, thatserver_address = sock.recvfrom(4096)
            # If we reach the end of the message, break out of this while loop
            # if our response isn't empty, we marked msgResponded = true
            if (response != ""):
                msgResponded = True

        except socket.timeout, msg:
            print 'Result receive time out: ', msg
            tries += 1
            continue

        if (server_address != thatserver_address) :
            print 'Unknow server ip address.'
            msgResponded = False
            tries += 1
            continue

    # Check if server responded
    if (not msgResponded):
        print "Server failed to respond user authentication."
        sock.close()
        sys.exit()

    print "Reply from server: \n", response
    print 'closing socket'
    sock.close()

if __name__ == "__main__":
    # Get the command line inputs
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:p:u:c:r:d",["server=","port=","username=","password=","sensorvalue="])
    except getopt.GetoptError as err:
        print err
        print 'Usage:Python Sensor.udp.py -s host name -p port number -u username -c password -r sensor value -d debug mode'

    #Initialize all variables
    d = False
    server = None
    port = None
    username = None
    password = None
    sensorVal = None

    # Read the command line
    for opt, arg in opts:
        if opt == '-h':
            print 'usage:'
            print sys.argv[0] + ' -s <host name> -p <port number> -u <username> -c <password> -r <sensorvalue> -d <debug mode>'
            sys.exit()
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-p", "--port"):
            if arg.isdigit():
                port = int(arg)
            else:
                print "Port number is not in digits."
                sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-c", "--password"):
            password = arg
        elif opt in ("-r", "--sensorvalue"):
            sensorVal = arg
        elif opt in ("-d"):
            d = True;

    if (server == None) or (port == None) or (username == None) or (password == None) or (sensorVal == None) :
        print "Please don't let server, port number, username, password or sensorvalue be null"
        sys.exit()
    if (port not in range(1024,65536)):
        print "Bad port number: port number should between 1024 and 65536."
        sys.exit()

    runUDPClient()
