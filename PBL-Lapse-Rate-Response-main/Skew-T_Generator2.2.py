# -*- coding: utf-8 -*-
"""
Author: Alex Chambers
Date Created: 4/9/2021   
Last Edited: 2/18/2022  12:15:00 pm

ISGC

This program generates Skew-T plots from Grawmet Radiosonde Profile Data
with a profile hunting function enabled to find all profiles in 
the selected subdirectory

"""
##################################IMPORT ALL MODULES/PACKAGES#######################################
import time
import sys                                            # Used to control entire program (ie. stop run)
import re
import numpy as np                                    # Numbers (like pi) and math
import matplotlib.pyplot as plt                       # Easy plotting
import pandas as pd                                   # Convenient data formatting, and who doesn't want pandas
from numpy.core.defchararray import lower             # For some reason I had to import this separately
import os                                             # File reading and input
from io import StringIO                               # Used to run strings through input/output functions
import tkinter as tk                                  # Used to create Window Explorer
from tkinter import filedialog, Tk                    # Used to create Window Explorer
import matplotlib.gridspec as gridspec
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import Hodograph, SkewT
from metpy.units import units
import readGrawProfile_alg as rgp


start_time = time.time()
plt.close("all")



#########FUNCTIONS THE PROGRAM WILL CALL#####
def getUserInputFile(prompt):
    print(prompt)
    main = Tk()
    # Creates directory for user to choose (location of profile data)
    userInput = filedialog.askdirectory()
    main.destroy()
    if userInput == "":  # If user cancels or does not select, exit the program
        sys.exit()
    return userInput  # Return the file directory user chos

def getUserInputTF(prompt):
    print(prompt+" (Y/N)")  # Prompts user for a Yes or No
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "Please enter a 'Y' or 'N'"
    if lower(userInput) == "y":
        return True
    else:
        return 
    
def getUserInputFig(prompt):
    print(prompt+"(Y/N)")
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "Please enter a 'Y' or 'N'"
    if lower(userInput) == "y":
            return True
    else:
        return

def SkewTGenerator(data,saveName):
    #Pull specific columns of data relavent to the SkewT
    T = data['T'].values*units.degC                         #make dataframe column with units
    P = data['P'].values*units.hPa
    Td = data['Dewp.'].values*units.degC
    P_wind = P[::400]                                        #use every 40'th wind datapoint (gets really clutterd)
    alt = data['Alt'].values*units.m
    wind_speed = data['Ws'][::400].values*units.knots
    wind_dir = data['Wd'][::400].values*units.degrees
    u,v = mpcalc.wind_components(wind_speed,wind_dir)
    
    ###Set up Skew T generator
    fig = plt.figure(figsize=(15,15))                       #build figure workspace
    gs  = gridspec.GridSpec(3,3)
    skew = SkewT(fig,rotation=30)                           #call SkewT from the package

    skew.plot(P,T,'r')
    skew.plot(P,Td,'black')
    skew.plot_barbs(P_wind,u,v,y_clip_radius=.01)
    skew.ax.set_ylim(1030,100)                              #set y-limits
    skew.ax.set_xlim(-55,40)                                #set x-limits
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    
    
    ######THIS IS TO ADD ALTITUDE [M] SO YOU CAN START TO GET A CORRELATION######
    ######THE ACTUAL PROGRAM DOSNT INCLUDE THIS, BUT MAY HELP GETTING STARTED####
    decimate = 220   #every 220 datapoints, add the alt to the plot
    for p,t,h in zip(P[::decimate],T[::decimate],alt[::decimate]):
        if p>=100*units.hPa:
            skew.ax.text(t,p,round(h,0),)
    #############################################################################        
    
    plt.title(saveName,fontsize=20)         #add a title to the plot
    if saveFigFiles:                        #chack if your user input was to save
        plt.savefig('%s/SkewT_%s.jpg' %(dataSource,saveName),dpi=200)   #save figure in the folder you grabed it from
    plt.show()                              #show the figure in the screen
    return
    
########## FILE RETRIEVAL SECTION ##########
# Need to find all txt files in dataSource directory and iterate over them
dataSource = getUserInputFile(
    "Select path to data input directory: ")  # File directory location
saveFigFiles = getUserInputFig(
    "Save Skew-T Plots?")

for path, subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
            profile = rgp.readProfile(dataSource,subdirs,path,file)
            if profile is not None:                                     #check to make sure it actually grabbed a REAL profile
                data = profile[0]                                       #make a dataframe from the retrival subprogram
                saveName = profile[2]                                   #grab the saveName from the retrival subprogram
                makeSkewT = SkewTGenerator(data,saveName)               #go to the function to make the skew T
                
                
 
print("Finished Analysis of All Subdirectories in %s" % (dataSource))
print("\n------ Program operated in %s seconds -------" %(time.time() - start_time))
# 