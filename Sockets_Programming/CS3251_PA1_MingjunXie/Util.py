import sys
import hashlib
import random, string

#MD5 hashing algorithm
# Source from md5 source shared by TA
def MD5(username, password, challenge):
	string = username+password+challenge
	return hashlib.md5(string).hexdigest()

# Random 64 character String generator
# Source from stackoverflow
def randomString(length=64):
   return ''.join(random.choice(string.lowercase) for i in range(length))

# Random a Client ID for distinguish different clients
def makeClientID(length=11):
	return ''.join(random.choice(string.lowercase+string.digits) for i in range(length))