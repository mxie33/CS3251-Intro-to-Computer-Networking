#!/usr/bin/python
'''
Created on 01/31/2017

@author: Mingjun Xie
'''
import socket   # for sockets
import sys      # for exit
import string   # for string operation

def runTCPServer():

    # Create an INET, STREAMing socket (TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print 'Socket created'
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    # bind the socket with the port
    try:
        HOST = socket.gethostbyname(socket.gethostname())
        print "Server IP:",HOST
        s.bind((HOST, PORT))
        #print 'Socket bind complete'
    except socket.error , errmsg:
        print 'Bind failed. Error Code : ' + str(errmsg[0]) + ' Message ' + errmsg[1]
        sys.exit()

    try:
        s.listen(10) # max number for listen is 10
        print 'Socket now listening on port [' + str(PORT) + ']'
    except socket.error, errmsg:
        print 'Bind failed. Error Code : ' + str(errmsg[0]) + ' Message ' + errmsg[1]
        sys.exit()

    while 1:
    	# connect with client TCP
        conn, addr = s.accept()
        # print 'Connected with ' + addr[0] + ':' + str(addr[1])
        data = ""
        try:
            #receive the message from client
            data = conn.recv(1024)
        except socket.error, err:
            print 'Request receive Failed: ' + err
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

        try:
            conn.sendall(reply)
        except socket.error, err:
            print 'Reply send fail: ', err
            continue
        #print "Reply sent successfully:\n", reply
    s.close()
    print 'Socket Closed'

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) < 2:
    	print 'Usage:Python smsengineTCP.py portnumber filename.txt'
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

    runTCPServer()
        