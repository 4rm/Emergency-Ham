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
    
    
    t1 = Thread(target=status.server) #running server on another thread
    t1.start()
    
    
    nodeList = status.runClient()
    print(nodeList)
    
    status.Emergency() #sets emergency status
    
    nodeList = status.runClient()
    print(nodeList)
    
    
    
    nodeList = status.runClient()
    print(nodeList)
    
    nodeList = status.runClient()
    print(nodeList)
    
    status.terminateServer() #ends the listening socket on ther server
    t1.join() #joins the threads before terminating the program


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
