import os

#starts linphone daemon
def initialize():
	os.system("linphonecsh init")

#input ip address to call	
def call(ip_address):
	header = "linphonecsh dial sip:linphone@"
	os.system(header+ip_address)

#answers call	
def answer():
	os.system("linphonecsh generic answer")

#hangup call	
def hangup():
	os.system("linphonecsh generic terminate")

#end linphone daemon
def end_linphone():
	os.system("linphonecsh exit")
	




