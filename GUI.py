import os
import re
import sys
import math
import time
import random
import signal
import threading
import tkinter as tk
from tkinter import ttk
from voip import voipPhone
from threading import Thread
from statusService import status

class HamPhone:
    def __init__(self, master):
        self.master=master
        #master.title('HamPhone')
        #master.resizable(False, False)
        #master.overrideredirect(1)
        master.geometry("480x800")
        style=ttk.Style()
        style.theme_create("biggerTabs", settings={
            "TNotebook.Tab": {"configure": {"padding": [10, 18], "font":('',22) },}})
        style.theme_use("biggerTabs")
        style.configure('TNotebook.Tab', focuscolor='gray70')
        style.map('TNotebook.Tab', background=[('selected', 'gray70')])
        
        self.n=ttk.Notebook(master)
        self.n.pack()
        
        self.f1=tk.Frame(self.n)
        self.f2=tk.Frame(self.n)
        self.f3=tk.Frame(self.n)
        self.f4=tk.Frame(self.n)
        self.f5=tk.Frame(self.n)
        self.f5.bind("<Visibility>", self.destroy)

        powerImg=tk.PhotoImage(file="power.gif")
        self.green=tk.PhotoImage(file="green2.png")
        self.green_small=self.green.subsample(3,3)
        self.red=tk.PhotoImage(file="red2.png")
        self.red_small=self.red.subsample(3,3)
        self.refresh_image=tk.PhotoImage(file="refresh.png")
        self.phone_image=tk.PhotoImage(file="phone.png")
        
        self.n.add(self.f1, text='Phone')
        self.n.add(self.f2, text='Nodes')
        self.n.add(self.f3, text='Status')
        self.n.add(self.f4, text='          ', state="disabled")
        self.n.add(self.f5, image=powerImg)
        self.n.img=powerImg

        self.numFrame=tk.Frame(self.f1)
        self.numFrame.grid(row=0, column=0)
            
        self.current_number=tk.StringVar()
        self.current_number.set('')
        self.call_number=tk.Label(self.numFrame, textvariable=self.current_number, width=23, bg='white',
                                  relief='sunken', height=2, font = ('' , 26), padx=5)
        self.call_number.grid(row=0, column=0)
        
        self.numpad=tk.Frame(self.f1)
        self.numpad.grid(row=1, column=0)

        self.Buttons=['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0']

        button_ipadding_x = 54
        button_ipadding_y = 13
        
        for i,n in enumerate(self.Buttons):
            self.num=tk.Button(self.numpad, text=n, command=lambda n=n:self.IPget(str(n)), relief=tk.GROOVE,
                               width=1, font = ('' , 45))
            self.num.grid(row=1+math.floor(i/3), column=i%3, ipadx=button_ipadding_x, ipady=button_ipadding_y)

        self.delete=tk.Button(self.numpad, text=u"\u2190", width=1, relief=tk.GROOVE,
                              command=lambda:self.current_number.set(self.current_number.get()[:-1]),
                              font = ('' , 45), fg='red', activeforeground='red')
        self.delete.grid(row=4, column=2, ipadx=button_ipadding_x, ipady=button_ipadding_y)
        
        self.command_Buttons=tk.Frame(self.f1)
        self.command_Buttons.grid(row=2, column=0)

        self.callText=tk.StringVar()
        self.callText.set('Call')
        self.call_button=tk.Button(self.command_Buttons, textvariable=self.callText,
                                   command=lambda:self.call(), relief=tk.RAISED, bg='#90EE90',
                                   activebackground="sea green", width=10, font=('',23))
        self.call_button.grid(row=0, column=1, ipadx=85, ipady=0)

        self.nodes=tk.Frame(self.f2)
        self.nodes.pack()
        self.getNodeList()

        self.refresh=tk.Button(self.f2, image=self.refresh_image, foreground='blue', font=('',20),
                               takefocus=False, height=40, width=40, command=lambda:self.ThreadTest())
        self.refresh.pack(side=tk.BOTTOM, anchor=tk.E)
        self.callstatus=0
        self.previouscallstatus=0
        self.callStatus()

        self.myLocation=tk.StringVar()
        self.myLocation.set(status.getLocation())
        self.LocLabel=tk.Label(self.f3, text="Node location:", font=('',20))
        self.LocLabel.grid(row=0, column=0, sticky=tk.W, pady=(10,0))
        self.currLocLabel=tk.Label(self.f3, textvariable=self.myLocation, font=('',14), fg='grey')
        self.currLocLabel.grid(row=1, column=0, sticky=tk.W)
        self.LocData=tk.Frame(self.f3)
        self.LocData.grid(row=2, column=0, sticky=tk.W)
        self.Loc=tk.Entry(self.LocData)
        self.Loc.pack(side=tk.LEFT, anchor=tk.W)
        self.locSet=tk.Button(self.LocData, text="SET", command=lambda:self.serverLocationSet())
        self.locSet.pack(side=tk.RIGHT)

        self.myStatus=tk.StringVar()
        self.myStatus.set(status.getMsg())
        self.statusLabel=tk.Label(self.f3, text="My status:", font=('',20))
        self.statusLabel.grid(row=3, column=0, sticky=tk.W, pady=(25,0))
        self.currStatusLabel=tk.Label(self.f3, textvariable=self.myStatus, font=('', 14), fg='grey')
        self.currStatusLabel.grid(row=4, column=0, sticky=tk.W)
        self.statusData=tk.Frame(self.f3)
        self.statusData.grid(row=5, column=0, sticky=tk.W)
        self.Status=tk.Entry(self.statusData)
        self.Status.pack(side=tk.LEFT, anchor=tk.W)
        self.statusSet=tk.Button(self.statusData, text="SET", command=lambda:self.serverStatusSet())
        self.statusSet.pack(side=tk.RIGHT)

        self.alertLabel=tk.Label(self.f3, text="Set alert:", font=('',20))
        self.alertLabel.grid(row=6, column=0, sticky=tk.W, pady=(25,5))
        self.alertButtonFrame=tk.Frame(self.f3)
        self.alertButtonFrame.grid(row=7, column=0, padx=35)
        self.noAlertButton=tk.Button(self.alertButtonFrame, image=self.green, fg='green', font=('',80),
                                     command=lambda:self.noAlert(), activeforeground="dark green",
                                     activebackground="gray50", width=180, height=180)
        self.noAlertButton.pack(side=tk.LEFT, ipadx=0)
        self.yesAlertButton=tk.Button(self.alertButtonFrame, image=self.red, fg='red', font=('',80),
                                      command=lambda:self.yesAlert(), activeforeground="red3",
                                      activebackground="gray50", width=180, height=180)
        self.yesAlertButton.pack(side=tk.RIGHT, ipadx=0)
        self.checkAlert()

        self.canvas = tk.Canvas(self.f3, width=460, height=180)  
        self.canvas.grid(row=8)  
        self.img = tk.PhotoImage(file="banner.gif")
        self.canvas.create_image(275, 110, image=self.img)

        self.tag=tk.Label(self.f3, text="Emilio Garcia and Vinay Shah, Capstone 2019")
        self.tag.grid(row=9, pady=25)
        self.t2 = Thread(target=self.getNodeList)
        
    def checkAlert(self):
        if status.getEmergency() == '1':
            self.yesAlert()
        elif status.getEmergency() == '0':
            self.noAlert()
        
    def ThreadTest(self):
        if not self.t2.is_alive():
            try:
                self.t2.start()
            except:
                self.t2 = Thread(target=self.getNodeList)
                self.t2.start()
        
    def serverStatusSet(self):
        self.myStatus.set(self.Status.get())
        status.postMsg(self.myStatus.get())
        status.saveData()
        
    def serverLocationSet(self):
        self.myLocation.set(self.Loc.get())
        status.setLocation(self.myLocation.get())
        status.saveData()

    def noAlert(self):
        self.noAlertButton.configure(relief=tk.SUNKEN, bg="gray70")
        self.yesAlertButton.configure(relief=tk.RAISED, bg="gray95")
        status.noEmergency()
        status.saveData()

    def yesAlert(self):
        self.noAlertButton.configure(relief=tk.RAISED, bg="gray95")
        self.yesAlertButton.configure(relief=tk.SUNKEN, bg="gray70")
        status.Emergency()
        status.saveData()

    def IPget(self, string):
        if len(self.current_number.get())<15:
            self.current_number.set(self.current_number.get()+string)
        else:
            self.error()

    def call(self):
        if bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",self.current_number.get())):
            print('Calling: ' + self.current_number.get())
            voipPhone.call(self.current_number.get())
            self.current_number.set('Calling...')
            self.callText.set('Hang up')
            self.call_button.configure(command=lambda:self.hangup(), bg='red', activebackground="firebrick3")
            self.call_number.configure(fg='black')
            self.master.after(1000, lambda:self.current_number.set(''))
            self.previouscallstatus=self.callstatus
            self.callstatus=2
        else:
            self.error()

    def hangup(self):
        print('Hanging up...')
        voipPhone.hangup()
        self.callText.set('Call')
        self.call_button.configure(command=lambda:self.call(), bg='#90EE90', activebackground="sea green")
        self.previouscallstatus=self.callstatus
        self.callstatus=0

    def error(self):
        self.call_number.configure(fg='red')
        self.master.after(125, lambda:self.call_number.configure(fg='black'))

    def colorGet(self, status):
        if self.status=='0':
            return self.green_small
        if self.status=='1':
           return self.red_small

    def getNodeList(self):
        self.nodes.destroy()
        reports = status.runClient()
        self.nodes=tk.Frame(self.f2)
        self.nodes.pack()

        for x,item in enumerate(reports):
            self.border=tk.Frame(self.nodes, bg='black', height=2, width=480)
            self.border.pack(fill=tk.X, pady=5)

            self.IP=item.split(':')[0]
            self.status=item.split(':')[1]
            self.msg=item.split(':')[2]
            self.payload=self.IP+' '+self.status+' '+self.msg
            self.entryFrame=tk.Frame(self.nodes, width=480, height=60)
            self.entryFrame.pack(fill=tk.X, pady=20)
            self.entryFrame.pack_propagate(0)
            
            self.nameFrame=tk.Frame(self.entryFrame)
            self.nameFrame.pack(side=tk.LEFT, padx=5)
            self.IPLabel=tk.Label(self.nameFrame, text=self.IP, font=('',16))
            self.IPLabel.pack(side=tk.TOP, anchor=tk.W)
            self.msgLabel=tk.Label(self.nameFrame, text=self.msg, font=('',12))
            self.msgLabel.pack(side=tk.BOTTOM, anchor=tk.W)
            
            self.controlFrame=tk.Frame(self.entryFrame)
            self.controlFrame.pack(side=tk.RIGHT)
            self.color=self.colorGet(self.status)
            self.statusLight=tk.Label(self.controlFrame, image=self.color, width=50, height=50)
            self.statusLight.pack(side=tk.RIGHT)
            self.callButton=tk.Button(self.controlFrame, image=self.phone_image, width=50, height=50, takefocus=False,
                                      command=lambda:self.nodeCall(self.IP))
            self.callButton.pack(side=tk.LEFT)
        self.border=tk.Frame(self.nodes, bg='black', height=2, width=480)
        self.border.pack(pady=5)
        #self.master.after(30000, lambda:self.getNodeList())

    def callStatus(self):
        content=voipPhone.callstatus()
        if content==0 and self.callstatus!=2:
            print("No incoming calls")
            if self.previouscallstatus==1:
                self.callText.set('Call')
                self.call_number.configure(fg='black')
        if content==1 and self.callstatus!=2:
            self.previouscallstatus=self.callstatus
            self.callstatus=1
            print("Incoming Call")
            self.callText.set('Accept Call')
            self.call_button.configure(command=lambda:voipPhone.answer())
            self.call_number.configure(fg='blue')
        if content==2:
            print("ongoing call")
            self.callText.set('Hangup')
            self.call_button.configure(command=lambda:self.hangup())
        self.master.after(3000, lambda:self.callStatus())

    def nodeCall(self,IP):
        self.n.select(0)
        self.current_number.set(IP)

    def destroy(self, event):
        status.terminateServer() #ends the listening socket on ther server
        t1.join() #joins the threads before terminating the program
        voipPhone.end_linphone() #ends linphone process
        self.master.destroy()
        
t1 = Thread(target=status.server) #running server on another thread
t1.start() #starts thread
voipPhone.initialize() #starts linphone process
status.loadData()
root=tk.Tk()
test=HamPhone(root)
root.mainloop()
