 # -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 14:32:10 2021
Last Updated: 10/12/2021 - 09:15PST


This is the user interface program for the PBL algorithm
that:
    -Reads and parces GRAWMET profiles into the program
    -Analyzses the PBL using methods:
        -VPT
        -RI
        -PT
    -Calculates atmospheric conditions
    -Determines proper PBL method based on conditions
    -Creates analysis reports
        -printed version in console
        -Printed version in text file (easy to read)
        -CSV version to allow easy data transfer to other programs
        
     
NOTE: this programs location MUST be in the same folder as "readGrawProfile_alg" 
and "AlgorithmFunctions"folder to load subprograms properly   
     
This program has been developed for the use of the NASA-ISGC 
for the purposes of the National Eclipse Ballooning Project
author: Chambers,Alex

"""
import os
import time
import readGrawProfile_alg as rgp
import AlgorithmFunctions as af
import numpy as np





##############################################
#####SETUP TEXT FILE NAMES IF SAVING##########
##############################################
site = 'Tolten'

pblTxtName = "PBLMethods_%s" %(site)
algTxtName = "PBL_AlgorithumResults_%s" %(site)

pblCsvName = "PBLMethodsCSV_%s"%(site)
algCsvName = "PBL_AlgorithumCSV_%s"%(site)

### NO USER-INPUT REQUIRED BEYOND THIS POINT###

##############################################
#########PROGRAM OPERATION####################
##############################################

start_time = time.time()
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
    
output1 = []
output2 = []
millsOutput = []
for path, subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        try:
            profile = rgp.readProfile(dataSource,subdirs,path,file)
            if profile is not None:
                data = profile[0]
                saveName = profile[2]
                datetime = profile[3]
                RunProgram = af.operations(data,saveName)
                PBLResults= af.Selection(RunProgram)
                TotalResults = af.fullOutput(datetime,RunProgram,output1,output2,saveName,PBLResults)
                mills = af.mills700(data,millsOutput,saveName)##################################
        except:                                                 #If not running consecutivly and dont want to skip errors,
            print("Error Running " +saveName)                   #comment this block and the "try" line 72
            pass  
      
if profile is not None:
    Results = af.printConsole(TotalResults,savePath)
    if saveData:
        fileNames = [pblTxtName,algTxtName,pblCsvName,algCsvName]
        textfiles = af.saveTxt(TotalResults,savePath,fileNames)
        mills = np.array(mills)####################################
        np.savetxt("%s/900millsLR"%(savePath),mills,fmt='%s',delimiter=",",encoding="utf-8")      
        print("Data Saved")
    print("\n----- Program operated in %.5s seconds / %.5s minutes -------" %((time.time()-start_time),(time.time()-start_time)/60))
    del start_time,output1,output2
