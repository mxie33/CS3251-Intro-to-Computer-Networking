#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''
import socket   # for sockets
import sys  # for exit
import getopt   # for handling command line arguments
import Util


def runTCPClient():  
    # Create an INET, STREAMing socket (TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
    if (d):
        print 'Socket Created'

    # Get the server IP
    try:
        serverIP = socket.gethostbyname(server)
        if (d):
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
        if (d):
            print 'Socket Connected to ' + server + ' on ip ' + serverIP
    except socket.error, msg:
        print 'Connection error: ', msg
        s.close()
        sys.exit()

    # Send the request to remote server

    try :
        requestMsg = "request"
        # Send the request string
        s.send(requestMsg)
    except socket.error:
        # Send failed
        print 'Send failed'
        s.close()
        sys.exit()

    # Receive the challenge string from the server
    challenge = ""
    try:
        challenge = s.recv(4096)
    except socket.error, msg:
        print "Challenge string accept error:" , msg
        s.close()
        sys.exit()

    hashMD5 = Util.MD5(username, password, challenge)
    try :
        s.sendall(username + "," + hashMD5 + "," + sensorVal)
    except socket.error, msg:
        print "Authentication information send failed: ", msg
        s.close()
        sys.exit()

    response = s.recv(4096)
    print "Reply from server: \n", response
    # Close the socket, signals that the application is ready to close the TCP connection
    print 'Socket Closed to ' + server + ' on ip ' + socket.gethostbyname(socket.gethostname())
    s.close()


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:p:u:c:r:d",["server=","port=","username=","password=","sensorvalue="])
    except getopt.GetoptError as err:
        print err
        print 'Usage:Python Sensor.tcp.py -s host name -p port number -u username -c password -r sensor value -d debug mode'

    d = False
    server = None
    port = None
    username = None
    password = None
    sensorVal = None

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
        print "Bad port number: port number should goes between 1024 and 65536."
        sys.exit()
    if d:
        print "server host name: ", server
        print "server port number: ", port
        print "username:", username
        print "password:", password     
        print "sensor value:", sensorVal
    runTCPClient()
