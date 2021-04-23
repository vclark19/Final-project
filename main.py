#!/usr/bin/env python
# coding: utf-8

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
    """
    a label that displays images, and plays them if they are gifs.
    Function was taken from https://stackoverflow.com/a/43770948
    """

    def load(self, im):
        '''
        Will load image for gif
        
        Parameters
        ----------
        
        im: *file*
            Image to animate
        
        Returns
        ------
        
        None
        '''
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
        '''
        Function to configure the image.

        Returns
        -------
        None.

        '''
        self.config(image="")
        self.frames = None

    def next_frame(self):
        '''
        Function to loop through different frames in the image.

        Returns
        -------
        None.

        '''
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
    '''
    Class that contains the functions and set up for the various windows within
    the GUI.
    '''

    def __init__(self, master=None):
        '''
        Function to initialize a series of variables, including
        the size of the window, title, background image, and the welcome
        screen.

        Parameters
        ----------

        master: *operator*
            Master signifies if window will be root or tk()

        Returns
        -------

        None
        '''

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
        self.canvas.create_text(380, 75, text=self.lines,
                                font=self.myFont_heading)

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
        self.password_entry = Entry(self, textvariable=self.password,
                                    show="*", width=30)
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
        # Load in saved dictionary
        dictAdmin = loaddict()

        # Hash the username using sha512 encoding
        hashed_user = hashlib.sha512(self.username.get().encode()).hexdigest()

        # checks if the username entered matches the saved username, and then will
        # check to see if the stored salted password matches the entered password
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
        # destroy old window
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

        # set up username entry
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username,
                                    width=30)
        username_entry = self.newWindow.create_window(290, 80,
                                                      anchor='nw',
                                                      window=self.username_entry)

        # set up password entry
        self.newWindow.create_text(380, 145, text="Create password!",
                                   font=self.myFont_heading)
        self.new_password = StringVar()
        self.password_entry = Entry(self, textvariable=self.new_password,
                                    show="*", width=30)
        password_entry = self.newWindow.create_window(290, 180,
                                                      anchor='nw',
                                                      window=self.password_entry)

        self.newWindow.create_text(380, 250, text="Confirm password!",
                                   font=self.myFont_heading)
        self.password_confirm = StringVar()
        self.password_entry = Entry(self, textvariable=self.password_confirm,
                                    show="*", width=30)
        password_entry = self.newWindow.create_window(290, 290,
                                                      anchor='nw',
                                                      window=self.password_entry)
        # button to confirm entry
        self.confirm = Button(self,
                              text="Enter", width=15,
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

        # hashing username and password
        hashed_passwd = hashpw(self.new_password.get().encode(), gensalt())
        hashed_user = hashlib.sha512(self.username.get().encode()).hexdigest()

        # checks to see if hashed+salted passwords match each other
        # if they match, screen resets to log in screen
        if checkpw(self.password_confirm.get().encode(), hashed_passwd):
            dictAdmin[hashed_user] = hashed_passwd
            savedict(dictAdmin)
            mb.showinfo('Account Created', 'Please log in!')
            self.newWindow.destroy()
            self.welcome_setup()

        # if they do not error message pops up
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
        # defines download url
        file_url = "https://files.rcsb.org/download/" + self.tempfile.get() + ".pdb"

        self.pdb_label = self.tempfile.get()

        r = requests.get(file_url, stream=True)
        pdb_file = self.tempfile.get() + ".pdb"

        # opens blank file and fills it with downloaded data
        with open(pdb_file, "wb") as self.pdb:
            for chunk in r.iter_content(chunk_size=(1000)):
                if chunk:
                    self.pdb.write(chunk)

        # If file does not exist it be removed
        count = 0
        error_msg = "    <title>404 Not Found</title>"
        with open(pdb_file, "r") as pdbr:
            pdb_readlines = pdbr.readlines()
            for line in pdb_readlines:
                if error_msg in line:
                    count += 1
                    break

        if count > 0:
            os.remove(pdb_file)
            mb.showerror("Error", "PDB file does not exist!")

        if count == 0:
            self.dropdown()

        # opens file and reads lines for future data handling
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

        # opens a file explorer for the user
        self.filename = filedialog.askopenfile(mode="r", initialdir="/",
                                               filetypes=(
                                                   ("All Files", "*.txt"), ("All Files", "*.*")),
                                               title="Choose a file.")

        # reads lines of the chosen file from the file explorer
        self.pdb = self.filename.read().splitlines()

       # if the file starts with the HEADER phrase then the next screen will come up
        if self.pdb[0].startswith("HEADER"):
            self.pdb_label = self.pdb[0][62:66]
            self.dropdown()
            return self.pdb
        # If it does not have the HEADER then an error is prompted
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
        # destroy old window
        try:
            self.thirdWindow.destroy()
        except AttributeError:
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

        # set up entry to fetch PDB file from internet
        self.secondWindow.create_text(380, 100,
                                      text="Please Enter PDB File Name!",
                                      font=self.myFont_heading)
        self.tempfile = StringVar()
        self.tempfile_entry = Entry(self, textvariable=self.tempfile,
                                    width=10)
        tempfile_entry = self.secondWindow.create_window(350, 140,
                                                         anchor='nw',
                                                         window=self.tempfile_entry)
        # button to confirm entry
        self.fetch = Button(self,
                            text="Fetch", width=10,
                            command=self.fetch_file)
        self.fetch_c = self.secondWindow.create_window(343, 170,
                                                       anchor="nw",
                                                       window=self.fetch)
        # set up button to open file explorer
        self.secondWindow.create_text(380, 230,
                                      text="Or Upload File",
                                      font=self.myFont_heading)

        self.browse = Button(self,
                             text="Browse Files", width=15,
                             command=self.explorer_file)
        self.browse_c = self.secondWindow.create_window(330, 260,
                                                        anchor="nw",
                                                        window=self.browse)

    def get_coordinates(self, line):
        '''
        Function to take in a line from the PDB file and return the xyz coordinates
        in float form.

        Parameters
        ----------
        line : *str*
            String of chracaters from the PDB file.

        Returns
        -------
        [x, y, z]: *list*
            List of xyz coordinates for a atom.

        '''
        x = float(line[31:38])
        y = float(line[39:46])
        z = float(line[47:54])
        return [x, y, z]

    def calc_atom_dist(self, atom1_xyz, atom2_xyz):
        '''
        Function to calculate the distance between two atoms based on their xyz coordinates.


        Parameters
        ----------
        atom1_xyz : *list, float*
            A series of numbers pertaining to the xyz coordinates of an atom.
        atom2_xyz : *list, float*
            A series of numbers pertaining to the xyz coordinates of an atom..

        Returns
        -------
        dist : *float*
            The distance between two atoms in angstroms.

        '''
        atom1_x, atom1_y, atom1_z = atom1_xyz
        atom2_x, atom2_y, atom2_z = atom2_xyz

        dist = math.sqrt((atom1_x - atom2_x)**2 + (atom1_y - atom2_y)**2 +
                         (atom1_z - atom2_z)**2)
        return dist

    def h_bond(self, file):
        '''
        Function to calculate the hydrogen bond partners in a given PDB file.
        Function will parse out all atoms ending in either O (oxygen) or N (nitrogen).
        File will then open calculate the distance between every oxygen atom and nitrogen
        atom and if the distance is less than or equal to 3.2 angstroms then the atoms
        will be declared hydrogen bond partners and written to a text file.

        Parameters
        ----------
        file: *txt file*
            The pdb file that was obtained by fetching the internet or through the 
            file explorer in readlines() mode.

        Returns
        -------
        None
        '''
        # creates empty lists for all oxygen, nitrogen, and final hydrogen bonded atoms
        oxygen = []
        h_bonds = []
        nitrogen = []
        count = 1

        # parses out the oxygen and nitrogen atoms in the pdb file
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:14] == "O":
                oxygen.append(line.strip())
            if line[:4] == "ATOM" and line[13:14] == "N":
                nitrogen.append(line.strip())

        # opens output text file
        self.h_label = "H_bond_" + self.pdb_label + ".txt"
        self.h_file = open(self.h_label, "w")

        # gets coordinates for every oxygen and nitrogen atom in the lists
        # if the distance is less than or equl to 3.2 the wo atoms are added to the out
        # put text file and the counter is updated
        for i in range(len(oxygen)):
            o_atoms = self.get_coordinates(oxygen[i])
            for w in range(len(nitrogen)):
                n_atoms = self.get_coordinates(nitrogen[w])
                h_bond_distance = self.calc_atom_dist(o_atoms, n_atoms)
                if h_bond_distance <= 3.2:
                    entry = str("Pair #" + str(count) + '\n' +
                                oxygen[i]+'\n' + nitrogen[w]+'\n')
                    self.h_file.write(entry)
                    count += 1
        self.h_file.close()

    def radius(self, file):
        '''
        Function to generate the center of mass and radius of gyration of a given protein.

        Parameters
        ----------
        file: *txt file*
            The pdb file that was obtained by fetching the internet or through the 
            file explorer in readlines() mode..

        Returns
        -------
        None.

        '''

        # creates empty lists for xyz coordinates, unprocessed atoms and final atom distance
        x_coordinates = []
        y_coordinates = []
        z_coordinates = []
        raw_atoms = []
        atom_distance = []

        # parses out the atoms with carbon alpha atoms to simplify the center of mass calculations
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:15] == "CA":
                x_coordinates.append(float(line[31:38]))
                y_coordinates.append(float(line[39:46]))
                z_coordinates.append(float(line[47:54]))
                raw_atoms.append(line.strip())

        # calculates the center of mass of a protein based on xyz coordinates
        self.center_of_mass = (mean(x_coordinates), mean(
            y_coordinates), mean(z_coordinates))

        # calculates the distance every atom has in relation to the center of mass
        # if the atom is not the center of mass then it is added to an atom distance list
        for i in range(len(raw_atoms)):
            atom1_xyz = self.get_coordinates(raw_atoms[i])
            atom2_xyz = self.center_of_mass
            atom_dist = self.calc_atom_dist(atom1_xyz, atom2_xyz)
            if atom_dist > 0:
                atom_distance.append(atom_dist)

        # radius of gyration calculated based on the total atom distances from the center of
        # mass divided by the amount of atoms in the molecule

        self.radius_gyration = sum(atom_distance) / len(raw_atoms)

        self.output_text = str("Center of Mass = " + str(self.center_of_mass
                                                         ) + '\n' + "Radius of Gyration = " + str(
                                                             str(self.radius_gyration) + "Å"))

    def hydropathy(self, file):
        '''
        Function to calculate the hydrophobicity of a given protein in
        terms of the octanol and interface scale developed by Wimley and White, 1996.
        Function will graph the hydrophobicity in the different scales in a sliding 
        window to show how the hydrophobicity of a region changes.

        Parameters
        ----------
        file: *txt file*
            The pdb file that was obtained by fetching the internet or through the 
            file explorer in readlines() mode.

        Returns
        -------
        None.

        '''
        self.hydro_label = self.pdb_label
        # dictionary for the conversion of amino acids to FASTA format
        fasta = []
        aminoacid = {}
        aminoacid["ALA"] = "A"
        aminoacid["CYS"] = "C"
        aminoacid["ASP"] = "D"
        aminoacid["GLU"] = "E"
        aminoacid["PHE"] = "F"
        aminoacid["GLY"] = "G"
        aminoacid["HIS"] = "H"
        aminoacid["ILE"] = "I"
        aminoacid["LYS"] = "K"
        aminoacid["LEU"] = "L"
        aminoacid["MET"] = "M"
        aminoacid["MSE"] = "M"
        aminoacid["ASN"] = "N"
        aminoacid["PRO"] = "P"
        aminoacid["GLN"] = "Q"
        aminoacid["ARG"] = "R"
        aminoacid["SER"] = "S"
        aminoacid["THR"] = "T"
        aminoacid["VAL"] = "V"
        aminoacid["TRP"] = "W"
        aminoacid["UNK"] = "X"
        aminoacid["TYR"] = "Y"

        # parses out all carbon alpha atoms for simplicity
        # if the residue is in the amino acid list, it will be converted
        # to a fasta format and saved to fasta list
        for line in self.pdb:
            if line[:4] == "ATOM" and line[13:15] == "CA":
                if line[17:20] in aminoacid:
                    fasta.append(aminoacid[line[17:20]].strip())

        # dictionary with the octanol values for every fasta amino acid
        octanol = []
        octscale = {}
        octscale["A"] = "0.5"
        octscale["R"] = "1.81"
        octscale["N"] = "0.85"
        octscale["D"] = "3.64"
        octscale["C"] = "-0.02"
        octscale["Q"] = "0.77"
        octscale["E"] = "3.63"
        octscale["G"] = "1.15"
        octscale["H"] = "2.33"
        octscale["I"] = "-1.12"
        octscale["L"] = "-1.25"
        octscale["M"] = "-0.67"
        octscale["F"] = "-1.71"
        octscale["P"] = "0.14"
        octscale["S"] = "0.46"
        octscale["T"] = "0.25"
        octscale["W"] = "-2.09"
        octscale["Y"] = "-0.71"
        octscale["V"] = "-0.46"

        # dictionary with the interface values for every fasta amino acid
        interface = []
        intscale = {}
        intscale["A"] = "0.17"
        intscale["R"] = "0.81"
        intscale["N"] = "0.42"
        intscale["D"] = "1.23"
        intscale["C"] = "-0.24"
        intscale["Q"] = "0.58"
        intscale["E"] = "2.02"
        intscale["G"] = "0.01"
        intscale["H"] = "0.96"
        intscale["I"] = "-0.31"
        intscale["L"] = "-0.56"
        intscale["M"] = "-0.23"
        intscale["F"] = "-1.13"
        intscale["P"] = "0.45"
        intscale["S"] = "0.13"
        intscale["T"] = "0.14"
        intscale["W"] = "-1.85"
        intscale["Y"] = "-0.94"
        intscale["V"] = "-0.07"

        # iterates thrugh fasta list and if the letter is in the octscale and intscale
        # dictionary then the values are recorded in the appropriate list
        for letter in fasta:
            if letter in octscale and intscale:
                octanol.append(float(octscale[letter].strip()))
                interface.append(float(intscale[letter].strip()))

        average_octanol = []
        average_int = []
        # calculates the average octanol value for a 19 window of residues
        for i in range(9, len(octanol)-10):
            average_octscale = mean(octanol[i-9:i+9])
            average_octanol.append(average_octscale)

        # calculates the average interface value for a 19 window of residues
        for i in range(9, len(interface)-10):
            average_intscale = mean(interface[i-9:i+9])
            average_int.append(average_intscale)

        # creates numpy arrays for the average octanol and interface lists
        # graphs the scale and saves it to the working directory
        average_octanol_np = np.array(average_octanol)
        average_interface_np = np.array(average_int)
        average_scale = average_octanol_np - average_interface_np
        xaxis = np.arange(10, len(average_interface_np)+10)
        plt.figure(figsize=(8, 6))
        plt.plot(xaxis, average_octanol_np, 'r-', label="Octanol Scale")
        plt.plot(xaxis, average_interface_np, 'b:', label="Interface Scale")
        plt.plot(xaxis, average_scale, 'g--', label="Octanol-Interface Scale")
        plt.ylabel("Total free energy (kcal/mol)", fontsize=16)
        plt.xlabel("Residue Number in 19 AA Window", fontsize=16)
        plt.title("Hydrophobicity Scale of " + self.hydro_label)
        plt.legend()
        plt.savefig("Hydrophobicity_Scale_" + self.hydro_label + ".png")
        plt.close()
        self.fig = PhotoImage(
            file="Hydrophobicity_Scale_" + self.hydro_label + ".png")

    def ss(self, file):
        '''
        Will take in a pdb file and parse the data set to return a list of secondary
        structures in the protein.

        Parameters
        ----------
        file: *txt file*
            The pdb file that was obtained by fetching the internet or through the 
            file explorer in readlines() mode.

        Returns
        -------
        None.

        '''
        self.sf_label = "secondary_structure_" + self.pdb_label + ".txt"

        self.sf = open(self.sf_label, "a")

        ss = []

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
                helix += 1
            if entry.startswith('SHEET'):
                self.sf.write(str(entry) + '\n')
                sheet += 1

        self.out_entry = str("There are " + str(helix) + " alpha helices and " +
                             str(sheet) + " beta sheets! \nFull file saved as " + self.sf_label)
        self.sf.close()

    def close(self, file):

        pdb_line = [i for i in self.pdb if i[:4] == "ATOM"]

        self.cc_label = "Close_contacts_" + self.pdb_label + ".txt"

        self.close_contacts = open(self.cc_label, "w")
        count = 0
        # Ignoring molecules on the same residue
        for i in range(len(pdb_line)):
            for j in range(i+1, len(pdb_line)):
                if pdb_line[i][17:26] != pdb_line[j][17:26]:
                    atom1_xyz = self.get_coordinates(pdb_line[i])
                    atom2_xyz = self.get_coordinates(pdb_line[j])
                    atom_dist = self.calc_atom_dist(atom1_xyz, atom2_xyz)
                    if atom_dist <= 2.7:
                        entry = str("Pair #" + str(count) + '\n' +
                                    pdb_line[i]+'\n' + pdb_line[j]+'\n')
                        self.close_contacts.write(entry)
                        count += 1
        self.out_msg = str("There are " + str(count) + " van der Waals contacts!" +
                           '\nFull details saved as ' + self.cc_label)

        self.close_contacts.close()

    def disulfide(self, file):

        pdb_line = [i for i in self.pdb if i[:4] ==
                    "ATOM" and i[17:20] == "CYS" and i[13:15] == "SG"]

        self.ds_label = "Disulfide_bonds_" + self.pdb_label + ".txt"

        disulfide_txt = open(self.ds_label, "w")

        count = 0

        for i in range(len(pdb_line)):
            for j in range(i+1, len(pdb_line)):
                if pdb_line[i][17:26] != pdb_line[j][17:26]:
                    atom1_xyz = self.get_coordinates(pdb_line[i])
                    atom2_xyz = self.get_coordinates(pdb_line[j])
                    atom_dist = self.calc_atom_dist(atom1_xyz, atom2_xyz)
                    if atom_dist <= 5:
                        entry = str("Pair #" + str(count) + '\n' +
                                    pdb_line[i]+'\n' + pdb_line[j]+'\n')
                        disulfide_txt.write(entry)
                        count += 1
        if count == 0:
            if os.path.isfile(self.ds_label):
                disulfide_txt.close()
                os.remove(self.ds_label)
                self.out_msg = str(
                    "There are no disulfide bonds in this protein!")
                mb.showerror("Error", self.out_msg)

        if count >= 1:
            self.out_msg = str("There are " + str(count) + " disulfide bonds!" +
                               '\nFull details saved as ' + self.ds_label)
            mb.showinfo("Success!", self.out_msg)
            disulfide_txt.close()

    def calculate_task(self):
        '''
        Function that will perform a new function based on what option
        was clicked from the dropdown menu.

        Returns
        -------
        None.

        '''

        # hydrogen bond function
        # will output success message after it is completed
        if self.clicked.get() == self.options[0]:
            self.h_bond(self.pdb)
            mb.showinfo(
                "Success!", "File saved in directory as " + self.h_label)

        # radius of gyration function
        # will output summary of calculations after it is completed
        if self.clicked.get() == self.options[1]:
            self.radius(self.pdb)
            mb.showinfo("Success!", self.output_text)

        # hydrophobicity scale function
        # will output message stating where the graph is saved
        # will create popup window displaying the graph

        if self.clicked.get() == self.options[2]:
            self.hydropathy(self.pdb)
            mb.showinfo(
                "Success!", "Graph saved in directory as Hydrophobicity_Scale_" + self.hydro_label + ".png")
            self.tl = Toplevel()
            self.tl.geometry('576x432')
            self.tl.title("Hydrophobicity Scale")
            self.hc = Canvas(self.tl, width=576, height=432)
            self.hc.pack()
            self.hc.create_image(0, 0, image=self.fig,
                                 anchor="nw")

        # secondary structure funcion
        # will output summary message after it is completed
        if self.clicked.get() == self.options[3]:
            self.ss(self.pdb)
            mb.showinfo("Success!", self.out_entry)

        # close contacts function
        # will output summary message
        if self.clicked.get() == self.options[4]:
            self.close(self.pdb)
            mb.showinfo("Success!", self.out_msg)

        # disulfide bond calculation function
        if self.clicked.get() == self.options[5]:
            self.disulfide(self.pdb)
        
        
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
        # destory old window
        self.secondWindow.destroy()

        # set up new window with drop down menu
        self.thirdWindow = Canvas(self, width=760, height=443)
        self.thirdWindow.pack()
        self.thirdWindow.create_image(0, 0, image=self.bg, anchor='nw')

        # Write image citation
        self.thirdWindow.create_text(
            650, 420, text="Image from img.theweek.in", font=self.myFont_citation)

        # write heading
        self.thirdWindow.create_text(380, 35,
                                     text="Choose task below",
                                     font=self.myFont_heading)
        # set up drop down menu
        self.options = ["Hydrogen Bond Partners",
                        "Radius of Gyration",
                        "Hydrophobicity of Protein",
                        "Number and Type of Secondary Structures",
                        "Number and Type of Close Contacts",
                        "Number of Disulfide Bonds"
                        ]

        self.clicked = StringVar()
        self.clicked.set("Choose Below")
        self.drop = OptionMenu(self, self.clicked, *self.options)

        dropdown_menu = self.thirdWindow.create_window(330, 60,
                                                       anchor="nw",
                                                       window=self.drop
                                                       )
        #sets up calculate button
        self.calculate = Button(self,
                                text="Calculate", width=10,
                                command=self.calculate_task)

        self.calculate_c = self.thirdWindow.create_window(350, 100,
                                                          anchor="nw",
                                                          window=self.calculate)
        
        #creates back button
        self.back = Button(self,
                           text="Back", width=10,
                           command=self.second_setup)

        self.back_c = self.thirdWindow.create_window(350, 350,
                                                          anchor="nw",
                                                          window=self.back)
        # places a funny gif
        lbl = ImageLabel(self)
        lbl.place(x=150, y=130)
        photo = lbl.load('calc.gif')


if __name__ == "__main__":
    app = Application(master=root)
    app.mainloop()

