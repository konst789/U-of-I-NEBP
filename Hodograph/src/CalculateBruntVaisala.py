# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 16:22:07 2023

@author: gera2396
"""
import numpy as np
import OutputFormater as out


def CalculateBruntVaisalaSquared (Tpotential,Alt,DoPrintOutput):
    out.pim('Begin Brunt-Vaisala Squared Calculation',DoPrintOutput)
    
    dt=np.diff(Tpotential)  # get an array of the change of potential temperature
    Dt=np.append(0,dt) # add a zero for first value to make arrays same length
    dz=np.diff(Alt) #get an array of the change of altitude
    Dz=np.append(0,dz) # add a zero for first value to make arrays same length 
    #Tpot=np.append(0,Tpotential)
    
    #Calculate brunt vaisala squared
    BruntVaisalaSquared=((9.80665/Tpotential)*(Dt/Dz))
    
    out.pim('Brunt-Vaisala Squared Calculation Complete',DoPrintOutput)
    return BruntVaisalaSquared