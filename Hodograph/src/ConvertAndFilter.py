# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 12:54:53 2023

@author: lkear
"""

#Dependencies
import os
import readGrawProfile_alg as rgp
import numpy as np
import pandas as pd

#########Read From File and convert Data####################
                 
dataSource = rgp.getUserInputFile("Select path to data input directory: ")
saveData   = rgp.getUserInputTF("Do you want to save output data?")

if saveData:
    savePrompt = rgp.getUserInputTF("Save to same directory?")
    if savePrompt: 
        savePath = dataSource
    elif saveData:
        savePath = rgp.getUserInputFile("Enter path to data output directory:")
    else:
        savePath = "NA"
else:
    savePath = "NA"
    
for path, subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        try:
            profile = rgp.readProfile(dataSource,subdirs,path,file)
            if profile is not None:
                data = profile[0]
                saveName = profile[2]
                datetime = profile[3]
                         
        except:
            print("Error Running " +saveName)
            pass

#Save File
if saveData:
    data.to_csv((saveName + "_Proccessed.csv"))      
    print(saveName +"_Proccessed.csv Saved")
