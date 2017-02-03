#!/usr/bin/python
'''
Created on 02/02/2017

@author: Mingjun Xie
'''
import socket       # for sockets
import sys          # for exit
import string       # for string operation
#runUDPServer method
def runUDPServer():

    # create UDP/IP socket
    try:
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
        print 'Socket created'
    except socket.err, errmsg:
        print 'Could not create socket. Error Code : ' + str(errmsg[0]) + ' Message ' + errmsg[1]
        sys.exit()

    # Bind the socket to the port
    HOST = socket.gethostbyname(socket.gethostname())
    server_address = (HOST, PORT)

    try:
        udpSock.bind(server_address)
        print 'Bind complete: started on %s port %s' % server_address
    except socket.error, errmsg:
        print 'Bind failed. Error Code : ' + str(errmsg[0]) + ' Message ' + errmsg[1]
        sys.exit()

    while 1:
        # receive message from client
        try:
            data, clientAddress = udpSock.recvfrom(4096)
        except socket.error, errmsg:
            print "Request receive failed: ", errmsg
            continue

        reply = ""
        if len(data) == 0:
            reply = "0 -1 bad input"
        else:
            data = data.translate(None, string.punctuation)
            messages = data.split(" ")
            spam = 0.0
            s_words_reply = ""
            for word in messages:
                if word.lower() in s_words:
                    spam += 1
                    s_words_reply += " " + word
            scores = spam/len(messages)
            spam = spam % 2**32  # ???? cast into unsigned int
            reply = (str)(scores) + " " + (str)(spam) + " " + s_words_reply

        #send reply to the client
        try:
            sent = udpSock.sendto(reply, clientAddress)
        except socket.error, err:
            print 'Reply send fail: ', err
            continue

        print 'Reply sent successfully:\n', reply
        print 'sent %s bytes back to %s' % (sent, clientAddress)

    ########################reach the end of the communication###############################################################################
    #########################################################################################################################################

# main method for udp server
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print 'Usage:Python smsengineUDP.py portnumber filename.txt'
        sys.exit()

    # Initialize variables
    PORT = (int)(args[0])
    filename = args[1]

    if (PORT == None) or (filename == None) :
        print "Please don't let port number or file name to be null."
        sys.exit()

    if (PORT not in range(1024,65536)):
        print "Bad port number: port number should between 1024 and 65536."
        sys.exit()

    # Read the spam words file
    s_words = []
    f = open(filename, 'r')
    for row in f:
        row = row.replace('\n', "")
        s_words.append((str)(row)) # the list is for storing spam words
    f.close()

    runUDPServer()
