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
import time
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt


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
                
        self.pdb = open(pdb_file, "r")
        self.pdb = self.pdb.readlines()
        
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
        
        self.h_file = open("H_bond.txt", "w")
        
        for i in range(len(oxygen)):
            o_atoms=self.get_coordinates(oxygen[i])
            for w in range(len(nitrogen)):
                n_atoms=self.get_coordinates(nitrogen[w])
                h_bond_distance=self.calc_atom_dist(o_atoms, n_atoms)
                if h_bond_distance <= 3.2:
                    entry = str("Pair #" + str(count) +'\n' + oxygen[i]+'\n' + nitrogen[w]+'\n')
                    self.h_file.write(entry)
                    count += 1
        self.h_file.close()
               
    def radius(self, file):
        
        x_coordinates=[]
        y_coordinates=[]
        z_coordinates=[]
        raw_atoms = []
        atom_distance = []
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:15] == "CA":
                x_coordinates.append(float(line[31:38]))
                y_coordinates.append(float(line[39:46]))
                z_coordinates.append(float(line[47:54]))
                raw_atoms.append(line.strip())
                
        self.center_of_mass = (mean(x_coordinates), mean(y_coordinates)
                          , mean(z_coordinates))
       
        for i in range(len(raw_atoms)):
            atom1_xyz = self.get_coordinates(raw_atoms[i])
            atom2_xyz = self.center_of_mass
            atom_dist = self.calc_atom_dist(atom1_xyz, atom2_xyz)
            if atom_dist > 0:
                atom_distance.append(atom_dist)
        self.radius_gyration = sum(atom_distance)/ len(raw_atoms)
        
        self.output_text = str("Center of Mass = " + str(self.center_of_mass
                                                         )+ '\n' + "Radius of Gyration = " + str(
                                                             str(self.radius_gyration) + "Å" ))
    def hydropathy(self, file):
            
            
        fasta = []
        aminoacid={}
        aminoacid["ALA"]="A"
        aminoacid["CYS"]="C"
        aminoacid["ASP"]="D"
        aminoacid["GLU"]="E"
        aminoacid["PHE"]="F"
        aminoacid["GLY"]="G"
        aminoacid["HIS"]="H"
        aminoacid["ILE"]="I"
        aminoacid["LYS"]="K"
        aminoacid["LEU"]="L"
        aminoacid["MET"]="M"
        aminoacid["MSE"]="M"
        aminoacid["ASN"]="N"
        aminoacid["PRO"]="P"
        aminoacid["GLN"]="Q"
        aminoacid["ARG"]="R"
        aminoacid["SER"]="S"
        aminoacid["THR"]="T"
        aminoacid["VAL"]="V"
        aminoacid["TRP"]="W"
        aminoacid["UNK"]="X"
        aminoacid["TYR"]="Y"
        
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:15]=="CA":
                if line[17:20] in aminoacid:
                    fasta.append(aminoacid[line[17:20]].strip())
        octanol = []           
        octscale={}
        octscale["A"]="0.5"
        octscale["R"]="1.81"
        octscale["N"]="0.85"
        octscale["D"]="3.64"
        octscale["C"]="-0.02"
        octscale["Q"]="0.77"
        octscale["E"]="3.63"
        octscale["G"]="1.15"
        octscale["H"]="2.33"
        octscale["I"]="-1.12"
        octscale["L"]="-1.25"
        octscale["M"]="-0.67"
        octscale["F"]="-1.71"
        octscale["P"]="0.14"
        octscale["S"]="0.46" 
        octscale["T"]="0.25" 
        octscale["W"]="-2.09"
        octscale["Y"]="-0.71"
        octscale["V"]="-0.46"       
        
        interface= []       
        intscale={}
        intscale["A"]="0.17"
        intscale["R"]="0.81"
        intscale["N"]="0.42"
        intscale["D"]="1.23"
        intscale["C"]="-0.24"
        intscale["Q"]="0.58"
        intscale["E"]="2.02"
        intscale["G"]="0.01"
        intscale["H"]="0.96"
        intscale["I"]="-0.31"
        intscale["L"]="-0.56"
        intscale["M"]="-0.23"
        intscale["F"]="-1.13"
        intscale["P"]="0.45"
        intscale["S"]="0.13" 
        intscale["T"]="0.14" 
        intscale["W"]="-1.85"
        intscale["Y"]="-0.94"
        intscale["V"]="-0.07"
        
        for letter in fasta:
            if letter in octscale and intscale:
                octanol.append(float(octscale[letter].strip()))
                interface.append(float(intscale[letter].strip()))
        
        average_octanol = []
        average_int = []
        for i in range(9, len(octanol)-10):
            average_octscale = mean(octanol[i-9:i+9])
            average_octanol.append(average_octscale)
            
        for i in range(9, len(interface)-10):
            average_intscale = mean(interface[i-9:i+9])
            average_int.append(average_intscale)
        
        
        average_octanol_np = np.array(average_octanol)
        average_interface_np = np.array(average_int)
        average_scale = average_octanol_np - average_interface_np
        xaxis = np.arange(10, len(average_interface_np)+10)
        plt.figure(figsize=(8,6))
        plt.plot(xaxis, average_octanol_np, 'r-', label="Octanol Scale")
        plt.plot(xaxis, average_interface_np, 'b:', label="Interface Scale")
        plt.plot(xaxis, average_scale, 'g--', label="Octanol-Interface Scale")
        plt.ylabel("Total free energy (kcal/mol)", fontsize=16)
        plt.xlabel("Residue Number in 19 AA Window", fontsize=16)
        plt.legend()
        plt.savefig("Hydrophobicity_Scale.png")
        plt.close()
        self.fig = PhotoImage(file="Hydrophobicity_Scale.png")
    
    def ss(self, file):
        self.sf = open("secondary_structure.txt","a")
        
        ss=[]
        
        for line in self.pdb:
            if line[:5] == "HELIX":
                ss.append(line)
            if line[:5] == "SHEET":
                ss.append(line)
        
        helix = 1
        sheet = 1
        for entry in ss:
            if entry.startswith('HELIX'):
                self.sf.write(str(entry) + '\n')          
                helix +=1
            if entry.startswith('SHEET'):
                self.sf.write(str(entry) + '\n')
                sheet +=1
                
        self.out_entry = str("There are " + str(helix) + " alpha helices and "+
                             str(sheet)+ " beta sheets! \nFull file saved as secondary_structure.txt")
        self.sf.close()
        
    def calculate_task(self):
        
        
        if self.clicked.get() == self.options[0]:
            self.h_bond(self.pdb)  
            mb.showinfo("Success!", "File saved in directory as H_bond.txt")
            
        if self.clicked.get() == self.options[1]:
            self.radius(self.pdb)
            mb.showinfo("Success!", self.output_text)
        
        if self.clicked.get() == self.options[2]:
            self.hydropathy(self.pdb)
            mb.showinfo("Success!", "Graph saved in directory as Hydrophobicity Scale.png")
            self.tl = Toplevel()
            self.tl.geometry('576x432')
            self.tl.title("Hydrophobicity Scale")
            self.hc = Canvas( self.tl, width=576, height=432)
            self.hc.pack()
            self.hc.create_image(0, 0, image = self.fig,
                                          anchor="nw")
            
        if self.clicked.get() == self.options[3]:
            self.ss(self.pdb)
            mb.showinfo("Success!", self.out_entry)
        
        
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
                   "Hydrophobicity of Protein",
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
        
        
        lbl = ImageLabel(self)
        lbl.place(x=150, y=130)
        photo=lbl.load('calc.gif')
        
            
if __name__ == "__main__":
    app = Application(master=root)
    app.mainloop()




















































