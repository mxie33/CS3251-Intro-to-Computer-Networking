Class:CS3251-Computer Networking I
Date: 2016.09.30
Name: Mingjun Xie
GTID:903074907
Email:mxie33@gatech.edu

FILES:
Util.py: This file contains several important function for the socketprogramming, for example the md5 hash algorithm.
Sensor-tcp.py: the sensor tcp python file
Sensor-server-tcp.py: the sensor server tcp python file
Sensor-udp.py: the sensor udp python file
sensor-server-udp.py: the sensor server udp python file
password.csv: the sample username and password pair file
SampleOutput_mxie33.txt: This is the sample out put report with several cases tested.

Run the command below for tcp/ip udp/ip client server program running:
debug mode is optional
python sensor-tcp.py -s <host address> -p <port number> -u <username> -c <password> -r <recorded sensor value> (-d <debug mode>)
python sensor-server-tcp.py -p <port number> -f <filename.csv> (-d <debug mode>)
python sensor-udp.py -s <host address> -p <port number> -u <username> -c <password> -r <recorded sensor value> (-d <debug mode>)
python sensor-server-udp.py -p <port number> -f <filename.csv> (-d <debug mode>)

Run the command below for testing socket programming files
bash testing-tcp.sh
bash testing-udp.sh

FYI, if you run chmod +x *.py, you can run myfiles with ./xxx.py
for example:
First type this line in the command line
chomd +x *.py
Then you can run:
./sensor-server-tcp.py -p 8591 -f password.csv -d

Functionality:
1.authentication handling
2.sensor transacrtion and result
3.multiple transactions and results from the same sensor
4.multiple transactions and results from different sensors
5.handling multiple transactions from different sensors sending simultaneously

Protocol description:
This application will require a online authentication thorough checking username and password, and it can record value from sensor and do calculations such as mean and max, min.
To make this application work, firstly, the server must keep running on the machine to wait for receiving messages.
The sensor will send a request string to the server before sending user information and get a random 64-character-string from the server.
If the server checked the data is "request", the server will send the random 64 character string from the server.
After receiving the 64-character-string, the sensor is acknowledged to be ready to start the user authentication with server and will use MD5 algorithm to hash a concatenated string of username,password and the 64-character-string.The user authentication requires a unhashed username together with the md5 hashed string and the sensor value it recorded. After preparing the information required by user authentication, the sensor client will send the string to the server.
If the server receive the user information successfully, it will use the unhashed username to find the correct password that paired with the username and then do the same md5 hashing on the concatenated string of username,password and the 64 character string which is the one that the server sent to client before. After checking the user informating through comapre the two hashed string, if the user authentication is passed, the server will continue to do calculations with the client's data history as well as adding the the recorded value to this data history. But if the user authentication is not passed, the server will find which part is wrong and send the result to the client to report the error.
After sending the final result, the conversation between client and server will be terminated.
And the client's socket will be closed and the server will keep running and waiting for next client and their messages.

Limitation:
The command line need to be in exactly that order to make server/client running.


