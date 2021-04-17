#!/usr/bin/env python
# coding: utf-8

# In[22]:


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
    from tkFileDialog import *
except ImportError:
    # if user has python3
    from tkinter import *
    import tkinter.font as font
    import tkinter.messagebox as mb
    from tkinter import filedialog
    
from PIL import *
from PIL import ImageTk
import hashlib
from bcrypt import *
import pickle
import os.path
import os
import requests
from itertools import count, cycle 
import math

root = Tk()



class ImageLabel(Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
        
    
def loaddict():
    '''
    Function to load the saved login database from the saved pickle 
    format.
    
    **Parameters**
    
    None

    **Returns**
    
    dictAdmin: *dict*
        Dictionary containing encrypted login info
    
    '''
    with open("admin.txt", "rb") as dictAdmin:
        return pickle.load(dictAdmin)

        
def savedict(dictAdmin):
    '''
    Function to save the login database from in a saved pickle 
    format.
    
    **Parameters**
    
    dictAdmin: *dict*
        Dictionary containing encrypted login info

    **Returns**
    
    None

    
    '''
    
    pickle.dump(dictAdmin, open("admin.txt", "wb"))

        
class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, root)
        self.master.geometry('760x443')
        self.master.resizable(False, False)
        self.master.title('PDB Processing Program')
        self.bg = PhotoImage(file="bg_img.png")
        self.grid()
        self.welcome_setup()
        
    def welcome_setup(self, master=None):
        '''
        Function to set up the initial welcome screen of the GUI. Function will
        create a canvas and set a background image, username entry and password
        entry. It will also create buttons for log in and to create an account.
        
        **Parameters**
        
        self: *object*
        
        **Returns**
        
        None
        '''
        # set up background image
        self.canvas = Canvas(self, width=760, height=443)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw')

        # Import welcome text file with setup text
        with open("text_setup.txt") as f:
            self.lines = f.read()
        f.close()
        
        self.myFont_heading = font.Font(family='Helvetica', size=20)
        self.canvas.create_text(380, 75, text=self.lines, font=self.myFont_heading)

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
        '''
        Function that checks if the hashed username entered on the welcome string 
        matches any of the saved hashed usernames. If usernames match, code will
        use bcrypt.checkpw to compare saved and entered passwords. If either username 
        or password is incorrect, an error message will pop up.
        
        **Parameters**
        
        self: *object*
        
        **Returns**
        
        None.

        '''
        dictAdmin = loaddict()
        hashed_user = hashlib.sha512(self.username.get().encode()).hexdigest()
        
        if any([True for k, v in dictAdmin.items() if k == hashed_user and checkpw(
                self.password.get().encode(), v)]):
            self.second_setup()
        else:
            mb.showerror("Error", "Username or Password is incorrect")
        
    def create_account(self, master=None):
        '''
        Function will first destroy the old window and set up the create an 
        account window.

        Parameters
        ----------
        master : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        '''
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
        self.new_password = StringVar()
        self.password_entry = Entry(self, textvariable = self.new_password,
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
        '''
        Function begins by checking the user's directory to see if the admin
        database exists, if it does then the dictionary is loaded, if it does
        not exist then the dictionary is created. Function will use the bcrypt.checkpw
        function to see if the two passwords match. If they match the window will be 
        destroyed and the user will be prompted to log in on the main screen.
        If they do not match an error message will appear.
        
        Parameters
        ----------
        self: *object*
        
        Returns
        -------
        None.

        '''
        
        
        if os.path.isfile('admin.txt'):
            dictAdmin = loaddict()
        else:
            dictAdmin = {}
        
        #hashing username and password
        hashed_passwd = hashpw(self.new_password.get().encode(), gensalt())
        hashed_user = hashlib.sha512(self.username.get().encode()).hexdigest()
        
        #checks to see if hashed+salted passwords match each other
        #if they match, screen resets to log in screen
        if checkpw(self.password_confirm.get().encode(), hashed_passwd):
            dictAdmin[hashed_user] = hashed_passwd
            savedict(dictAdmin)
            mb.showinfo('Account Created', 'Please log in!')
            self.newWindow.destroy()
            self.welcome_setup()
            
        #if they do not error message pops up
        if not checkpw(self.password_confirm.get().encode('utf8'), hashed_passwd):
            mb.showerror("Error", "Passwords Do Not Match")
    
    def fetch_file(self):
        '''
        Function will search the internet for the desired PDB file by following
        the URL listed. With the file open, it will be downloaded in chunks and
        saved to a pdb file. The file will then be read and if one of the first
        few lines contains the error message then the file will be deleted and
        an error message will appear. If no error message is present then the 
        dropdown function will be called.
        
        Parameters
        -------
        
        self: *object*

        Returns
        -------
        pdb : *file*
            DESCRIPTION the PDB file downloaded.

        '''
        #defines download url
        file_url = "https://files.rcsb.org/download/" + self.tempfile.get() +".pdb"
        
        r = requests.get(file_url, stream = True)
        pdb_file = self.tempfile.get() + ".pdb"
        
        #opens blank file and fills it with downloaded data
        with open(pdb_file, "wb") as self.pdb:
            for chunk in r.iter_content(chunk_size=(1000)):
                if chunk:
                    self.pdb.write(chunk)
        
        #If file does not exist it be removed             
        count=0
        error_msg = "    <title>404 Not Found</title>"           
        with open(pdb_file, "r") as pdbr:
            pdb_readlines = pdbr.readlines()
            for line in pdb_readlines:
                if error_msg in line:
                    count +=1
                    break
                
        if count > 0:
            os.remove(pdb_file)
            mb.showerror("Error", "PDB file does not exist!")
            
        if count == 0:
            self.dropdown()
                
        return self.pdb
    
    def explorer_file(self):
        '''
        Function will open a file explorer so the user can upload a PDB file of
        their choosing. If the file does not end in PDB an error will pop up.
        
        Parameters
        -------
        self: *object*
        
        Returns
        -------
        self.pdb: *file*
            DESCRIPTION the PDB file that was uploaded.

        '''
        
        self.filename = filedialog.askopenfile(mode="r", initialdir="/", 
                                                   filetypes =(("All Files", "*.txt"),("All Files","*.*")), 
                                                   title = "Choose a file.")
        
        self.pdb = self.filename.read().splitlines()
       
         
        if self.pdb[0].startswith("HEADER"):
            self.dropdown()
            return self.pdb
        else:
            mb.showerror("Error", "Not a PDB file!")
                
    
    def second_setup(self):
        '''
        Function to set up second window that asks users to name a PDB file
        or upload their own PDB file.
        
        Parameters
        -------
        self: *object*

        Returns
        -------
        None.

        '''
        #destroy old window
        self.canvas.destroy()
        
        # set up new window to create an account
        self.secondWindow = Canvas(self, width=760, height=443)
        self.secondWindow.pack()
        self.secondWindow.create_image(0, 0, image=self.bg, anchor='nw')
       
        # Write image citation
        self.secondWindow.create_text(
            650, 420, text="Image from img.theweek.in", font=self.myFont_citation)
        
        # write heading for new screen
        self.secondWindow.create_text(380, 35,
                                    text="Welcome!",
                                    font=self.myFont_heading)
        
        #set up entry to fetch PDB file from internet
        self.secondWindow.create_text(380, 100,
                                    text="Please Enter PDB File Name!",
                                    font=self.myFont_heading)
        self.tempfile = StringVar()
        self.tempfile_entry = Entry(self, textvariable = self.tempfile,
                                    width=10)
        tempfile_entry = self.secondWindow.create_window(350, 140,
                                                       anchor='nw',
                                                       window=self.tempfile_entry)
        #button to confirm entry
        self.fetch = Button(self,
                                text="Fetch", width = 10,
                                command=self.fetch_file)
        self.fetch_c = self.secondWindow.create_window(343, 170,
                                                            anchor="nw",
                                                            window=self.fetch)
        #set up button to open file explorer
        self.secondWindow.create_text(380, 230,
                                    text="Or Upload File",
                                    font=self.myFont_heading)
        
        self.browse = Button(self,
                                text="Browse Files", width = 15,
                                command=self.explorer_file)
        self.browse_c = self.secondWindow.create_window(330, 260,
                                                            anchor="nw",
                                                            window=self.browse)
    #################################
    ##NEED TO FIGURE OUT HOW TO PUT
    ##ALL MATH IN NEW CLASS
    ###################################
    
    def get_coordinates(self, line):
        x = float(line[31:38]) #gets xyz coordinates
        y = float(line[39:46])
        z = float(line[47:54])
        return [x, y, z]
    
    def calc_atom_dist(self, atom1_xyz, atom2_xyz):
        atom1_x, atom1_y, atom1_z = atom1_xyz #calculates distance
        atom2_x, atom2_y, atom2_z = atom2_xyz

        dist = math.sqrt((atom1_x - atom2_x)**2 + (atom1_y - atom2_y)**2 +
                         (atom1_z - atom2_z)**2)
        return dist

    def h_bond(self, file):
        
        oxygen = []
        h_bonds=[]
        nitrogen = []
        count = 1
        
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:14] == "O":
                oxygen.append(line.strip())
            if line[:4] == "ATOM" and line[13:14] == "N":
                nitrogen.append(line.strip())
        
        h_file = open("H_bond.txt", "a")
        
        for i in range(len(oxygen)):
            o_atoms=self.get_coordinates(oxygen[i])
            for w in range(len(nitrogen)):
                n_atoms=self.get_coordinates(nitrogen[w])
                h_bond_distance=self.calc_atom_dist(o_atoms, n_atoms)
                if h_bond_distance <= 3.2:
                    entry = str("Pair #" + str(count) +'\n' + oxygen[i]+'\n' + nitrogen[w]+'\n')
                    h_file.write(entry)
                    count += 1
        h_file.close()
        '''
        Pick back up and print the list to the screen and add back button
        to do another task
        '''
        
        
    def calculate_task(self):
        
        lbl = ImageLabel(self)
        lbl.place(x=150, y=130)
        photo=lbl.load('calc.gif')
        
        
        if self.clicked.get() == self.options[0]:
            self.h_bond(self.pdb)
            
    def dropdown(self):
        '''
        Function to create the third screen which contains the dropdown menu.
        
        Parameters
        -------
        self: *object*
        
        Returns
        -------
        None.

        '''
        #destory old window
        self.secondWindow.destroy()
        
        #set up new window with drop down menu
        self.thirdWindow = Canvas(self, width=760, height=443)
        self.thirdWindow.pack()
        self.thirdWindow.create_image(0, 0, image=self.bg, anchor='nw')
       
        # Write image citation
        self.thirdWindow.create_text(
            650, 420, text="Image from img.theweek.in", font=self.myFont_citation)
        
        #write heading
        self.thirdWindow.create_text(380, 35,
                                    text="Choose task below",
                                    font=self.myFont_heading)
        
        self.options = ["Hydrogen Bond Partners", 
                   "Radius of Gyration",
                   "van der Waals Interactions",
                   "Number and Type of Secondary Structures"
                   ]
        
        self.clicked = StringVar()
        self.clicked.set("Choose Below") 
        self.drop = OptionMenu(self, self.clicked, *self.options)
        
        dropdown_menu = self.thirdWindow.create_window(330, 60,
                                                       anchor="nw",
                                                       window = self.drop
                                                       )
        self.calculate = Button(self,
                                text="Calculate", width = 10,
                                command = self.calculate_task)
        
        self.calculate_c = self.thirdWindow.create_window(350, 100,
                                                            anchor="nw",
                                                            window=self.calculate)


if __name__ == "__main__":
    app = Application(master=root)
    app.mainloop()




















































