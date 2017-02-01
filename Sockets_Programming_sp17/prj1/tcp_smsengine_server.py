#!/usr/bin/python
'''
Created on 01/31/2017

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
    
    while 1:
    	# do something
    s.close()
    print 'Socket Closed'

if __name__ == "__main__":


    args = sys.argv[1:]
    if len(args) < 2:
    	print 'Usage:Python tcp_smsengine_server.py port number filename.txt'
    	sys.exit()

    # Initialize variables
    PORT = (int)(args[0])
    filename = args[1]

    if (PORT == None) or (filename == None) :
        print "Please don't let port number or file name to be null."
        sys.exit()

    if (PORT.isdigit() not in range(1024,65536)):
        print "Bad port number: port number should between 1024 and 65536."
        sys.exit()
    # Read the spam words file
    s_words = []
    with open(filename,"r") as f :
        reader = csv.reader(f)
        for row in reader:
            s_words.append(row) # the list is for storing spam words
    f.close()

    runTCPServer()
        