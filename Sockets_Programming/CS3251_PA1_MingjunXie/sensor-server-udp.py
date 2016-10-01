#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''
import socket       # for sockets
import sys          # for exit
import Util         # for random string generator and md5 hashing
import csv          # for reading csv file
import math         # for calculating min max and avg
import getopt       # for handling command line arguments
from time import localtime, strftime #for printing time string
#Initialize global variable
TIMEOUT = 3
MAX_TRIES = 3

#runUDPServer method
def runUDPServer():
    allAvg = 0
    datasize = 0
    clientStateDict = {}
    #########################################################################################################################
    ##########################################################Create a UDP/IP socket#########################################
    try:
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
        print 'Socket created'
    except socket.err, msg:
        print 'Could not create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Bind the socket to the port
    HOST = socket.gethostbyname(socket.gethostname())
    server_address = (HOST, PORT)
    #udpSock.settimeout(TIMEOUT)

    try:
        udpSock.bind(server_address)
        print 'Bind complete: started on %s port %s' % server_address
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    while 1:
    #########################################################################################################################
    ##################################Receiving Request and send challenge string############################################
        if (d):
            print 'waiting to receive message'
        try:
            data, clientAddress = udpSock.recvfrom(4096)
        except socket.error, msg:
            print "Request receive failed: ", msg
            continue

        # if server receive data from client
        # print request when in debug mode
        if (d and data):
            print 'received %s bytes from %s' % (len(data), clientAddress)
            print 'received request [' + data + '] sending OK'
        data = data.split(",")
        clientID_Request= data[0]
        # check if data is request
        # if request, the server will continue to send challenge string
        if (data[1] == "request"):
            challenge = Util.randomString()
            clientStateDict[clientID_Request] = [challenge, "request"]
            if (d):
                print "Challenge string: ", challenge
            try:
                sent = udpSock.sendto(challenge, clientAddress)
            except socket.error, err:
                print 'Challenge string send failed: ' + err
                del clientStateDict[clientID_Request]
                continue
        else:
            sent = udpSock.sendto("Wrong request.",clientAddress)
            continue
        #########################################################################################################################
        #####################################################User authentication#################################################
        # Then we receive info from client address
        info = ""
        # try to receive the user info
        try:
            # receiving the user information
            info, clientAddress = udpSock.recvfrom(4096)
            if (d):
                print "receive data from ", clientAddress
                print info
            # checking if info is empty
            if (info == ""):
                sent = udpSock.sendto("User info not received!",clientAddress)
                print "Info was not received, please request again."
                continue

        except socket.error,err:
            print 'User info receive failed: ', err

        if (d):
            print "Successfully received: \n", info

        # information received successfully
        info = info.split(",")
        clientID_Authentication = info[0]
        if not clientStateDict.has_key(clientID_Authentication) or clientStateDict[clientID_Authentication][1] != "request":
            print "Client: ", clientID_Authentication, " not exist or in wrong state."
            continue
        username = info[1] # the username received from client
        #Initialize the reply message
        reply = " "
        if not userDict.has_key(username):
            reply = "Invalid username:" + username + ", User authentication failed."
        else :
            password = userDict[username][0] #password from user dict
            hashmd5 = info[2] #the server received md5 from client
            try:
                sensorValue = (float)(info[3]) # senser value received from client
            except ValueError:
                print "Bad sensor value!"
                try:
                    sent = udpSock.sendto("Bad sensor value!", clientAddress)
                except socket.error, err:
                    print 'Reply send fail: ', msg
                    continue
                continue
            challenge = clientStateDict[clientID_Authentication][0]
            smd5 = Util.MD5(username, password, challenge)
            if (d):
                print "password: ", password
                print "hashmd5: ", hashmd5
                print "sensor value: ", sensorValue
                print "smd5: ", smd5

            # now we check the information
            if hashmd5 != smd5:
                reply = "Hash not matched, password maybe wrong. User authentication failed."
            else:
                dataList = userDict[username][1]
                dataList.append(sensorValue)
                datasize += 1
                minVal = min(dataList)
                maxVal = max(dataList)
                avg = (float)(sum(dataList))/len(dataList)
                allAvg = (float) ((allAvg * (datasize-1))+ sensorValue)/datasize
                reply = "Sensor: "+username+" recorded: "+(str)(sensorValue)+" time: "+strftime("%Y-%m-%d %H:%M:%S", localtime())+" sensorMin: "+(str)(minVal)+" sensorAvg: "+(str)(avg)+" sensorMax: "+(str)(maxVal)+" allAvg: "+(str)(allAvg)
        del clientStateDict[clientID_Authentication]
        #send reply to the client
        try:
            sent = udpSock.sendto(reply, clientAddress)
        except socket.error, err:
            print 'Reply send fail: ', msg
            continue

        print 'Reply sent successfully:\n', reply
        print 'sent %s bytes back to %s' % (sent, clientAddress)

    ########################reach the end of the communication###############################################################################
    #########################################################################################################################################

# main method for udp server
if __name__ == "__main__":
    #########################################################################################################################
    #########################################Handling command line inputs####################################################
    try:
        opts, args = getopt.getopt(sys.argv[1:],"p:f:d",["server=","file=","debug="])
    except getopt.GetoptError as err:
        print err
        print 'Usage:Python sensor.server.tcp.py -p port number -f filename.csv -d debug mode'
    # Initialize variables
    d = False
    PORT = None
    filename = None

    for opt, arg in opts:
        if opt == '-h':
            print 'usage:'
            print sys.argv[0] + ' -s <host name> -p <port number> -u <username> -c <password> -r <sensorvalue> -d <debug mode>'
            sys.exit()
        elif opt in ("-p", "--port"):
            if arg.isdigit():
                PORT = int(arg)
            else:
                print "Port number is not in digits."
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-d"):
            d = True;

    if (PORT == None) or (filename == None) :
        print "Please don't let port number or file name to be null."
        sys.exit()

    ###########################################################################################################################
    ###################################################Read the csv file#######################################################

    userDict = {}
    try:
        with open(filename,"r") as f :
            reader = csv.reader(f)
            for row in reader:
                #we store username and password pair in the dictionary
                userDict[row[0]] = (row[1],[]) # the list is for storing sensor value
            if (d):
                print userDict
        f.close()
    except:
        print "File open failed."
        sys.exit()
    #########################################################################################################################
    ##################################################run UDP Server#########################################################
    runUDPServer()
