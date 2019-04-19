import os
import time
import signal
import sys
from statusService import status
from voip import voipPhone
from threading import Thread


#parent process handles informing
#remote users of its status(server function)
#child process gathers emergency status
#of remote users(client function)

def implementationMode():
    
    #following 3 lines should be the first thing called in the program
    t1 = Thread(target=status.server) #running server on another thread
    t1.start() #starts thread
    voipPhone.initialize() #starts linphone process
    
    #start with some default message/location data
    
    #posts message
    status.postMsg('This is comp 1')
    
    #sets location info
    status.setLocation('123 Main St')
    
    #saves message and location data using pickle
    status.saveData()
    
    #loads message and location data
    status.loadData()
    
    #prints array of nearby nodes
    nodeList = status.runClient()
    print(nodeList)
    
    #posts message
    status.postMsg('computer 1')
    
    #changes emergency status to 1
    status.Emergency()
    
    #prints array of nearby nodes
    nodeList = status.runClient()
    print(nodeList)
    
    #changes emergency status to 0
    status.noEmergency()

    
    #prints array of nearby nodes
    nodeList = status.runClient()
    print(nodeList)
    
    #prints array of nearby nodes
    nodeList = status.runClient()
    print(nodeList)
    
    #the following code should be run before exiting out of the program
    status.terminateServer() #ends the listening socket on ther server
    t1.join() #joins the threads before terminating the program
    voipPhone.end_linphone() #ends linphone process


#this is just used for testing the code
#will be removed for actual implementation
userInput = input('Testing Mode: Enter 1 for server or 2 for client Implementation Mode: Enter 3(experimental) ')


if userInput == '1':
    status.server()    

elif userInput == '2':
    nodeList = status.runClient()
    print(nodeList)

elif userInput == '3':
    implementationMode()

else:
    print('Error')
