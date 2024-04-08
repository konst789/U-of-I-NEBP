# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:18:25 2023

@author: lkear
"""

import os

print(os.getcwd())
ProgramDirectoryMain = os.getcwd()

if not os.path.exists(ProgramDirectoryMain+'\data'):
    #Checks if there is a data file, creates one if there is not
    os.mkdir('data')
    
DataDirectory = str(ProgramDirectoryMain+'\data')
SourceDirectory = str(ProgramDirectoryMain+'\src')

os.chdir(DataDirectory)
if not os.path.exists(DataDirectory+'/unproccessedProfiles'):
    #Checks if there is a data file, creates one if there is not
    os.mkdir('unproccessedProfiles')
    
if not os.path.exists(DataDirectory+'/proccessedProfiles'):
    #Checks if there is a data file, creates one if there is not
    os.mkdir('proccessedProfiles')