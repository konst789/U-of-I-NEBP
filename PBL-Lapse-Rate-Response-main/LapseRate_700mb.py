# -*- coding: utf-8 -*-
"""
Created on Wed October 26 14:32:10 2021
Last Updated: 10/10/2022 - 17:00PST


This program calculates the lapse rate of a GRAWMET atmospheric profile
through 700mb above the surface. A first order polynomial fit is applied 
to temperature and altitude profiles, and reported in a positive value.


This program has been developed for the use of the NASA-ISGC 
for the purposes of the National Eclipse Ballooning Project
author: Chambers,Alex
contact: chambers.alexander00@gmail.com
"""

import os 
import readGrawProfile_alg as rgp         
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""NOTE: this programs location MUST be in the same folder as "readGrawProfile_alg" folder 
for it to load the subprogram properly"""

def lapse700mb(data,mills700):
    gndAlt = 50                                             #Ground altitude             
    alt = data['Alt']                                       #Altitude
    temp = data['T']                                        #Temperature

    alt_cut = alt[(alt>=gndAlt)*(alt<=mills700)]            #Altitude values between ground and alt@700mb
    temp_cut = temp[(alt>=gndAlt)*(alt<=mills700)]          #Altitude values between ground and alt@700mb
    slope,intercept = np.polyfit(alt_cut,temp_cut,1)        #Apply first order polynomial fit to above data

    return round(slope*-1000,2)                             #report slope in [°K/m] - slope is negative but reported positive

def fullOutput(output,LR700,saveName):
    output.append((saveName,LR700))                         #pull in list and append resent results to bottom
    return output

dataSource = rgp.getUserInputFile("Select path to data input directory: ")
saveData   = rgp.getUserInputTF("Do you want to save output data?")

if saveData:
    savePrompt = rgp.getUserInputTF("Save to same directory?")
    if savePrompt:
        savePath = dataSource
    elif saveData:
        savePath = rgp.getUserInputFile("Enter path to data output directory: ")
    else:
        savePath = "NA"
else:
    savePath = "NA"
    
output = []
for path,subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        profile = rgp.readProfile(dataSource,subdirs,path,file)
        if profile is not None:
            data = profile[0]
            saveName = profile[2]                                       #Assign Profile Data "data" 
            mills700 = data['Alt'].loc[abs(data['P']-700).idxmin()]     #Altitude location at 700mb
            LR700  = lapse700mb(data,mills700)                          #Run function to find Lapse Rate through 700mb
            print("Lapse @ 700mb= " +str(LR700))
            results = fullOutput(output,LR700,saveName)                 #Send to appending output function
         
header = ['Launch Title','LR - 700mb']
TotalResults = np.array(results)                                        #Make results a numpy array
TotalResults = np.insert(TotalResults,[0],header,axis=0)                #Add the results and header to array
print(TotalResults)
if saveData:
    np.savetxt("%s/LapseRates_Tolten_900mb.txt"%(savePath),TotalResults,fmt='%s',delimiter="\t\t",encoding='utf-8')
