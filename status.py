import socket
import os
import time
import signal
import sys

#Emergency Status at Local Location
#0=no emergency 1=emergency
localEmergencyStatus = '0'

#Address of remote location
#This will be given a list of
#addresses from arp
remoteAddress = '127.0.0.1'


#server function tells remote users
#its emergency status
def server():

    listeningSocket = socket.socket()

    port = 10000
    listeningSocket.bind(('', port))

    listeningSocket.listen(10)

    while True:
        clientSocket, clientAddress = listeningSocket.accept()
        print(f'Connected to {clientAddress}')
        clientSocket.send(localEmergencyStatus.encode('ASCII'))
        clientSocket.close()
        print(f'Connection to {clientAddress} closed')

#client function gathers emergency status
#of remote users
def client():
    client = socket.socket()
    port = 10000
    client.connect((remoteAddress, port))
    remoteEmergencyStatus = client.recv(1).decode('ASCII')
    client.close()
    print(f'Emergency Status at Remote Location {remoteAddress} is {remoteEmergencyStatus}')

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
            client()
            time.sleep(2)

    else:
        print('Fork Error')




#this is just used for testing the code
#will be removed for actual implementation
userInput = input('Testing Mode: Enter 1 for server or 2 for client Implementation Mode: Enter 3(experimental) ')



if userInput == '1':
    server()

elif userInput == '2':
    client()

elif userInput == '3':
    implementationMode()

else:
    print('Error')
