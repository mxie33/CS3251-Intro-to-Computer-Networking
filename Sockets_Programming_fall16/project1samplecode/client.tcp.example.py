# Socket client example in python
# from: http://www.binarytides.com/python-socket-programming-tutorial/

import socket	# for sockets
import sys	# for exit
import getopt	# for handling command line arguments

server = 'www.google.com';
port = 80;
message = "GET / HTTP/1.1\r\n\r\n"

try:
   opts, args = getopt.getopt(sys.argv[1:],"hs:p:m:",["server=","port=","message="])
except getopt.GetoptError:
   print 'using default server [' + server + '] port [' + port + '] and message [' + message + ']'
for opt, arg in opts:
   if opt == '-h':
      print 'usage: '
      print sys.argv[0] + ' -s <server> -p <port> -m <message>'
      sys.exit()
   elif opt in ("-s", "--server"):
      server = arg
   elif opt in ("-p", "--port"):
      port = int(arg)
   elif opt in ("-m", "--message"):
      # This is a hack to allow you to send the same HTTP GET message as the previous example code
      # without having to deal with escaping the trailing whitespace on the command line
      message = arg + "\r\n\r\n"
      # alternatively, uncomment this
      #message = arg

# Create an INET, STREAMing socket (TCP)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
 
try:
    remote_ip = socket.gethostbyname( server )
    # Gracefully handles passing in an IP address as well as a DNS name
 
except socket.gaierror:
    # Could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
# Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + server + ' on ip ' + remote_ip
 
# Send some data to remote server
 
try :
    # Set the whole string
    s.sendall(message)
except socket.error:
    # Send failed
    print 'Send failed'
    sys.exit()
 
print '******************* SENDING MESSAGE FOLLOWS **************************'
print message
print 'sent successfully'
 
# Now receive 4096 bytes of data from the stream, drop the rest if we don't read again before closing
reply = s.recv(4096)

print '***************************** REPLY FOLLOWS *********************************'
print reply
print '***************************** END REPLY *********************************'

# Close the socket, signals that the application is ready to close the TCP connection
s.close()

print 'Socket Closed to ' + server + ' on ip ' + remote_ip
