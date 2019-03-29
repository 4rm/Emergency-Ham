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
        #master.overrideredirect(1) #Hides titlebar, use with Pi
        master.geometry("480x800")
        

        self.n=ttk.Notebook(master)
        self.n.pack()

        self.f1=ttk.Frame(self.n)
        self.f2=ttk.Frame(self.n)
        
        self.n.add(self.f1, text='Phone')
        self.n.add(self.f2, text='Nodes')

        self.numFrame=tk.Frame(self.f1)
        self.numFrame.grid(row=0, column=0)
            
        self.current_number=tk.StringVar()
        self.current_number.set('')
        self.call_number=tk.Label(self.numFrame, textvariable=self.current_number, width=20, bg='white',
                                  relief='sunken', height=2, font = ('' , 26))
        self.call_number.grid(row=0, column=0)
        
        self.numpad=tk.Frame(self.f1)
        self.numpad.grid(row=1, column=0)

        self.Buttons=['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0']

        button_ipadding_x = 44
        button_ipadding_y = 19
        
        for i,n in enumerate(self.Buttons):
            self.num=tk.Button(self.numpad, text=n, command=lambda n=n:self.IPget(str(n)), relief=tk.GROOVE,
                               width=1, font = ('' , 45))
            self.num.grid(row=1+math.floor(i/3), column=i%3, ipadx=button_ipadding_x, ipady=button_ipadding_y)

        self.delete=tk.Button(self.numpad, text='⌫', width=1, relief=tk.GROOVE,
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
        self.randlist()

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
            self.master.after(1000, lambda:self.current_number.set(''))
        else:
            self.error()
        

    def hangup(self):
        print('Hanging up...')
        self.callText.set('Call')
        self.call_button.configure(command=lambda:self.call(), bg='#90EE90', activebackground="sea green")
        
    def randlist(self):
        self.nodes.destroy()
        self.nodes=tk.Frame(self.f2)
        self.nodes.pack()
        listlength=random.randrange(20)
        mylist=[]
        for i in range(listlength+1):
            self.entry=tk.StringVar()
            self.entry.set(random.random())
            mylist.append(self.entry)
        for i in range(len(mylist)):
            self.node=tk.Label(self.nodes, textvariable=mylist[i])
            self.node.pack()
        self.master.after(1000, lambda:self.randlist())

    def error(self):
        self.call_number.configure(fg='red')
        self.master.after(125, lambda:self.call_number.configure(fg='black'))

root=tk.Tk()
test=HamPhone(root)
root.mainloop()
