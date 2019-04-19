import socket
import os
import time
import signal
import sys
import pickle



#Emergency Status at Local Location
#0=no emergency 1=emergency

global localEmergencyStatus
localEmergencyStatus = '0'


global msg
msg = ''

global location
location = ''

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
    
def getMsg():
    return msg
    
def setLocation(newLocation):
    global location
    location = newLocation
    
def getLocation():
    return location
    
def terminateServer():
    global endServer
    endServer = 1
    try:
        client('127.0.0.1')
    
    except:
        pass
	
def saveData():
    lst2Save = [localEmergencyStatus, msg, location]
    pickle_out = open("data.pickle", "wb")
    pickle.dump(lst2Save, pickle_out)
    pickle_out.close

def loadData():
    try:
        pickle_in = open("data.pickle", "rb")
        global localEmergencyStatus
        global msg
        global location
        lst2Load = pickle.load(pickle_in)
        localEmergencyStatus = lst2Load[0]
        msg = lst2Load[1]
        location = lst2Load[2]
    
    except:
        print('No saved data found')


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
        
        if localEmergencyStatus == '0':
            msgToSend = localEmergencyStatus + ':' + msg
        else:
            msgToSend = localEmergencyStatus + ':' + location
        
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


