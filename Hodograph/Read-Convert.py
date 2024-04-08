# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:51:26 2023

@author: lkear
"""

import os
import readGrawProfile_alg as rgp

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
                
                ##################################         
        except:
            print("Error Running " +saveName)
            pass

#Save File
if saveData:

    data.to_csv((savePath + "out.csv"))      
    print("Data Saved")

