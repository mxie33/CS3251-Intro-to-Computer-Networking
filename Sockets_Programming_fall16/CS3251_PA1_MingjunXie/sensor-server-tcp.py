#!/usr/bin/python
'''
Created on 09/30/2016

@author: Mingjun Xie
'''
import socket   # for sockets
import sys      # for exit
import Util     # for random string generator and md5 hashing
import csv      # for reading csv file
import math    # for calculating min max and avg
import getopt   # for handling command line arguments
from time import localtime, strftime # for time string


def runTCPServer():
    #initialize static variable
    datasize = 0
    allAvg = 0
    # Create an INET, STREAMing socket (TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (d):
            print 'Socket created'
    except socket.error:
        print 'Failed to create socket'
        sys.exit()


    # bind the socket with the port
    try:
        HOST = socket.gethostbyname(socket.gethostname())
        if (d):
            print "Server IP:",HOST
        s.bind((HOST, PORT))
        if (d):
            print 'Socket bind complete'
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    try:
        s.listen(10) # max number for listen is 10
        print 'Socket now listening on port [' + str(PORT) + ']'
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Now we accpet a call from a client and keep talking to it
    while 1:
        # Wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        try:
            #receive the request from client
            data = conn.recv(1024)
        except socket.error, err:
            print 'Request receive Failed: ' + err
            continue
        print "Request Received."
        if (d):
            print 'received request [' + data + '] sending OK'
        if data == "request":
            challenge = Util.randomString()
            if (d):
                print "Challenge: ", challenge
            try:
                conn.sendall(challenge)
            except socket.error, err:
                print 'Challenge string send failed: ' + err
                continue

            info = ""
            try:
                data = conn.recv(1024)
                info = data
                if (d):
                    print info
                info = info.split(",")
            except socket.error, err:
                print 'User info receive failed: ' + err
                continue

            username = info[0] # the username received from client
            reply = ""
            if not userDict.has_key(username):
                reply = "Invalid username:" + username + ", User authentication failed."
            else :    
                password = userDict[username][0] #password from user dict
                hashmd5 = info[1] #the server received md5 from client
                
                try:
                    sensorValue = (float)(info[2]) # senser value received from client
                except ValueError:
                    try:
                        conn.sendall("Bad sensor value.")
                    except socket.error, err:
                        print 'Reply send fail: ', err
                        conn.close()
                        print 'Connection Closed with ' + addr[0] + ':' + str(addr[1])
                        continue
                    conn.close()
                    print 'Connection Closed with ' + addr[0] + ':' + str(addr[1])
                    continue

                smd5 = Util.MD5(username, password, challenge)
                if (d):
                    print "password: ", password
                    print "hashmd5: ", hashmd5
                    print "sensor value: ", sensorValue
                    print "smd5: ", smd5

                # now we check the informatison
                if hashmd5 != smd5:
                    reply = "Hash not matched. User authentication failed."
                else:
                    dataList = userDict[username][1]
                    dataList.append(sensorValue)
                    datasize += 1
                    minVal = min(dataList)
                    maxVal = max(dataList)
                    avg = (float)(sum(dataList))/len(dataList)
                    allAvg = (float) ((allAvg * (datasize-1))+ sensorValue)/datasize
                    reply = "Sensor: "+username+" recorded: "+(str)(sensorValue)+" time: "+strftime("%Y-%m-%d %H:%M:%S", localtime())+" sensorMin: "+(str)(minVal)+" sensorAvg: "+(str)(avg)+" sensorMax: "+(str)(maxVal)+" allAvg: "+(str)(allAvg)
            try:
                conn.sendall(reply)
            except socket.error, err:
                print 'Reply send fail: ', err
            print "Reply sent successfully:\n", reply
        conn.close()
        print 'Connection Closed with ' + addr[0] + ':' + str(addr[1])

    s.close()
    print 'Socket Closed'

if __name__ == "__main__":

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
    if (PORT not in range(1024,65536)):
        print "Bad port number: port number should between 1024 and 65536."
        sys.exit()
    # Read the csv file
    userDict = {}
    with open(filename,"r") as f :
        reader = csv.reader(f)
        for row in reader:
            #we store username and password pair in the dictionary
            userDict[row[0]] = (row[1],[]) # the list is for storing sensor value
        if (d):
            print userDict
    f.close()

    runTCPServer()
        