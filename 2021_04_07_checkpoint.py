#!/usr/bin/env python
# coding: utf-8

# In[60]:


'''
Goal of this project is to make a GUI for a protein application
The application will first ask the user to sign in or make an account
Next it will ask them to enter a PDB label and the code will
fetch the file from the internet and then ask the user to choose
from a drop down menu of different tasks to accomplish with the code.

These tasks will be finding hydrogen bond distance, van der waal distance,
molecular weight of the protein, radius of gyration, center of mass of protein.
'''

try:
    # if user has python2
    from Tkinter import *
except ImportError:
    # if user has python3
    from tkinter import *


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.geometry('500x500')
        self.master.title('PDB Processing Program')
        self.grid()
        self.welcome_setup()
    
    def welcome_setup(self):
        self.banner = Label(self, text = "Welcome to the PDB Processing Program \n\nPlease enter username and password", font=20)
        self.banner.pack(padx = 100, pady = 0)
        
        self.username_label = Label(self, text = "Username", font=10)
        self.username_label.pack(padx = 100, pady=15)
        self.username_entry = Entry(self, width = 30)
        self.username_entry.pack(padx = 100, pady = 16)
        
        self.password_label = Label(self, text = "Password", font=10)
        self.password_label.pack(padx = 100, pady=20)
        self.password_entry = Entry(self, width = 30)
        self.password_entry.pack(padx = 100, pady = 21)
        
'''
Going to pick up from stickying the labels to places in the GUI and adding buttons for usernma
and password'''
        
        
root = Tk()
app = Application(master = root)
app.mainloop()
print(grid())


# In[ ]:


https://medium.com/swlh/build-a-gui-on-python-using-tkinter-from-scratch-step-by-step-for-beginners-69466223bcdf

