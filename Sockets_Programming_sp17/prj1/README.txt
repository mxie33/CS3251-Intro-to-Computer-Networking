1. Name: Mingjun Xie
2. Email: mxie33@gatech.edu
3. Submitted files:
	smsclientTCP.py -- sms tcp client program
	smsclientUDP.py -- sms UDP client program
	smsengineTCP.py -- sms tcp server program
	smsengineUDP.py -- sms UDP server program
	README.txt 	-- read me file
	sample.txt	-- sample out put of the project
4. Instructions for running the program:
	the command line should be like:
	python smsengineTCP.py portnumber filename.txt
	python smsclientTCP.py serverIP portnumber filename.txt
	python smsengineUDP.py portnumber filename.txt
	python smsclientUDP.py serverIP portnumber filename.txt
	Some examples:
	i.e. python smsengineTCP.py 8591 words.txt
	i.e. python smsclientTCP.py 127.0.1.1 8591 message.txt
5. Constraints
	port number can only be in range(1024,65536) in order to not using reserved port for other protocols.
	
