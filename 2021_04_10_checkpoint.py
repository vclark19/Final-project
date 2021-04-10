#!/usr/bin/env python
# coding: utf-8

# In[20]:


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
    import Tkinter.font as font
except ImportError:
    # if user has python3
    from tkinter import *
    import tkinter.font as font
from PIL import *
import hashlib
from bcrypt import *


root = Tk()


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, root)
        self.master.geometry('760x443')
        self.master.resizable(False, False)
        self.master.title('PDB Processing Program')
        self.bg = PhotoImage(file="bg_img.png")
        self.grid()
        self.admin = {}
        self.welcome_setup()

    def welcome_setup(self, master=None):

        # set up background image
        self.canvas = Canvas(self, width=760, height=443)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw')

        # Import welcome text file with setup text
        with open("text_setup.txt") as f:
            lines = f.read()
        f.close()

        self.myFont_heading = font.Font(family='Helvetica', size=20)
        self.canvas.create_text(380, 75, text=lines, font=self.myFont_heading)

        # Write image citation
        self.myFont_citation = font.Font(family='Helvetica', size=7)
        self.canvas.create_text(
            650, 420, text="Image from img.theweek.in", font=self.myFont_citation)

        # Write username and password entry
        self.myFont = font.Font(family='Helvetica', size=15)
        self.canvas.create_text(380, 140, text="Username",
                                font=self.myFont)
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username,
                                    width=30)
        username_entry = self.canvas.create_window(290, 170,
                                                   anchor='nw',
                                                   window=self.username_entry)

        self.canvas.create_text(380, 210, text="Password",
                                font=self.myFont)
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable = self.password,
                                    show = "*", width=30)
        password_entry = self.canvas.create_window(290, 240,
                                                   anchor='nw',
                                                   window=self.password_entry)
        
        # create buttons for log in and create account
        self.enter_button = Button(self, text="Log in",
                                  command=self.login_check)
        self.enter_button_canvas = self.canvas.create_window(410, 280,
                                                             anchor="nw",
                                                             window=self.enter_button)

        self.account_button = Button(self,
                                     text="Create account",
                                     command=self.create_account)
        self.account_button_canvas = self.canvas.create_window(310, 280,
                                                               anchor="nw",
                                                               window=self.account_button)
    def login_check(self):
        username = self.username.get()
        password = self.password.get()
        
        hashed = hashpw(password.encode('utf8'), gensalt())
        print(hashed)
        
        #self.canvas.create_text(430, 400, text=(hashed), font=self.myFont)
        
    def create_account(self, master=None):
        
        #destroy old window
        self.canvas.destroy()
        
        # set up new window to create an account
        self.newWindow = Canvas(self, width=760, height=443)
        self.newWindow.pack()
        self.newWindow.create_image(0, 0, image=self.bg, anchor='nw')
        # Write image citation
        
        self.newWindow.create_text(
            650, 420, text="Image from img.theweek.in", font=self.myFont_citation)
        # write heading for new screen
        self.newWindow.create_text(380, 35,
                                    text="Create username!",
                                    font=self.myFont_heading)
        
        #set up username entry
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username,
                                    width=30)
        username_entry = self.newWindow.create_window(290, 80,
                                                       anchor='nw',
                                                       window=self.username_entry)
        
        #set up password entry
        self.newWindow.create_text(380, 145, text="Create password!",
                                font=self.myFont_heading)
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable = self.password,
                                    show = "*", width=30)
        password_entry = self.newWindow.create_window(290, 180,
                                                       anchor='nw',
                                                       window=self.password_entry)
        
        self.newWindow.create_text(380, 250, text="Confirm password!",
                                font=self.myFont_heading)
        self.password_confirm = StringVar()
        self.password_entry = Entry(self, textvariable = self.password_confirm,
                                    show = "*", width=30)
        password_entry = self.newWindow.create_window(290, 290,
                                                       anchor='nw',
                                                       window=self.password_entry)
        #button to confirm entry
        self.confirm = Button(self,
                                text="Enter", width = 15,
                                command=self.check_account)
        self.confirm_c = self.newWindow.create_window(323, 330,
                                                            anchor="nw",
                                                            window=self.confirm)
    def check_account(self):
        hashed_passwd = hashpw(self.password_entry.get().encode('utf8'), gensalt())
        hashed_user = hashlib.sha512(self.username.get().encode()).hexdigest()
        if checkpw(self.password_confirm.get().encode('utf8'), hashed_passwd):
            self.admin[hashed_user] = hashed_passwd
    '''
       Add in message for if passwords dont match
       '''
#             e=Toplevel()
#             e.geometry("180x100")
#             e.title("Error")
#             el = Label(e, text = "Error! Passwords Do Not Match!", font=self.myFont)
        
        
        
if __name__ == "__main__":
    app = Application(master=root)
    app.mainloop()


# In[ ]:


https://img.theweek.in/content/dam/week/news/sci-tech/2019/May/science-research-study-biology-lab-chemistry-scientific-shut.jpg

