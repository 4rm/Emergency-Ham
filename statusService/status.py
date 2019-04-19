import socket
import os
import time
import signal
import sys




#Emergency Status at Local Location
#0=no emergency 1=emergency

global localEmergencyStatus
localEmergencyStatus = '0'


global msg
msg = ''

#cleanly terminate server
global endServer
endServer = 0


def Emergency():
    global localEmergencyStatus
    localEmergencyStatus = '1'
	
def noEmergency():
    global localEmergencyStatus
    localEmergencyStatus = '0'
    
def postMsg(newMsg):
    global msg
    msg = newMsg
    
def terminateServer():
    global endServer
    endServer = 1
    try:
        client('127.0.0.1')
    
    except:
        pass


#server function tells remote users
#its emergency status
def server():
    
    listeningSocket = socket.socket()

    port = 10000
    listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    listeningSocket.bind(('', port))

    listeningSocket.listen(10)
    
    global endServer
    while endServer==0:
        clientSocket, clientAddress = listeningSocket.accept()
        print('Connected to ' + str(clientAddress))
        
        msgToSend = localEmergencyStatus + ':' + msg
        
        #clientSocket.send(localEmergencyStatus.encode('ASCII'))
        clientSocket.send(msgToSend.encode('ASCII'))        
        clientSocket.close()
        print('Connection closed to ' + str(clientAddress))
    
    listeningSocket.close()
    endServer = 0

#client function gathers emergency status
#of remote users
def client(remoteAddress):
    client = socket.socket()
    port = 10000
    client.connect((remoteAddress, port))
    #remoteEmergencyStatus = client.recv(1).decode('ASCII')
    receivedMsg = client.recv(50).decode('ASCII')
    
    client.close()
    #print('Emergency status at remote location ' + remoteAddress + ' is ' + remoteEmergencyStatus)
    #return remoteAddress[:-1] + ':' + remoteEmergencyStatus
    return remoteAddress[:-1] + ':' + receivedMsg
    

#gets lists of client
#ip on the network
def getMeshNodes():
    os.system('java SSH_CONNECT > mesh_nodes')

	
def runClient():
    getMeshNodes()
    nodeList = []
    f = open("mesh_nodes", "r")
    for x in f:
	    remoteAddress = x
	    try:
	        node = client(remoteAddress)
	        nodeList.append(node)
		
	    except:
	        pass
		    
    
    return nodeList


