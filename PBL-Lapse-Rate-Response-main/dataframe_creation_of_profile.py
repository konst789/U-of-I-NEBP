# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:24:20 2023

@author: konge
"""

import os
import readGrawProfile_alg as rgp  
import numpy as np
import pandas as pd
from datetime import datetime


dataSource = rgp.getUserInputFile("Select path to data input directory: ")
#saveData   = rgp.getUserInputTF("Do you want to save output data?")
output = []
for path,subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        profile = rgp.readProfile(dataSource,subdirs,path,file)
        if profile is not None:
            data = profile[0]
            saveName = profile[2]  
print(data)
filelocation=r'C:/Users/konge/OneDrive - University of Idaho/NASA Ballonn/All_Flight_Data/Chile Flight Profile Data/alt vs vpt/' # folder location to create csv or excel file

filename='data1.csv' # file name for csv

data.to_csv(filelocation+filename)

# excelfile='data2.xlsx' #name of excel file
# data.to_excel(filelocation+excelfile)