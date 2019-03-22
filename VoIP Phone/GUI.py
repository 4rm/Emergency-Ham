import voipPhone
import tkinter as tk
import math
from tkinter import ttk

class HamPhone:
    def __init__(self, master):
        self.master=master
        master.title('HamPhone')
        voipPhone.initialize()
        #Creates frame for displaying the currently entered number
        numFrame=tk.Frame(master)
        numFrame.grid(row=0, column=0)
            
        self.current_number=tk.StringVar()
        self.current_number.set('')
        self.call_number=tk.Label(numFrame, textvariable=self.current_number, width=15)
        self.call_number.grid(row=0, column=0)
        
        #Creates frame for the numpad + dot
        numpad=tk.Frame(master)
        numpad.grid(row=1, column=0)
        
        for i in range(10):
            self.num=tk.Button(numpad, text=i, command=lambda i=i:self.IPget(str(i)))
            self.num.grid(row=1+math.floor(i/3), column=i%3)
            
        self.dot=tk.Button(numpad, text='.', command=lambda:self.IPget('.'))
        self.dot.grid(row=4, column=1)
        
        #Creates frame for the non-numpad buttons
        command_Buttons=tk.Frame(master)
        command_Buttons.grid(row=2, column=0)
        self.call_button=tk.Button(command_Buttons, text='call', command=lambda:voipPhone.call(self.current_number.get()))
        self.call_button.grid(row=0, column=1)

        self.delete=tk.Button(command_Buttons, text='←', command=lambda:self.current_number.set(self.current_number.get()[:-1]))
        self.delete.grid(row=0, column=0)
        
    def IPget(self, string):
        self.current_number.set(self.current_number.get()+string)

    #def call(self):
        #print('linphonecsh dial sip:linphone@' + self.current_number.get())
        #self.current_number.set('')

root=tk.Tk()
test=HamPhone(root)
root.mainloop()
