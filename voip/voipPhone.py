import os

#starts linphone daemon
def initialize():
	os.system("linphonecsh init -c ~/.linphonerc")

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

#get call status
def callstatus():
        current_status=os.popen("linphonecsh generic calls").read()
        if current_status=="No active call.\n":
                return "None"
        elif current_status.split("|")[6].strip()=='IncomingReceived':
                return "Inc"
        elif current_status.split("|")[6].strip()=='StreamsRunning':
                return "Ong"
                        
	




