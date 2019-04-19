import tkinter as tk
import math
import random
import re
from tkinter import ttk

class HamPhone:
    def __init__(self, master):
        self.master=master
        master.title('HamPhone')
        master.resizable(False, False)
        master.overrideredirect(1)
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

        self.refresh=tk.Button(self.f2, text=u"\uD83D\uDDD8", foreground='blue', font=('',20),
                               takefocus=False, height=0, width=0, command=self.getNodeList)
        self.refresh.pack(side=tk.BOTTOM, anchor=tk.E)
        self.callstatus=0
        self.previouscallstatus=0
        self.callStatus()

        self.myLocation=tk.StringVar()
        self.myLocation.set('test_address, test_state, test_zip')
        self.LocLabel=tk.Label(self.f3, text="Node location:", font=('',20))
        self.LocLabel.grid(row=0, column=0, sticky=tk.W, pady=(10,0))
        self.currLocLabel=tk.Label(self.f3, textvariable=self.myLocation, font=('',14), fg='grey')
        self.currLocLabel.grid(row=1, column=0, sticky=tk.W)
        self.LocData=tk.Frame(self.f3)
        self.LocData.grid(row=2, column=0, sticky=tk.W)
        self.Loc=tk.Entry(self.LocData)
        self.Loc.pack(side=tk.LEFT, anchor=tk.W)
        self.locSet=tk.Button(self.LocData, text="SET", command=lambda:self.myLocation.set(self.Loc.get()))
        self.locSet.pack(side=tk.RIGHT)

        self.myStatus=tk.StringVar()
        self.myStatus.set('test_message')
        self.statusLabel=tk.Label(self.f3, text="My status:", font=('',20))
        self.statusLabel.grid(row=3, column=0, sticky=tk.W, pady=(25,0))
        self.currStatusLabel=tk.Label(self.f3, textvariable=self.myStatus, font=('', 14), fg='grey')
        self.currStatusLabel.grid(row=4, column=0, sticky=tk.W)
        self.statusData=tk.Frame(self.f3)
        self.statusData.grid(row=5, column=0, sticky=tk.W)
        self.Status=tk.Entry(self.statusData)
        self.Status.pack(side=tk.LEFT, anchor=tk.W)
        self.statusSet=tk.Button(self.statusData, text="SET", command=lambda:self.myStatus.set(self.Status.get()))
        self.statusSet.pack(side=tk.RIGHT)

        self.alertLabel=tk.Label(self.f3, text="Set alert:", font=('',20))
        self.alertLabel.grid(row=6, column=0, sticky=tk.W, pady=(25,5))
        self.alertButtonFrame=tk.Frame(self.f3)
        self.alertButtonFrame.grid(row=7, column=0, padx=35)
        self.noAlertButton=tk.Button(self.alertButtonFrame, text=u"\uD83D\uDFD2", fg='green', font=('',80),
                                     command=lambda:self.noAlert(), activeforeground="dark green",
                                     activebackground="gray50")
        self.noAlertButton.pack(side=tk.LEFT, ipadx=15)
        self.yesAlertButton=tk.Button(self.alertButtonFrame, text=u"\uD83D\uDFD2", fg='red', font=('',80),
                                      command=lambda:self.yesAlert(), activeforeground="red3",
                                      activebackground="gray50")
        self.yesAlertButton.pack(side=tk.RIGHT, ipadx=15)
        self.noAlert()

        self.canvas = tk.Canvas(self.f3, width=460, height=180)  
        self.canvas.grid(row=8)  
        self.img = tk.PhotoImage(file="banner.gif")
        self.canvas.create_image(275, 110, image=self.img)

        self.tag=tk.Label(self.f3, text="Emilio Garcia and Vinay Shah, Capstone 2019")
        self.tag.grid(row=9, pady=25)

    def noAlert(self):
        self.noAlertButton.configure(relief=tk.SUNKEN, bg="gray70")
        self.yesAlertButton.configure(relief=tk.RAISED, bg="gray95")

    def yesAlert(self):
        self.noAlertButton.configure(relief=tk.RAISED, bg="gray95")
        self.yesAlertButton.configure(relief=tk.SUNKEN, bg="gray70")

    def IPget(self, string):
        if len(self.current_number.get())<15:
            self.current_number.set(self.current_number.get()+string)
        else:
            self.error()

    def call(self):
        if bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",self.current_number.get())):
            print('linphonecsh dial sip:linphone@' + self.current_number.get())
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
        self.callText.set('Call')
        self.call_button.configure(command=lambda:self.call(), bg='#90EE90', activebackground="sea green")
        self.previouscallstatus=self.callstatus
        self.callstatus=0

    def error(self):
        self.call_number.configure(fg='red')
        self.master.after(125, lambda:self.call_number.configure(fg='black'))

    def colorGet(self, status):
        if self.status=='0':
            return 'green'
        if self.status=='1':
           return 'red'

    def testNodeList(self):
        reports1=["192.168.1.1:0:All clear here"]
        reports2=["192.168.1.1:0:All clear here","24.47.135.177:1:Send help! We're trapped!"]
        reports3=["192.168.1.1:0:All clear here","24.47.135.177:1:Send help! We're trapped!",
                  "42.76.145.188:1:Emergency! We require assistance, please call!"]
        reports=[reports1, reports2, reports3]
        randint=random.randrange(3)
        return reports[randint]

    def getNodeList(self):
        self.nodes.destroy()
        reports=self.testNodeList()
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
            self.msgLabel.pack(side=tk.BOTTOM)
            
            self.controlFrame=tk.Frame(self.entryFrame)
            self.controlFrame.pack(side=tk.RIGHT)
            self.color=self.colorGet(self.status)
            self.statusLight=tk.Label(self.controlFrame, text=u"\uD83D\uDFD2", font=('',30),fg=self.color)
            self.statusLight.pack(side=tk.RIGHT)
            self.callButton=tk.Button(self.controlFrame, text=u"\uD83D\uDCDE", font=('', 24), takefocus=False,
                                      command=lambda:self.nodeCall(self.IP))
            self.callButton.pack(side=tk.LEFT)
        self.border=tk.Frame(self.nodes, bg='black', height=2, width=480)
        self.border.pack(pady=5)
        self.master.after(30000, lambda:self.getNodeList())

    def callStatus(self):
        f=open("alert.txt","r")
        content=f.read()
        if content=="None" and self.callstatus!=2:
            print("No incoming calls")
            if self.previouscallstatus==1:
                self.callText.set('Call')
                self.call_number.configure(fg='black')
        if bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",content)) and self.callstatus!=2:
            self.previouscallstatus=self.callstatus
            self.callstatus=1
            IP=content
            print("Call from: " + IP)
            self.callText.set('Accept Call')
            self.current_number.set(IP)
            self.call_number.configure(fg='blue')
        if self.callstatus==2:
            print("ongoing call")
        self.master.after(1000, lambda:self.callStatus())
        f.close()

    def nodeCall(self,IP):
        self.n.select(0)
        self.current_number.set(IP)

    def destroy(self, event):
        self.master.destroy()
        
root=tk.Tk()
test=HamPhone(root)
root.mainloop()
