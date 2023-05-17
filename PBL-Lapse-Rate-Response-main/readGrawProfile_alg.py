# -*- coding: utf-8 -*-
"""
Created on Fri May 28 14:09:51 2021

This program contains the functions to:
    -get the file directory from the user using a Tkinter windows interface 
    -read in and clean profiles from GRAW generated text files
    -query user for save status and location

Last Updated: 10/9/2021 - 14:36PST
@author: Chambers,Alex
"""
import re
import os
import sys
import numpy as np
import pandas as pd
from io import StringIO
from tkinter import filedialog,Tk
from numpy.core.defchararray import lower
from datetime import datetime

def getUserInputFile(prompt):
    print(prompt)
    main = Tk()
    userInput = filedialog.askdirectory()
    main.destroy()
    if userInput == "":
        sys.exit()
    return userInput

def getUserInputTF(prompt):
    print(prompt+" (Y/N)")
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "please enter a 'Y' or 'N'"
        if lower(userInput) == "y":
            return True
        else:
             return

def strip_datetime(path,file):
    x = open(os.path.join(path,file), 'r').readlines()
    flightDT = pd.DataFrame([x[1].split()]).T
    flightDT = flightDT.to_numpy()
    date = ' '.join(flightDT[3:6,0])
    time = flightDT[8,0]

    dateTime = datetime.strptime((date+' '+time), '%d %B %Y %H:%M:%S')
    return dateTime


def readProfile(dataSource,subdirs,path,file):
        def atoi(text):
            return int(text) if text.isdigit() else text
        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text)]
        subdirs.sort(key=natural_keys)
        if file.endswith(".txt"):
            # Used to fix a file reading error
            saveName = (file.split(".", 2))[0]
            contents = ""
            # Check to see if this is a GRAWMET profile
            isProfile = False
            f = open(os.path.join(path, file), 'r')
            print("Running file "+saveName)
            for line in f:
                if line.rstrip() == "Profile Data:":
                    isProfile = True
                    contents = f.read()                   
            f.close()
            if not isProfile:
                print("File "+file +
                      " is either not a GRAWMET profile, or is corrupted.")

            if isProfile:  # Read in the data and perform analysis
                
                # Fix a format that causes a table reading error
                contents = contents.replace("UTC Time", "UTC")
                contents = contents.split("\n")
                contents.pop(1)  # Remove units from temp file
                index = -1
                for i in range(0, len(contents)):  # Find beginning of footer
                    if contents[i].strip() == "Tropopauses:":
                        index = i
                for item in contents:  # Find Tropopause string in footer
                    if '1. Tropopause:' in item:
                        trop = (item.strip())
                if index >= 0:  # Remove footer, if found
                    contents = contents[:index]
                contents = "\n".join(contents)  # Reassemble string
                del index


                # Read in the data
                RawData = pd.read_csv(StringIO(contents),
                                      delim_whitespace=True, na_values=['-'])
                # del contents

                # Find the end of usable data
                badRows = []
                for row in range(RawData.shape[0]):
                    # Check for nonnumeric or negative rise rate
                    if not str(RawData['Rs'].loc[row]).replace('.', '', 1).isdigit():
                        badRows.append(row)
                    elif row > 0 and np.diff(RawData['Alt'])[row-1] <= 2:
                        badRows.append(row)
                    else:
                        for col in range(RawData.shape[1]):
                            # This value appears a lot and is obviously wrong
                            if RawData.iloc[row, col] == 999999.0:
                                badRows.append(row)
                                break
                # Create dataframe of cleaned data
                data = RawData.drop(RawData.index[badRows])
                    #Create dataframe of cleaned data
                data = data.reset_index(drop=True) 
                datetime = strip_datetime(path,file)
                       
                return data, trop, saveName,datetime       
