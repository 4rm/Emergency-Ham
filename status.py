import socket
import os
import time
import signal
import sys

#Emergency Status at Local Location
#0=no emergency 1=emergency
localEmergencyStatus = '0'

pid = 0

#server function tells remote users
#its emergency status
def server():

    listeningSocket = socket.socket()

    port = 10000
    listeningSocket.bind(('', port))

    listeningSocket.listen(10)

    while True:
        clientSocket, clientAddress = listeningSocket.accept()
        #print(f'Connected to {clientAddress}')
        print('Connected to ' + str(clientAddress))
        clientSocket.send(localEmergencyStatus.encode('ASCII'))
        clientSocket.close()
        #print(f'Connection to {clientAddress} closed')
        print('Connection closed to ' + str(clientAddress))

#client function gathers emergency status
#of remote users
def client(remoteAddress):
    client = socket.socket()
    port = 10000
    client.connect((remoteAddress, port))
    remoteEmergencyStatus = client.recv(1).decode('ASCII')
    client.close()
    #print(f'Emergency Status at Remote Location {remoteAddress} is {remoteEmergencyStatus}')
    print('Emergency status at remote location ' + remoteAddress + ' is ' + remoteEmergencyStatus)
    

#gets lists of client
#ip on the network
def getMeshNodes():
	os.system('java SSH_CONNECT > mesh_nodes')
	
def runClient():
    getMeshNodes()
    f = open("mesh_nodes", "r")
    for x in f:
	    remoteAddress = x
	    try:
	        client(remoteAddress)
	    except:
		    pass

#parent process handles informing
#remote users of its status(server function)
#child process gathers emergency status
#of remote users(client function)
def implementationMode():
    pid = os.fork()

    if pid > 0:	#parent process
        server()

    elif pid == 0:	#child process
        while (True):
            runClient()
            time.sleep(5)

    else:
        print('Fork Error')




#this is just used for testing the code
#will be removed for actual implementation
userInput = input('Testing Mode: Enter 1 for server or 2 for client Implementation Mode: Enter 3(experimental) ')

#signal handler for interrupts
def sigHandle(sig, frame):
	os.kill(pid, signal.SIGTERM)
	exit(0)

signal.signal(signal.SIGINT, sigHandle)

if userInput == '1':
    server()

elif userInput == '2':
    runClient()

elif userInput == '3':
    implementationMode()

else:
    print('Error')
