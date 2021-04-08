#!/usr/bin/env python
# coding: utf-8

# In[17]:


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
root = Tk()


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, root)
        self.master.geometry('760x443')
        self.master.title('PDB Processing Program')
        self.grid()
        self.welcome_setup()
        

    def welcome_setup(self, master = None):
        
        #set up background image
        self.canvas = Canvas(self, width=760, height = 443)
        self.canvas.pack()
        self.bg= PhotoImage(file="bg_img.png")
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw')
        
        # Import welcome text file with setup text
        with open("text_setup.txt") as f:
            lines = f.read()
        f.close()
        
        myFont = font.Font(family='Helvetica', size=20)
        self.canvas.create_text(380, 75, text=lines, font=myFont)
        
        #Write username and password entry
        self.canvas.create_text(380, 200, text="Username", font=myFont)
        self.username_entry = Entry(self, width=30)
        username_entry = self.canvas.create_window(290, 230,
                                                   anchor='nw',
                                                   window = self.username_entry)
        
        self.canvas.create_text(380, 290, text="Password", font=myFont)
        self.password_entry = Entry(self, width=30)
        password_entry = self.canvas.create_window(290, 320,
                                                    anchor='nw',
                                                    window = self.password_entry)
        
        

if __name__ == "__main__":
    app = Application(master=root)
    app.mainloop()


# In[ ]:


https://img.theweek.in/content/dam/week/news/sci-tech/2019/May/science-research-study-biology-lab-chemistry-scientific-shut.jpg

